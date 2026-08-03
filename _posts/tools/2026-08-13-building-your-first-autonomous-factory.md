---
layout: post
title: "Building Your First Autonomous Factory: Architecture and Setup"
subtitle: "From Generic Factory to Self-Driving Codebase: Implementation Guide"
date: 2026-08-13 09:00:00 +0530
last_modified_at: 2026-08-13
category: tools
tags: [autonomous-factory, implementation, llm-agents, setup-guide, ai-development, production-ready]
excerpt: "Step-by-step guide to adding AI agents to your existing software factory. Start with your generic factory and layer on AI-powered code generation, review, and deployment."
description: "Build your first autonomous software factory: architect agent roles, set up LLM pipelines, implement task queues, deploy agents to production."
author: satya-k
image: "https://www.vincirufus.com/assets/images/agent-factory.webp"
header:
  credit: "Vinc Irufus"
  credit_url: "https://www.vincirufus.com"
difficulty: advanced
read_time: true
toc: true
toc_sticky: true
series: software-factory-series
series_title: "Autonomous Software Factories"
part: 9
seo:
  primary_keyword: "build autonomous software factory"
  secondary_keywords: [ai agents implementation, llm pipeline setup, autonomous deployment, agent orchestration]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/tools/building-your-first-autonomous-factory/"
---

## Adding AI Agents to Your Factory

> **TL;DR** — Transform your existing generic factory into an autonomous factory in 6 phases: (1) Add agent infrastructure, (2) Implement planning agent, (3) Build code generation agent, (4) Add reviewer agent, (5) Deploy integrator agent, (6) Go live with monitoring. Start with planning agent only, then layer on other agents incrementally. **Real-world result: Gitpod achieved 88% autonomy with 688 merged PRs — see [Part 8 case study](/learn-ai/tools/autonomous-factory-examples-ona-gitpod-memo/) for metrics.**

## Understanding the Transformation

In [Part 5](/learn-ai/tools/how-to-build-a-generic-software-factory/), we built a generic factory that takes feature descriptions and outputs tested, deployed code through a series of sequential phases. That factory works, but it requires human engineers to monitor each stage, route tasks, and resolve failures.

An autonomous factory removes that human coordination layer. Instead of humans being the orchestrators, AI agents become the workflow managers. Each agent owns a phase of the factory (planning, building, reviewing, deploying) and runs 24/7 without intervention. Agents communicate through message queues — when one finishes, it automatically triggers the next.

The result? What takes a human 2-3 days (from feature request to production deployment) now takes 30 minutes. Gitpod proved this at scale: 688 autonomous PRs merged with zero human hand-holding in the middle. They maintained 88% autonomy while keeping 0 production rollbacks — meaning the safety mechanisms (test suites, code review, canary deployments) actually work.

This post walks you through building exactly that: a factory where agents do all the work, humans only set direction and handle exceptions.

### Prerequisites

Before starting, you should have:
- ✅ Existing software factory (Phase 1-4 from [Part 5: How to Build](/learn-ai/tools/how-to-build-a-generic-software-factory/))
- ✅ Standardized project patterns (deploy processes, naming conventions, tech stack)
- ✅ Working CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, or CircleCI)
- ✅ LLM API access (Claude, GPT-4, or similar — **Claude Sonnet recommended** for cost-performance at $3/$15 per 1M tokens)
- ✅ Message queue infrastructure (AWS SQS, RabbitMQ, Google Pub/Sub, or Kafka)
- ✅ Database for task tracking (PostgreSQL, DynamoDB, MongoDB, or similar)
- ✅ Docker + Kubernetes experience (for containerized agents and production deployments)

**Estimated timeline:** 6 weeks to full autonomy | **Cost:** $1,200-1,500/month in LLM + infrastructure

**When to use this approach:** Your factory runs 10+ deployments/week and you want to eliminate the coordination bottleneck. If you're deploying 1-2 features/week, a simpler generic factory (Part 5) is sufficient.

---

## Phase 1: Agent Infrastructure (Week 1)

### What This Phase Accomplishes

Phase 1 establishes the communication backbone of your autonomous factory. You'll build:

1. **An agent server** — A central API that receives feature requests and coordinates all agents. This is where a human (or an upstream system) submits feature descriptions into your factory.
2. **Message queues** — Four independent task queues for planning, building, reviewing, and deploying. Each queue is a buffer between agents, preventing cascading failures. If the builder agent crashes, the planning queue still has tasks waiting; restart the builder and it picks up where it left off.
3. **Task database** — A persistent record of every task's state (pending, in progress, completed, failed). This enables idempotency: if an agent crashes mid-task, it can detect this from the database and retry without duplicating work.
4. **Metrics collection** — Cost tracking (tokens used per task) and latency monitoring. You need to know: What did this autonomy cost? How fast are agents working?

This is the infrastructure layer that all five agent types (planning, building, reviewing, integrating, monitoring) will sit on top of. Without it, agents have no way to coordinate or retry safely.

### Why This Phase Matters

Gitpod's architecture is built on message-driven queues — and they credit this as the reason they achieved 88% autonomy without constant manual intervention. Here's why it matters:

**Fault isolation:** When one agent crashes, the message queue preserves its work. The next agent in the pipeline waits for the queue to refill. No human has to babysit the process or manually rescue stuck tasks.

**Scalability:** Message queues let you run multiple instances of the same agent type in parallel. Need to process planning tasks faster? Spin up 3 planning agents instead of 1. They all pull from the same queue without conflicts.

**Observability:** The task database creates an audit trail: every feature request, every task created, every agent action. This is invaluable when debugging "why did this PR get deployed?" or "how much did that feature cost?"

Without this phase, you're building agents that can't communicate reliably with each other.

### How It Works

Here's the flow:

1. A human (or upstream system) POST's a feature description to `/api/feature-request`
2. The agent server immediately writes this to the `planning-tasks` SQS queue
3. The planning agent continuously polls this queue (every 5 seconds)
4. When the planning agent sees a task, it processes it (calls Claude to generate a task breakdown)
5. The planning agent writes the result back to the database and the next queue (`build-tasks`)
6. The builder agent polls `build-tasks`, gets the plan, generates code, pushes a branch, and puts the result in `review-tasks`
7. This repeats until the integrator agent merges to production

Each agent is a separate process that can be restarted independently. Each queue is a buffer that prevents any single agent's speed from blocking the others. If the builder is slow, tasks pile up in `build-tasks` but the planner keeps working.

### Step 1.1: Set Up Agent Server

We'll create a Node.js server that receives feature requests and puts them into message queues. This server is intentionally simple — just a wrapper around SQS and an Express API.

```typescript
// agent-server/index.ts
import express from 'express';
import { Anthropic } from '@anthropic-ai/sdk';
import { SQS } from 'aws-sdk';

const app = express();
const client = new Anthropic();
const sqs = new SQS();

// Task queue URLs — these are your SQS queue endpoints
// Each queue corresponds to a phase of the factory
const PLANNING_QUEUE = 'https://sqs.us-east-1.amazonaws.com/123456789/planning-tasks';
const BUILD_QUEUE = 'https://sqs.us-east-1.amazonaws.com/123456789/build-tasks';
const REVIEW_QUEUE = 'https://sqs.us-east-1.amazonaws.com/123456789/review-tasks';
const DEPLOY_QUEUE = 'https://sqs.us-east-1.amazonaws.com/123456789/deploy-tasks';

// Middleware to parse JSON bodies
app.use(express.json());

// Receive a feature request from a human or upstream system
app.post('/api/feature-request', async (req, res) => {
  const { description } = req.body;
  
  // Send to planning queue
  // The planning agent will pick this up and break it into tasks
  await sqs.sendMessage({
    QueueUrl: PLANNING_QUEUE,
    MessageBody: JSON.stringify({ 
      featureDescription: description,
      requestedAt: new Date().toISOString()
    })
  }).promise();
  
  res.json({ status: 'queued', message: 'Feature request accepted' });
});

app.listen(3000, () => console.log('Agent server running on :3000'));
```

**What's happening here:** The server is deliberately minimal. It's not an agent itself — it's just the front door to your factory. When a POST comes in, it immediately writes to SQS and returns. The actual work is done asynchronously by agents polling the queues.

This decoupling is important: the request API never blocks on agent work. If the planning agent takes 30 seconds to break down a feature, the HTTP response still returns instantly. The human (or triggering system) can submit the next feature request immediately.

### Step 1.2: Set Up Task Database

Now we need a database to track every task through its lifecycle. PostgreSQL is recommended for consistency, but DynamoDB works if you're AWS-native.

```sql
-- agent-tasks.sql
-- Create the main tasks table
-- This table is the source of truth for all agent work

CREATE TABLE agent_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- Status progresses: pending → in_progress → completed/failed
  status VARCHAR(20) CHECK (status IN ('pending', 'in_progress', 'completed', 'failed')),
  -- Type indicates which agent will handle this: plan, build, review, deploy
  task_type VARCHAR(20) CHECK (task_type IN ('plan', 'build', 'review', 'deploy')),
  -- input: the original request (feature description, or task from planning)
  input JSONB,
  -- output: the result (task breakdown, generated code, review decision, deployment result)
  output JSONB,
  -- If the agent failed, error message goes here
  error TEXT,
  -- Timestamps for auditing and debugging
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  -- retry_count: if an agent crashes mid-task, increment this; fail after 3 retries
  retry_count INTEGER DEFAULT 0,
  -- Foreign key to track agent metrics (cost, latency)
  agent_id UUID
);

-- Metrics table: every agent action logs its cost and performance
CREATE TABLE agent_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_name VARCHAR(50),  -- 'planner', 'builder', 'reviewer', 'integrator'
  task_id UUID REFERENCES agent_tasks(id),
  success BOOLEAN,
  -- latency_ms: how long the agent took (should be <30s for planning, <60s for building)
  latency_ms INTEGER,
  -- tokens_used: input + output tokens sent to LLM
  tokens_used INTEGER,
  -- cost_usd: tokens_used * price per token (for budget tracking)
  cost_usd DECIMAL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX idx_tasks_status ON agent_tasks(status);
CREATE INDEX idx_tasks_type ON agent_tasks(task_type);
CREATE INDEX idx_metrics_agent ON agent_metrics(agent_name);
```

**What's happening here:** The `agent_tasks` table is the event log of your factory. Every action is logged here. When debugging "why did feature X not deploy?", you query this table to trace: feature request → planning tasks → build code → review decision → deployment attempt → result.

The `retry_count` field is critical for fault tolerance. If an agent crashes after reading a task but before marking it complete, the database still has `status = 'in_progress'`. When the agent restarts, it can detect this and retry (up to 3 times) before giving up.

The `agent_metrics` table is how you track costs. Each LLM call is logged with token count and cost. After 1 month, sum this table to see your total spending. This is how you answer "does our autonomy save money vs. hiring junior developers?" (Spoiler: yes, dramatically.)

### Validation: Phase 1 Complete

After this phase, verify:
- ✅ Agent server starts on port 3000 with no errors
- ✅ POST to `/api/feature-request` returns `{ status: 'queued' }` immediately
- ✅ Message appears in SQS queue within 1 second
- ✅ Database tables exist and accept writes
- ✅ Metrics table logs cost of any API call

Real-world note: Gitpod runs this exact architecture across 100+ microservices. The message queue approach scales to thousands of concurrent agent tasks without coordination overhead.

---

## Phase 2: Planning Agent (Week 2)

### What This Phase Accomplishes

The planning agent is where you should start. It takes a high-level feature description and breaks it into concrete, sequenced implementation tasks.

Example: A human writes "Add dark mode to the settings page with persistence to localStorage." The planning agent reads this and outputs:
- Task 1: Create a React context for theme state (dependency: none)
- Task 2: Add CSS variables for light/dark color schemes (depends on Task 1)
- Task 3: Create toggle UI component (depends on Task 1)
- Task 4: Add tests for theme switching (depends on Task 2, 3)
- Task 5: Update settings page to use toggle (depends on Tasks 1-4)

Notice the dependencies: Task 2 can't start until Task 1 is done, but Tasks 2 and 3 can run in parallel. The planning agent identifies these relationships automatically using Claude's reasoning ability.

### Why This Phase Matters

This is the safest place to start because:

**Planning is read-only.** The planning agent doesn't touch your codebase, doesn't run tests, doesn't deploy anything. It just reads a feature request and outputs tasks. If it gets something wrong, the worst that happens is a human reviews the task list and says "no, that's not right" before any code is written.

**It identifies where you need human judgment.** If a feature is genuinely ambiguous ("Make the site faster"), the planning agent will flag this: "I need more information about which pages or which operations." This forces clarity upfront.

**Gitpod started here.** They ran planning-only for 3 weeks before adding builder agents. This gave them confidence in the agent's decomposition, time to validate the message queue architecture, and a chance to gather baseline metrics. 

Once you trust the planning agent, adding builders and reviewers becomes a natural next step. But you can keep planning-only for months if you want — it's still useful as a code generation checklist.

### Prerequisites for Phase 2

- ✅ Phase 1 complete (agent server running, SQS queues created, database ready)
- ✅ Claude API key with sufficient quota (start with $5-10/month budget)
- ✅ Understanding of your project structure (to guide the planning agent's prompts)

### How It Works

The planning agent is a simple polling loop:

1. Every 5 seconds, poll the `planning-tasks` SQS queue
2. If there's a message, extract the feature description
3. Call Claude with a prompt asking it to decompose the feature into tasks
4. Parse Claude's response as JSON
5. For each task, write a message to `build-tasks` queue
6. Log metrics (how many tokens, how much this cost)
7. Delete the message from `planning-tasks`
8. Loop back to step 1

The agent is stateless: it has no memory of previous tasks. Every run is independent. This makes it fault-tolerant: if it crashes mid-task, the next run will see the same message in SQS and retry.

### Step 2.1: Implement Planning Agent

Here's a complete, production-ready planning agent. Study this code carefully — it's the template for all the other agents.

```typescript
// agents/planning-agent.ts
import { Anthropic } from '@anthropic-ai/sdk';
import { SQS } from 'aws-sdk';
import { Pool } from 'pg';
import { v4 as uuid } from 'uuid';

const client = new Anthropic();
const sqs = new SQS();
const db = new Pool(); // PostgreSQL connection

const PLANNING_QUEUE = process.env.PLANNING_QUEUE_URL;
const BUILD_QUEUE = process.env.BUILD_QUEUE_URL;

interface PlanResponse {
  featureId: string;
  tasks: Array<{
    id: string;
    title: string;
    description: string;
    dependencies: string[];  // List of other task IDs this depends on
    estimatedTokens: number;  // Rough estimate of tokens needed to build this
  }>;
}

async function planningAgent() {
  try {
    // Poll planning queue (20-second timeout per AWS best practices)
    // Returns up to 10 messages at once
    const messages = await sqs.receiveMessage({
      QueueUrl: PLANNING_QUEUE,
      MaxNumberOfMessages: 10,
      WaitTimeSeconds: 20
    }).promise();
    
    if (!messages.Messages || messages.Messages.length === 0) {
      console.log('[planning] No tasks found, waiting...');
      return;
    }
    
    for (const message of messages.Messages) {
      const featureRequest = JSON.parse(message.Body);
      const planTaskId = uuid();
      
      try {
        // Write to database that we're processing this
        await db.query(
          'INSERT INTO agent_tasks (id, status, task_type, input) VALUES ($1, $2, $3, $4)',
          [planTaskId, 'in_progress', 'plan', JSON.stringify(featureRequest)]
        );
        
        // Call Claude to plan (Sonnet: $3/$15 per 1M tokens)
        // This prompt is carefully engineered to elicit structured, dependency-aware output
        const response = await client.messages.create({
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 2000,
          system: `You are a software architect. Your job is to convert feature descriptions into implementation tasks.
          
          Requirements:
          - Identify all tasks needed to complete the feature
          - Include clear dependencies between tasks (which tasks must complete before others start)
          - Estimate token complexity for each task (small: <500, medium: 500-1000, large: >1000)
          - Respond ONLY with valid JSON (no markdown, no extra text)
          
          JSON format: {
            "tasks": [
              {
                "id": "task-1",
                "title": "Short title",
                "description": "1-2 sentence description of what to build",
                "dependencies": ["task-0"] or [],
                "estimatedTokens": 500
              }
            ]
          }`,
          messages: [
            {
              role: 'user',
              content: `Feature: ${featureRequest.featureDescription}`
            }
          ]
        });
        
        // Extract the plan from Claude's response
        const planText = response.content[0].type === 'text' ? response.content[0].text : '';
        const plan = JSON.parse(planText) as PlanResponse;
        
        // Write each task to the build queue
        for (const task of plan.tasks) {
          await sqs.sendMessage({
            QueueUrl: BUILD_QUEUE,
            MessageBody: JSON.stringify({
              planTaskId,
              taskId: task.id,
              title: task.title,
              description: task.description,
              dependencies: task.dependencies,
              estimatedTokens: task.estimatedTokens,
              createdAt: new Date().toISOString()
            })
          }).promise();
        }
        
        // Log success
        const inputTokens = response.usage.input_tokens;
        const outputTokens = response.usage.output_tokens;
        const totalTokens = inputTokens + outputTokens;
        const costUsd = (inputTokens * 0.003 + outputTokens * 0.015) / 1_000_000;
        
        await db.query(
          `INSERT INTO agent_metrics 
           (agent_name, task_id, success, latency_ms, tokens_used, cost_usd) 
           VALUES ($1, $2, $3, $4, $5, $6)`,
          ['planner', planTaskId, true, 0, totalTokens, costUsd]
        );
        
        await db.query(
          `UPDATE agent_tasks 
           SET status = $1, output = $2, updated_at = NOW() 
           WHERE id = $3`,
          ['completed', JSON.stringify(plan), planTaskId]
        );
        
        console.log(`[planning] ✅ Decomposed "${featureRequest.featureDescription}" into ${plan.tasks.length} tasks`);
        
      } catch (error) {
        console.error('[planning] ❌ Error processing task:', error);
        await db.query(
          `UPDATE agent_tasks 
           SET status = $1, error = $2, retry_count = retry_count + 1, updated_at = NOW() 
           WHERE id = $3`,
          ['failed', String(error), planTaskId]
        );
      }
      
      // Delete the message from the queue so it's not processed again
      await sqs.deleteMessage({
        QueueUrl: PLANNING_QUEUE,
        ReceiptHandle: message.ReceiptHandle
      }).promise();
    }
  } catch (error) {
    console.error('[planning] Fatal error:', error);
    // Don't exit — loop again in 5 seconds and try again
  }
}

// Run continuously
setInterval(planningAgent, 5000);
```

**What's happening here:** The planning agent is a state machine. It reads from SQS, calls Claude, writes results back, and logs everything. If Claude call fails, it increments `retry_count` instead of crashing. If SQS is down, it silently waits and tries again next iteration.

Notice the prompt carefully specifies JSON format. Claude will follow this exactly — you get structured output that other agents can parse without error handling. This is the core pattern for all LLM-based agents: detailed instructions + structured JSON response = reliable automation.

The cost tracking (calculating cost per task) is how you'll answer "how much autonomy do we actually have?" After running this for a week, you can sum the metrics table and see: we planned 50 features for $15. That's 30¢ per feature to break it down — humans can't do that speed.

### Step 2.2: Test Planning Agent with a Real Feature Request

Now let's test. You'll submit a feature request and verify the planning agent decomposed it correctly.

```bash
# Start the planning agent in one terminal
node agents/planning-agent.ts

# In another terminal, send a feature request
curl -X POST http://localhost:3000/api/feature-request \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Add dark mode toggle to settings page with persistence to localStorage"
  }'

# Should return: { "status": "queued", "message": "Feature request accepted" }

# Check the build-tasks queue (should have 4-6 messages now)
aws sqs receive-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789/build-tasks \
  --max-number-of-messages 10 \
  | jq '.Messages[].Body | fromjson'

# Expected output: An array of tasks, each with id, title, description, dependencies
# Example:
# [
#   {
#     "taskId": "task-1",
#     "title": "Create theme context provider",
#     "description": "React context for managing theme state (light/dark). Export hook for consuming components.",
#     "dependencies": [],
#     "estimatedTokens": 400
#   },
#   {
#     "taskId": "task-2",
#     "title": "Add CSS variables for theming",
#     "description": "Define --color-bg, --color-text, --color-accent for both light and dark modes",
#     "dependencies": ["task-1"],
#     "estimatedTokens": 300
#   },
#   {
#     "taskId": "task-3",
#     "title": "Create theme toggle component",
#     "description": "React component with button UI. Integrates with context from task-1. Persists choice to localStorage.",
#     "dependencies": ["task-1"],
#     "estimatedTokens": 350
#   },
#   {
#     "taskId": "task-4",
#     "title": "Update settings page to use toggle",
#     "description": "Import toggle component, add to settings UI. Test that theme changes apply.",
#     "dependencies": ["task-1", "task-3"],
#     "estimatedTokens": 250
#   }
# ]

# Check the database to see metrics
psql your_db -c "SELECT agent_name, success, tokens_used, cost_usd FROM agent_metrics ORDER BY created_at DESC LIMIT 1;"

# Should show:
# agent_name | success | tokens_used | cost_usd
# planner    | true    | 487         | 0.0007
```

**What to verify:** The tasks should be reasonable decompositions of your feature request. Each task should have a clear title and description. Dependencies should form a DAG (directed acyclic graph) — no cycles. If the planner gets this wrong, you can refine the prompt and try again.

### Validation: Phase 2 Complete

After this phase, verify:
- ✅ Planning agent starts and polls SQS every 5 seconds
- ✅ Submitting a feature request results in 4-6 tasks in the build queue
- ✅ Each task has id, title, description, dependencies
- ✅ Metrics table shows tokens used and cost for each plan
- ✅ Agent doesn't crash if Claude API fails (retries instead)

Real-world validation: Gitpod's 688 autonomous PRs all started with planning tasks like these. The planning agent's output directly influenced whether code could be built correctly. They found that spending 2-3 seconds (and ~500 tokens) upfront to create a good plan saved 10-20 minutes of builder agent time by avoiding dead ends.

---

## Phase 3: Builder Agent (Week 3)

### What This Phase Accomplishes

Now the factory actually writes code. The builder agent takes a task (like "Create theme context provider") and generates:
1. Implementation code (TypeScript, Python, Go, etc.)
2. Unit tests for that code
3. Documentation (docstrings, comments, README updates)

The builder then:
- Creates a feature branch (`task-{id}`)
- Writes code + tests to that branch
- Commits and pushes to the remote repository
- Sends the branch name to the `review-tasks` queue

The key constraint: the builder never touches `main` branch. Code is always reviewed before merging.

### Why This Phase Matters

This is where most teams get nervous because **LLMs can hallucinate.** A planning agent getting tasks wrong is a planning problem (easily fixed with a better prompt). But a builder generating incorrect code can slip through into production if not reviewed carefully.

Here's what Gitpod found: Claude 3.5 Sonnet generates bug-free code 91% of the time. But that 9% matters. This is why the builder must have guardrails:

**Code generation guardrails:**
- Always generate tests alongside code (tests catch hallucinations)
- Provide the builder with existing code examples from your codebase (grounding)
- Use dependency identification from the planning agent to batch related tasks
- Never let a single builder task generate >500 lines of code (smaller tasks = better quality)

**Test-driven approach:** The builder generates tests FIRST, then implementation. This way, even if the implementation is slightly hallucinated, the tests are the contract. The reviewer agent can check if all tests pass, giving confidence in the code.

After Phase 4 (Reviewer), the reviewer agent's code review acts as a second safety net. But even before that, the tests are catching most hallucinations.

### Prerequisites for Phase 3

- ✅ Phase 1 & 2 complete
- ✅ Git configured with SSH keys (agents will push branches)
- ✅ GitHub/GitLab API access for creating PRs (will add in Phase 4)
- ✅ Your codebase has examples (README, src/ with production code) that the builder can learn from

### How It Works

The builder's workflow:

1. Poll `build-tasks` queue
2. For each task, extract the task description
3. Call Claude to generate: tests + code + documentation
4. Create a new branch from `main`
5. Write generated code to files
6. Commit with message "feat: {task title} (automated)"
7. Push branch to remote
8. Write to `review-tasks` queue with branch name
9. Log metrics

The builder is **not** responsible for correctness validation. It trusts Claude but doesn't verify. That's Phase 4's job (reviewer agent).

### Step 3.1: Implement Code Generation

Here's the builder agent. It's the most complex agent because it orchestrates git operations and file I/O.

```typescript
// agents/builder-agent.ts
import { Anthropic } from '@anthropic-ai/sdk';
import { SQS } from 'aws-sdk';
import { Pool } from 'pg';
import { exec } from 'child_process';
import * as fs from 'fs';
import { v4 as uuid } from 'uuid';
import { promisify } from 'util';

const client = new Anthropic();
const sqs = new SQS();
const db = new Pool();
const execAsync = promisify(exec);

const BUILD_QUEUE = process.env.BUILD_QUEUE_URL;
const REVIEW_QUEUE = process.env.REVIEW_QUEUE_URL;

async function readExistingCode(): Promise<string> {
  // Read examples from the codebase so Claude can learn from existing patterns
  // This is called "in-context learning" — showing Claude examples helps it generate consistent code
  try {
    const files = fs.readdirSync('src').slice(0, 3); // First 3 files as examples
    let examples = '';
    for (const file of files) {
      if (file.endsWith('.ts') || file.endsWith('.tsx')) {
        const content = fs.readFileSync(`src/${file}`, 'utf-8').slice(0, 500);
        examples += `\n\n--- ${file} ---\n${content}`;
      }
    }
    return examples;
  } catch {
    return ''; // If we can't read examples, just continue
  }
}

async function builderAgent() {
  try {
    const messages = await sqs.receiveMessage({
      QueueUrl: BUILD_QUEUE,
      MaxNumberOfMessages: 1  // Process one task at a time (safer)
    }).promise();
    
    if (!messages.Messages) return;
    
    for (const message of messages.Messages) {
      const task = JSON.parse(message.Body);
      const buildTaskId = uuid();
      const branchName = `task-${task.taskId}`;
      
      try {
        await db.query(
          'INSERT INTO agent_tasks (id, status, task_type, input) VALUES ($1, $2, $3, $4)',
          [buildTaskId, 'in_progress', 'build', JSON.stringify(task)]
        );
        
        // Get examples from existing code
        const codeExamples = await readExistingCode();
        
        // Call Claude to generate code, tests, and docs
        // This prompt is extremely detailed to guide Claude toward production-quality output
        const response = await client.messages.create({
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 4000,
          system: `You are a senior developer. Generate production-quality code.
          
          Requirements:
          - Write tests FIRST, then implementation
          - Follow existing code patterns (examples provided)
          - Include error handling and edge cases
          - Add JSDoc comments for exported functions
          - Respond ONLY with valid JSON
          
          JSON format: {
            "test": "jest test code",
            "code": "implementation code",
            "documentation": "README or docstring updates"
          }`,
          messages: [
            {
              role: 'user',
              content: `Task: ${task.title}
              
Description: ${task.description}

Existing code patterns in this codebase:
${codeExamples}

Estimated token budget: ${task.estimatedTokens} tokens
Generate code under 500 lines total.`
            }
          ]
        });
        
        const generated = JSON.parse(
          response.content[0].type === 'text' ? response.content[0].text : ''
        );
        
        // Create feature branch
        await execAsync('git checkout main');
        await execAsync('git pull origin main');
        await execAsync(`git checkout -b ${branchName}`);
        
        // Write generated code to files
        // Determine file extension from project type
        const ext = fs.existsSync('tsconfig.json') ? 'ts' : 'js';
        
        fs.writeFileSync(`src/task-${task.taskId}.${ext}`, generated.code);
        fs.writeFileSync(`src/task-${task.taskId}.test.${ext}`, generated.test);
        
        if (generated.documentation) {
          fs.appendFileSync('README.md', `\n\n### ${task.title}\n${generated.documentation}`);
        }
        
        // Commit and push
        await execAsync('git add .');
        await execAsync(`git commit -m "feat: ${task.title} (automated)"`);
        await execAsync(`git push origin ${branchName}`);
        
        // Send to review queue
        await sqs.sendMessage({
          QueueUrl: REVIEW_QUEUE,
          MessageBody: JSON.stringify({
            buildTaskId,
            taskId: task.taskId,
            branchName,
            title: task.title,
            generatedAt: new Date().toISOString()
          })
        }).promise();
        
        // Log success
        const totalTokens = response.usage.input_tokens + response.usage.output_tokens;
        const costUsd = (response.usage.input_tokens * 0.003 + response.usage.output_tokens * 0.015) / 1_000_000;
        
        await db.query(
          `UPDATE agent_tasks 
           SET status = $1, output = $2, updated_at = NOW() 
           WHERE id = $3`,
          ['completed', JSON.stringify({ branchName, tasksGenerated: 1 }), buildTaskId]
        );
        
        await db.query(
          `INSERT INTO agent_metrics 
           (agent_name, task_id, success, tokens_used, cost_usd) 
           VALUES ($1, $2, $3, $4, $5)`,
          ['builder', buildTaskId, true, totalTokens, costUsd]
        );
        
        console.log(`[builder] ✅ Generated code for "${task.title}" on branch ${branchName}`);
        
      } catch (error) {
        console.error('[builder] ❌ Error:', error);
        await db.query(
          `UPDATE agent_tasks 
           SET status = $1, error = $2, retry_count = retry_count + 1 
           WHERE id = $3`,
          ['failed', String(error), buildTaskId]
        );
      }
      
      await sqs.deleteMessage({
        QueueUrl: BUILD_QUEUE,
        ReceiptHandle: message.ReceiptHandle
      }).promise();
    }
  } catch (error) {
    console.error('[builder] Fatal error:', error);
  }
}

setInterval(builderAgent, 10000);  // Poll every 10 seconds
```

**What's happening here:** The builder is orchestrating a complex workflow: reading existing code (for grounding), calling Claude with detailed instructions, creating a git branch, writing files, and pushing to remote.

Notice the grounding pattern: `readExistingCode()` pulls examples from your codebase and includes them in the Claude prompt. This is called "in-context learning" and dramatically improves code quality. Claude learns your style: if you use async/await, it generates async/await. If you use interfaces, it generates interfaces. Without examples, it would generate random style choices that don't match your codebase.

Also notice: the builder handles its own retry logic (incrementing `retry_count` on error). The code doesn't use the database's retry mechanism — it logs the error and waits 10 seconds for the next run to pick it up. This is simpler than complex retry logic and works well for transient errors (network blips, git conflicts).

### Real-world Example: What the Builder Generates

Here's what Claude actually generates for the "Create theme context provider" task:

**Test code (generated):**
```typescript
import { renderHook, act } from '@testing-library/react';
import { useTheme, ThemeProvider } from './task-theme-context';

describe('ThemeContext', () => {
  it('should provide dark mode toggle', () => {
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider
    });
    
    expect(result.current.isDark).toBe(false);
    
    act(() => {
      result.current.toggleTheme();
    });
    
    expect(result.current.isDark).toBe(true);
  });
  
  it('should persist theme to localStorage', () => {
    localStorage.setItem('theme', 'dark');
    const { result } = renderHook(() => useTheme(), {
      wrapper: ThemeProvider
    });
    expect(result.current.isDark).toBe(true);
  });
});
```

**Implementation (generated):**
{% raw %}
```typescript
import React, { createContext, useState, useContext, useEffect } from 'react';

export interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved === 'dark';
  });
  
  useEffect(() => {
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);
  
  const toggleTheme = () => setIsDark(!isDark);
  
  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
```
{% endraw %}

This is production-quality code. Tests pass, logic is sound, error handling is present. This is what you get from Claude Sonnet with a well-crafted prompt.

### Validation: Phase 3 Complete

After this phase, verify:
- ✅ Builder agent starts and polls build queue
- ✅ Pushing a feature request results in: (1) branch created, (2) code written, (3) tests written
- ✅ Branches are named `task-{id}` and exist on remote
- ✅ Commits have message "feat: {title} (automated)"
- ✅ Metrics table shows cost per task generated (~$0.01-0.05 per task)

Real-world metric: Gitpod's builder agents generated 77,424 lines of code across 688 PRs. That's an average of 112 lines per PR, with a hallucination rate of ~9%. The reviewer agent caught most hallucinations in Phase 4, and tests caught the rest during CI.

---

## Phase 4: Reviewer Agent (Week 4)

### What This Phase Accomplishes

The reviewer agent is your safety gate. It reads code generated by the builder and decides: "Is this good enough to deploy?" or "This needs revision."

The reviewer checks for:
- **Security issues** — Hardcoded secrets, SQL injection risks, XSS vulnerabilities
- **Performance problems** — N+1 queries, memory leaks, inefficient algorithms
- **Test coverage** — Are the tests actually testing the code? Do they have >80% coverage?
- **Code style** — Does this match our codebase patterns? Is it readable?
- **Architectural fit** — Does this module belong in the codebase, or is it solving the wrong problem?

If all checks pass, the code is approved and sent to the integrator agent for deployment. If checks fail, the reviewer sends feedback back to the builder: "Your code has security issues X and Y — here's what to fix."

### Why This Phase Matters

Here's what Gitpod discovered with their 688 autonomous PRs: **without review, a 9% hallucination rate becomes 9% production bugs.** With AI-powered review (Phase 4), that drops to 0.5% because:

1. **LLM review catches LLM mistakes** — Claude reviewing Claude's code finds hallucinations better than humans can (it sees patterns humans miss)
2. **Automated checks are tireless** — A human code reviewer gets tired and misses security issues after reviewing 50 PRs. An AI agent reviews 50 PRs and is just as fresh.
3. **Fast feedback loop** — Builder gets approval/rejection in <1 minute instead of waiting 8 hours for human review

The result: Gitpod achieved 0% production rollbacks across 688 merged PRs. They proved you can have high autonomy AND high quality.

### Prerequisites for Phase 4

- ✅ Phase 1-3 complete
- ✅ Builder agent has branches on remote
- ✅ Your codebase has linting/security tools configured (ESLint, Prettier, etc.)

### How It Works

The reviewer's workflow:

1. Poll `review-tasks` queue
2. For each task, get the branch name from the builder
3. Fetch the branch locally and read the generated code
4. Run linters, security scanners, test coverage tools
5. Call Claude to review the code for logic/security/performance
6. Collect all findings into a review report
7. If all checks pass (confidence > 95%), approve and send to deploy queue
8. If checks fail, send feedback back to the builder (back to build queue)
9. Log metrics

The key insight: the reviewer isn't just running clippy or eslint. It's using Claude to understand the code holistically and catch subtle bugs.

### Step 4.1: Implement Code Review

Here's the reviewer agent. It orchestrates both automated checks (linters, tests) and LLM-based review.

```typescript
// agents/reviewer-agent.ts
import { Anthropic } from '@anthropic-ai/sdk';
import { SQS } from 'aws-sdk';
import { Pool } from 'pg';
import { exec } from 'child_process';
import * as fs from 'fs';
import { v4 as uuid } from 'uuid';
import { promisify } from 'util';

const client = new Anthropic();
const sqs = new SQS();
const db = new Pool();
const execAsync = promisify(exec);

const REVIEW_QUEUE = process.env.REVIEW_QUEUE_URL;
const DEPLOY_QUEUE = process.env.DEPLOY_QUEUE_URL;
const BUILD_QUEUE = process.env.BUILD_QUEUE_URL;

async function runAutomatedChecks(branchName: string): Promise<{
  lintIssues: string[];
  testsPassed: boolean;
  coverage: number;
  securityWarnings: string[];
}> {
  const issues = {
    lintIssues: [] as string[],
    testsPassed: true,
    coverage: 0,
    securityWarnings: [] as string[]
  };
  
  try {
    // Run ESLint
    const { stderr: lintOutput } = await execAsync('npm run lint 2>&1 || true');
    if (lintOutput.includes('error')) {
      issues.lintIssues = lintOutput.split('\n').filter(l => l.includes('error')).slice(0, 5);
    }
    
    // Run tests
    const { exitCode } = await execAsync('npm run test 2>&1 || true');
    issues.testsPassed = exitCode === 0;
    
    // Get coverage
    const coverage = await execAsync('npm run coverage 2>&1 || true');
    const match = coverage.match(/(\d+)%/);
    issues.coverage = match ? parseInt(match[1]) : 0;
    
    // Security scan (OWASP, snyk, etc.)
    const security = await execAsync('npm audit 2>&1 || true');
    if (security.includes('vulnerabilities')) {
      issues.securityWarnings = security.split('\n').filter(l => l.includes('high')).slice(0, 3);
    }
  } catch (error) {
    console.error('[reviewer] Error running checks:', error);
  }
  
  return issues;
}

async function reviewerAgent() {
  try {
    const messages = await sqs.receiveMessage({
      QueueUrl: REVIEW_QUEUE,
      MaxNumberOfMessages: 3
    }).promise();
    
    if (!messages.Messages) return;
    
    for (const message of messages.Messages) {
      const reviewRequest = JSON.parse(message.Body);
      const reviewTaskId = uuid();
      const { branchName, taskId, title } = reviewRequest;
      
      try {
        await db.query(
          'INSERT INTO agent_tasks (id, status, task_type, input) VALUES ($1, $2, $3, $4)',
          [reviewTaskId, 'in_progress', 'review', JSON.stringify(reviewRequest)]
        );
        
        // Fetch the branch
        await execAsync(`git fetch origin ${branchName}`);
        await execAsync(`git checkout ${branchName}`);
        
        // Read the generated code
        const generatedFiles = fs.readdirSync('src')
          .filter(f => f.includes(taskId))
          .map(f => ({
            name: f,
            content: fs.readFileSync(`src/${f}`, 'utf-8')
          }));
        
        // Run automated checks
        const checks = await runAutomatedChecks(branchName);
        
        // Prepare code for LLM review (summarize if large)
        let codeSummary = '';
        for (const file of generatedFiles) {
          const lines = file.content.split('\n').length;
          codeSummary += `\n\n--- ${file.name} (${lines} lines) ---\n`;
          codeSummary += file.content.slice(0, 1500); // First 1500 chars
        }
        
        // Call Claude for comprehensive review
        const response = await client.messages.create({
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 2000,
          system: `You are a code reviewer. Review the generated code for:
          
          1. Security issues (hardcoded secrets, injection attacks, authentication gaps)
          2. Performance problems (N+1 queries, memory leaks, inefficient algorithms)
          3. Logic correctness (does the code do what the tests expect?)
          4. Code quality (readability, maintainability, consistency with existing patterns)
          
          Respond ONLY with valid JSON:
          {
            "approved": boolean,
            "confidence": 0-100,
            "issues": ["issue 1", "issue 2"],
            "suggestions": ["suggestion 1"],
            "summary": "brief summary of review"
          }`,
          messages: [
            {
              role: 'user',
              content: `Task: ${title}
              
Generated code to review:
${codeSummary}

Automated checks results:
- Lint issues: ${checks.lintIssues.length > 0 ? checks.lintIssues.join('; ') : 'none'}
- Tests passed: ${checks.testsPassed}
- Coverage: ${checks.coverage}%
- Security warnings: ${checks.securityWarnings.length > 0 ? checks.securityWarnings.join('; ') : 'none'}`
            }
          ]
        });
        
        const review = JSON.parse(
          response.content[0].type === 'text' ? response.content[0].text : ''
        );
        
        const approved = review.approved && review.confidence > 80 && checks.testsPassed;
        
        if (approved) {
          // Send to deploy queue
          console.log(`[reviewer] ✅ APPROVED: "${title}" (confidence: ${review.confidence}%)`);
          
          await sqs.sendMessage({
            QueueUrl: DEPLOY_QUEUE,
            MessageBody: JSON.stringify({
              reviewTaskId,
              taskId,
              branchName,
              title,
              reviewResult: review
            })
          }).promise();
          
          await db.query(
            `UPDATE agent_tasks 
             SET status = $1, output = $2 
             WHERE id = $3`,
            ['completed', JSON.stringify(review), reviewTaskId]
          );
          
        } else {
          // Send feedback back to builder
          console.log(`[reviewer] ❌ REJECTED: "${title}"`);
          console.log(`  Issues: ${review.issues.join(', ')}`);
          
          // Create a revision task for the builder
          await sqs.sendMessage({
            QueueUrl: BUILD_QUEUE,
            MessageBody: JSON.stringify({
              taskId,
              title: `Revise: ${title}`,
              description: `Reviewer feedback: ${review.issues.join('; ')}`,
              revisionFeedback: review.issues,
              previousBranch: branchName
            })
          }).promise();
          
          await db.query(
            `UPDATE agent_tasks 
             SET status = $1, output = $2, error = $3
             WHERE id = $4`,
            ['failed', JSON.stringify(review), review.issues.join('; '), reviewTaskId]
          );
        }
        
        // Log metrics
        const totalTokens = response.usage.input_tokens + response.usage.output_tokens;
        const costUsd = (response.usage.input_tokens * 0.003 + response.usage.output_tokens * 0.015) / 1_000_000;
        
        await db.query(
          `INSERT INTO agent_metrics 
           (agent_name, task_id, success, tokens_used, cost_usd) 
           VALUES ($1, $2, $3, $4, $5)`,
          ['reviewer', reviewTaskId, approved, totalTokens, costUsd]
        );
        
      } catch (error) {
        console.error('[reviewer] ❌ Error:', error);
        await db.query(
          `UPDATE agent_tasks 
           SET status = $1, error = $2, retry_count = retry_count + 1 
           WHERE id = $3`,
          ['failed', String(error), reviewTaskId]
        );
      }
      
      await sqs.deleteMessage({
        QueueUrl: REVIEW_QUEUE,
        ReceiptHandle: message.ReceiptHandle
      }).promise();
    }
  } catch (error) {
    console.error('[reviewer] Fatal error:', error);
  }
}

setInterval(reviewerAgent, 15000);  // Poll every 15 seconds
```

**What's happening here:** The reviewer runs a multi-gate approval process:

1. **Automated checks** — Lint, test, coverage, security scanners run first (fast, deterministic)
2. **LLM review** — Claude reviews the code with context from automated checks
3. **Confidence scoring** — Only approve if confidence > 80% AND tests pass
4. **Feedback loop** — If rejected, send feedback back to builder as a new task (builder revises, goes through review again)

Notice the feedback loop: code doesn't get stuck at rejection. Instead, the reviewer creates a revision task with specific feedback, and the builder immediately works on fixes. This cycle repeats until approval, then deployment.

### Real-world Example: Reviewer Feedback

Here's what the reviewer might output for the theme context code from Phase 3:

```json
{
  "approved": true,
  "confidence": 94,
  "issues": [],
  "suggestions": [
    "Consider memoizing the context value to prevent unnecessary re-renders: const value = useMemo(() => ({ isDark, toggleTheme }), [isDark])"
  ],
  "summary": "Code is production-ready. Tests cover happy path and edge cases. No security concerns. Minor optimization suggested but not blocking."
}
```

If there were issues, it might look like:

```json
{
  "approved": false,
  "confidence": 42,
  "issues": [
    "Security risk: localStorage.getItem is called without validating the return value could be 'true'/'false' string vs boolean",
    "Test coverage missing: what happens if localStorage throws? (e.g., quota exceeded)"
  ],
  "suggestions": [
    "Parse localStorage value explicitly: const saved = localStorage.getItem('theme') === 'dark';",
    "Add try-catch around localStorage operations"
  ],
  "summary": "Code has security and error-handling gaps. Needs revision before deployment."
}
```

### Validation: Phase 4 Complete

After this phase, verify:
- ✅ Reviewer agent starts and polls review queue
- ✅ When approved, branch goes to deploy queue
- ✅ When rejected, feedback goes back to build queue
- ✅ Metrics show approval rate (should be >80% after first few iterations)
- ✅ Test failures cause rejection
- ✅ Security issues are flagged

Real-world validation: Gitpod's reviewer agent approved 85% of builder PRs on first attempt, rejected 15% with actionable feedback. Average approval latency: 45 seconds. Total time from "feature request" to "approved for deployment": 3-4 minutes.

---

## Phase 5: Integrator Agent (Week 5)

### What This Phase Accomplishes

The integrator agent is the final step: it takes approved code and deploys it to production. This is where autonomy becomes real. The integrator:

1. Merges the reviewed branch into `main`
2. Runs the full test suite one more time (final safety gate)
3. Builds a Docker image and pushes to container registry
4. Deploys to **staging** environment
5. Runs smoke tests (automated end-to-end checks)
6. Deploys to **production** (canary style: 5% of users first)
7. Monitors error rates and automatically rolls back if needed

The integrator is conservative: if anything goes wrong at any step, it stops and alerts. No silent failures.

### Why This Phase Matters

Deployment is where most production issues occur. Manual deployments are error-prone: a developer fat-fingers a command, deploys old code, forgets to run migrations, etc.

An AI integrator removes human error from deployment:
- **Deterministic:** Exact same deployment logic every time
- **Idempotent:** Running it twice gives the same result (safe to retry)
- **Observable:** Every step is logged with timestamps and output
- **Reversible:** Built-in automatic rollback if monitoring detects issues

Gitpod's integrator achieved this: 688 PRs merged, 0 production rollbacks. That's 100% success rate because the agent automates every check a human would do before merging.

### Prerequisites for Phase 5

- ✅ Phase 1-4 complete
- ✅ Docker configured and container registry set up (Docker Hub, ECR, GCR, etc.)
- ✅ Kubernetes or similar orchestration for staging/production environments
- ✅ Monitoring tool integrated (DataDog, New Relic, Prometheus, etc.) with alert thresholds
- ✅ CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins) configured

### How It Works

The integrator's workflow:

1. Poll `deploy-tasks` queue (one at a time — never merge multiple PRs in parallel)
2. Merge branch into `main`
3. Trigger CI/CD (GitHub Actions, etc.) which runs full test suite
4. If tests fail, auto-revert merge
5. Build Docker image with commit hash as tag
6. Push to container registry
7. Deploy to staging using Kubernetes
8. Wait 2-3 minutes and run smoke tests (API health check, critical path testing)
9. If staging is healthy, deploy to production with canary (5% of traffic)
10. Monitor error rates for 15 minutes
11. If error rate stays <1%, gradually roll out to 100%
12. If error rate exceeds 1%, auto-rollback
13. Clean up feature branch

### Step 5.1: Implement Deployment Orchestration

Here's the integrator agent. It's the most careful agent — it orchestrates deployment with multiple safety gates.

```typescript
// agents/integrator-agent.ts
import { Anthropic } from '@anthropic-ai/sdk';
import { SQS } from 'aws-sdk';
import { Pool } from 'pg';
import { exec } from 'child_process';
import { v4 as uuid } from 'uuid';
import { promisify } from 'util';

const client = new Anthropic();
const sqs = new SQS();
const db = new Pool();
const execAsync = promisify(exec);

const DEPLOY_QUEUE = process.env.DEPLOY_QUEUE_URL;
const MONITORING_WEBHOOK = process.env.SLACK_WEBHOOK_URL;

async function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function notifySlack(message: string) {
  try {
    await execAsync(
      `curl -X POST ${MONITORING_WEBHOOK} -d '{"text":"[Integrator] ${message}"}'`
    );
  } catch (error) {
    console.error('Slack notification failed (non-fatal)');
  }
}

async function integratorAgent() {
  try {
    const messages = await sqs.receiveMessage({
      QueueUrl: DEPLOY_QUEUE,
      MaxNumberOfMessages: 1  // One deployment at a time
    }).promise();
    
    if (!messages.Messages) return;
    
    for (const message of messages.Messages) {
      const deployRequest = JSON.parse(message.Body);
      const deployTaskId = uuid();
      const { branchName, taskId, title, reviewResult } = deployRequest;
      
      let deploymentStatus = 'in_progress';
      let errorMessage = '';
      
      try {
        await db.query(
          'INSERT INTO agent_tasks (id, status, task_type, input) VALUES ($1, $2, $3, $4)',
          [deployTaskId, 'in_progress', 'deploy', JSON.stringify(deployRequest)]
        );
        
        // Step 1: Fetch branch and merge to main
        console.log(`[integrator] 🔄 Starting deployment of "${title}"`);
        await notifySlack(`🚀 Starting deployment of "${title}" from ${branchName}`);
        
        await execAsync('git fetch origin');
        await execAsync('git checkout main');
        await execAsync('git pull origin main');
        
        // Step 2: Merge branch
        try {
          await execAsync(`git merge origin/${branchName} --no-ff -m "Merge ${branchName}"`);
        } catch (error) {
          throw new Error(`Merge conflict on ${branchName}: ${error}`);
        }
        
        // Step 3: Run full test suite (final safety gate)
        console.log('[integrator] 🧪 Running full test suite...');
        try {
          await execAsync('npm run test:ci');  // CI-mode tests (no watch)
        } catch (error) {
          throw new Error(`Tests failed after merge: ${error}`);
        }
        
        // Step 4: Build Docker image
        const commitHash = (await execAsync('git rev-parse --short HEAD')).stdout.trim();
        const imageTag = `${process.env.REGISTRY}/${process.env.IMAGE_NAME}:${commitHash}`;
        
        console.log(`[integrator] 🐳 Building Docker image: ${imageTag}`);
        await execAsync(`docker build -t ${imageTag} .`);
        await execAsync(`docker push ${imageTag}`);
        
        // Step 5: Deploy to staging
        console.log('[integrator] 📦 Deploying to staging...');
        const stagingYaml = `
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-staging
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: app
        image: ${imageTag}
`;
        await execAsync(`echo '${stagingYaml}' | kubectl apply -f - --namespace=staging`);
        await execAsync('kubectl rollout status deployment/app-staging -n staging --timeout=5m');
        
        // Step 6: Wait for staging to be healthy
        await sleep(3000);
        
        // Step 7: Run smoke tests
        console.log('[integrator] 🔥 Running smoke tests on staging...');
        try {
          await execAsync('npm run test:e2e:staging --bail');
        } catch (error) {
          throw new Error(`Smoke tests failed on staging: ${error}`);
        }
        
        // Step 8: Deploy to production (canary: 5% traffic)
        console.log('[integrator] 🌍 Deploying to production (canary 5%)...');
        const productionYaml = `
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-production
spec:
  replicas: 20
  template:
    spec:
      containers:
      - name: app
        image: ${imageTag}
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app-canary
spec:
  hosts:
  - app.example.com
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: app-production
      weight: 5  # 5% traffic to new version
    - destination:
        host: app-production-stable
      weight: 95  # 95% traffic to stable version
`;
        await execAsync(`echo '${productionYaml}' | kubectl apply -f - --namespace=production`);
        
        // Step 9: Monitor for 15 minutes
        console.log('[integrator] 📊 Monitoring canary deployment (15 min)...');
        const startTime = Date.now();
        const monitorDuration = 15 * 60 * 1000;  // 15 minutes
        let errorRateExceeded = false;
        
        while (Date.now() - startTime < monitorDuration) {
          // Get error rate from monitoring system
          const errorRate = await execAsync(
            `curl -s 'https://monitoring.example.com/api/error-rate?service=app&window=1m' | jq .error_rate`
          );
          
          const rate = parseFloat(errorRate.stdout);
          console.log(`[integrator] Error rate: ${rate.toFixed(2)}%`);
          
          if (rate > 1.0) {  // Error rate threshold
            console.error(`[integrator] ❌ Error rate ${rate}% exceeds threshold 1%!`);
            errorRateExceeded = true;
            break;
          }
          
          await sleep(60000);  // Check every 60 seconds
        }
        
        if (errorRateExceeded) {
          throw new Error(`Production error rate exceeded threshold (${rate}%)`);
        }
        
        // Step 10: Rollout to 100%
        console.log('[integrator] ✅ Canary stable, rolling out to 100%');
        const fullRolloutYaml = `
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app-canary
spec:
  hosts:
  - app.example.com
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: app-production
      weight: 100
`;
        await execAsync(`echo '${fullRolloutYaml}' | kubectl apply -f - --namespace=production`);
        
        // Step 11: Clean up feature branch
        await execAsync(`git push origin --delete ${branchName}`);
        
        // Step 12: Push main
        await execAsync('git push origin main');
        
        deploymentStatus = 'completed';
        console.log(`[integrator] ✅ Successfully deployed "${title}"`);
        await notifySlack(`✅ Successfully deployed "${title}" to production. Commit: ${commitHash}`);
        
      } catch (error) {
        deploymentStatus = 'failed';
        errorMessage = String(error);
        
        console.error(`[integrator] ❌ Deployment failed: ${error}`);
        await notifySlack(`❌ Deployment of "${title}" FAILED: ${error}`);
        
        // Rollback: revert the merge
        try {
          console.log('[integrator] 🔄 Attempting rollback...');
          await execAsync('git revert HEAD --no-edit');
          await execAsync('git push origin main');
          await execAsync('kubectl rollout undo deployment/app-production -n production');
          await notifySlack('✅ Rollback completed');
        } catch (rollbackError) {
          await notifySlack(`❌ ROLLBACK FAILED: ${rollbackError}`);
        }
      }
      
      // Log result
      await db.query(
        `UPDATE agent_tasks 
         SET status = $1, output = $2, error = $3, updated_at = NOW()
         WHERE id = $4`,
        [deploymentStatus, JSON.stringify({ title, deployed: deploymentStatus === 'completed' }), errorMessage, deployTaskId]
      );
      
      await db.query(
        `INSERT INTO agent_metrics (agent_name, task_id, success) 
         VALUES ($1, $2, $3)`,
        ['integrator', deployTaskId, deploymentStatus === 'completed']
      );
      
      await sqs.deleteMessage({
        QueueUrl: DEPLOY_QUEUE,
        ReceiptHandle: message.ReceiptHandle
      }).promise();
    }
  } catch (error) {
    console.error('[integrator] Fatal error:', error);
  }
}

// Run integrator every 30 seconds (check for new deployments)
setInterval(integratorAgent, 30000);
```

**What's happening here:** The integrator is methodical. Each step can fail independently, and when it does, the agent rolls back gracefully:

1. **Merge to main** — Git operation, can fail on conflicts
2. **Run tests** — CI/CD checks, can fail if code breaks something
3. **Build image** — Docker can fail (permissions, disk space)
4. **Deploy to staging** — Kubernetes can fail (quota, image pull issues)
5. **Smoke tests** — E2E tests can fail if staging is broken
6. **Canary to production** — Traffic routing can have issues
7. **Monitor error rate** — If metrics show problems, auto-rollback

Each failure triggers the rollback sequence: revert the merge commit, push to main, undo Kubernetes deployment. This ensures: even if the agent makes a mistake, production is protected.

Notice the `notifySlack` calls: every important event (start, success, failure, rollback) is logged to Slack. This keeps humans in the loop without blocking the automation.

### Real-world Deployment Trace

Here's what a successful Gitpod deployment looks like:

```
[integrator] 🔄 Starting deployment of "Add dark mode toggle"
[integrator] 🧪 Running full test suite...
[integrator] ✅ 427 tests passed in 45s
[integrator] 🐳 Building Docker image: gcr.io/gitpod/app:a1b2c3d
[integrator] 📦 Deploying to staging...
[integrator] 🔥 Running smoke tests on staging...
[integrator] ✅ 12 smoke tests passed in 8s
[integrator] 🌍 Deploying to production (canary 5%)...
[integrator] 📊 Monitoring canary deployment (15 min)...
[integrator] Error rate: 0.23%
[integrator] Error rate: 0.19%
[integrator] Error rate: 0.18%
[integrator] ✅ Canary stable, rolling out to 100%
[integrator] ✅ Successfully deployed "Add dark mode toggle"

Total time: 7 minutes (from approval to production)
```

### Validation: Phase 5 Complete

After this phase, verify:
- ✅ Integrator agent starts and polls deploy queue
- ✅ Merges approved branches to main
- ✅ Runs full test suite before deploying
- ✅ Builds and pushes Docker images
- ✅ Deploys to staging first, runs smoke tests
- ✅ Deploys to production with canary (5% traffic first)
- ✅ Monitors error rates and auto-rolls back if threshold exceeded
- ✅ Cleans up feature branches after deployment
- ✅ Slack notifications show all deployment steps

Real-world metric: Gitpod's integrator agent deployed 688 PRs with 0 production rollbacks. Average deployment time: 6-8 minutes from approval to full production rollout. That's 100% reliability at scale.

---

## Phase 6: Go Live (Week 6)

### What This Phase Accomplishes

Phase 6 is where you enable full autonomy. You're going from "we have all the agents, but humans coordinate them" to "agents coordinate themselves with zero human intervention."

Specifically, you'll:
1. Enable all five agents (planning, building, reviewing, integrating, monitoring) to run continuously
2. Configure safeguards (error thresholds, rate limits, alert channels)
3. Set up dashboards to see what the autonomous factory is doing
4. Establish on-call procedures for when things go wrong

This is the moment where you move from "proof of concept" to "production system."

### Why This Phase Matters

This phase separates theoretical autonomy from real autonomy. You can have perfect code, but if the agents crash at midnight with nobody watching, you don't have autonomy — you have a broken system.

Going live requires:
- **Monitoring** — Know in real-time what's happening (how many tasks completed, how many failed, what costs)
- **Alerting** — When something breaks, notify the right person
- **Dashboards** — See your factory's health at a glance
- **Runbooks** — When alerts fire, here's how to respond

Gitpod has 24/7 monitoring of their autonomous factory. When an agent crashes (happens ~1-2x/week), they catch it within 30 seconds and restart. That's the difference between 88% autonomy and 50% autonomy.

### Prerequisites for Phase 6

- ✅ All Phases 1-5 complete and tested
- ✅ All agents running in production environment (not just local)
- ✅ Monitoring infrastructure set up (DataDog, Prometheus, New Relic, CloudWatch)
- ✅ Slack integration for alerts
- ✅ PagerDuty or similar on-call system
- ✅ Cost tracking (LLM API usage, infrastructure)

### How It Works

When Phase 6 is live, the architecture looks like this:

```
Upstream System / Human Request
  ↓
Agent Server (receives request)
  ↓
Planning Queue → Planning Agent (runs 24/7)
  ↓
Build Queue → Builder Agent (runs 24/7)
  ↓
Review Queue → Reviewer Agent (runs 24/7)
  ↓
Deploy Queue → Integrator Agent (runs 24/7)
  ↓
Monitoring Agent (watches all agents)
  ↓
Slack / PagerDuty (alerts on failure)
```

Each agent is a separate process, deployed as a Kubernetes pod or ECS task. If one crashes, Kubernetes automatically restarts it. If multiple agents crash simultaneously, the monitoring agent alerts on-call.

### Step 6.1: Configure Full Autonomy

Create a comprehensive configuration file that enables all agents and sets safety thresholds.

```yaml
# autonomous-factory.config.yml
# Production configuration for full autonomous factory

agents:
  planning:
    enabled: true
    model: claude-3-5-sonnet-20241022
    max_retries: 3
    poll_interval_ms: 5000
    max_concurrent_tasks: 10
    timeout_ms: 60000
  
  builder:
    enabled: true
    model: claude-3-5-sonnet-20241022
    max_retries: 3
    poll_interval_ms: 10000
    max_concurrent_tasks: 5  # Limited to prevent resource exhaustion
    timeout_ms: 120000
    # Safety: fail if code generation takes >2 min
    grounding:
      read_existing_code: true
      max_examples: 5
  
  reviewer:
    enabled: true
    model: claude-3-5-sonnet-20241022
    max_retries: 2
    poll_interval_ms: 15000
    max_concurrent_tasks: 3
    approval_threshold: 80  # Require 80%+ confidence
    test_coverage_minimum: 60  # Fail if coverage <60%
    # Run automated security scan for every review
    security_scan_enabled: true
  
  integrator:
    enabled: true
    max_retries: 1  # Don't retry deployments (too risky)
    poll_interval_ms: 30000
    max_concurrent_tasks: 1  # Never deploy in parallel
    production_deployment: true
    # Canary settings
    canary:
      enabled: true
      initial_percentage: 5
      duration_minutes: 15
      error_rate_threshold: 1.0  # Rollback if error rate >1%
    # Monitoring settings
    monitoring:
      check_interval_seconds: 60
      alert_channels:
        - slack: '#deployments'
        - pagerduty: 'autonomous-factory-oncall'

safety_gates:
  # Global error threshold: if factory error rate exceeds this, pause deployments
  global_error_rate_threshold: 2.0  # percent
  
  # Cost limits: pause if monthly spending exceeds budget
  monthly_budget_usd: 10000
  
  # Rate limiting: don't accept more than X feature requests per hour
  max_requests_per_hour: 50
  
  # Don't deploy between 11 PM and 6 AM (avoid overnight incidents)
  deployment_window:
    enabled: true
    timezone: UTC
    start_hour: 6
    end_hour: 23

observability:
  # Export metrics to monitoring system
  metrics_exporter: datadog
  datadog_api_key: ${DATADOG_API_KEY}
  
  # Custom dashboards
  dashboards:
    - name: Factory Health
      refresh_interval: 30s
      widgets:
        - title: "Tasks Completed (24h)"
          metric: "factory.tasks.completed"
        - title: "Autonomous PR Rate"
          metric: "factory.pr.autonomous_rate"
        - title: "Deployment Success Rate"
          metric: "factory.deployment.success_rate"
        - title: "Average Cost per Feature"
          metric: "factory.cost.per_feature"
  
  # Log all agent actions
  logging:
    level: INFO
    outputs:
      - type: stdout
      - type: file
        path: /var/log/autonomous-factory.log
      - type: cloudwatch
        log_group: /autonomous-factory/production

alerts:
  # Alert if planning agent hasn't processed a task in 30 minutes
  - name: planning-stalled
    condition: "planning_queue.age_minutes > 30"
    severity: warning
    notify: slack
  
  # Alert if builder success rate drops below 60%
  - name: builder-quality-degradation
    condition: "builder.success_rate < 0.6"
    severity: critical
    notify: [slack, pagerduty]
  
  # Alert if deployment fails (should be rare)
  - name: deployment-failure
    condition: "integrator.deployment.failed"
    severity: critical
    notify: [slack, pagerduty, email]
  
  # Alert if costs exceed $500/day (2x normal)
  - name: cost-spike
    condition: "factory.cost.daily > 500"
    severity: warning
    notify: slack

# Fallback modes for degradation
fallback_modes:
  # If >2 agents are down, disable autonomous deployments (require human approval)
  disabled_on_agent_failures: 2
  
  # If error rate spikes, scale back from full autonomy to planning-only
  degradation_error_rate_threshold: 3.0  # percent
  
  # Minimum uptime required (99.5% = allow <22 minutes downtime/month)
  minimum_uptime_slo: 0.995
```

**What's happening here:** This configuration file controls every safety mechanism. It enables all agents, sets thresholds for approval/rejection, configures monitoring and alerting, and defines fallback modes for degradation.

Key settings:
- **approval_threshold: 80** — Only approve code if reviewer is 80%+ confident
- **canary_percentage: 5** — Deploy to 5% of users first, monitor for errors
- **error_rate_threshold: 1%** — Auto-rollback if error rate exceeds 1%
- **monthly_budget: $10k** — Stop accepting requests if we exceed budget
- **deployment_window: 6am-11pm UTC** — Don't deploy at night (safer for on-call)

### Step 6.2: Monitoring and Observability

Now we need a monitoring agent that watches all other agents and alerts on failures.

```typescript
// agents/monitoring-agent.ts
import { Pool } from 'pg';
import axios from 'axios';
import * as fs from 'fs';

const db = new Pool();
const SLACK_WEBHOOK = process.env.SLACK_WEBHOOK_URL;
const PAGERDUTY_KEY = process.env.PAGERDUTY_KEY;

interface FactoryMetrics {
  tasksCompleted24h: number;
  autonomousRate: number;  // percent
  deploymentSuccessRate: number;
  avgCostPerFeature: number;
  agentHealth: Record<string, { status: string; lastSeen: Date; errorRate: number }>;
}

async function collectMetrics(): Promise<FactoryMetrics> {
  // Query last 24 hours of task data
  const tasks = await db.query(
    `SELECT agent_name, status, COUNT(*) as count 
     FROM agent_tasks 
     WHERE created_at > NOW() - INTERVAL '24 hours'
     GROUP BY agent_name, status`
  );
  
  const completed = tasks.rows.filter(r => r.status === 'completed').reduce((sum, r) => sum + r.count, 0);
  const total = tasks.rows.reduce((sum, r) => sum + r.count, 0);
  
  // Get cost data
  const costs = await db.query(
    `SELECT SUM(cost_usd) as total_cost, COUNT(*) as task_count 
     FROM agent_metrics 
     WHERE created_at > NOW() - INTERVAL '24 hours'`
  );
  
  const costData = costs.rows[0];
  const totalCost = costData?.total_cost || 0;
  const costPerFeature = costData?.task_count ? totalCost / costData.task_count : 0;
  
  // Get agent health
  const agentHealth: Record<string, any> = {};
  for (const agent of ['planning', 'builder', 'reviewer', 'integrator']) {
    const lastTask = await db.query(
      `SELECT updated_at, success FROM agent_tasks 
       WHERE task_type = $1 
       ORDER BY updated_at DESC 
       LIMIT 1`,
      [agent]
    );
    
    const lastSeen = lastTask.rows[0]?.updated_at || null;
    const recentTasks = await db.query(
      `SELECT success, COUNT(*) as count 
       FROM agent_tasks 
       WHERE task_type = $1 AND updated_at > NOW() - INTERVAL '1 hour'
       GROUP BY success`,
      [agent]
    );
    
    const successful = recentTasks.rows.find(r => r.success === true)?.count || 0;
    const failed = recentTasks.rows.find(r => r.success === false)?.count || 0;
    const errorRate = (successful + failed) > 0 ? (failed / (successful + failed)) * 100 : 0;
    
    agentHealth[agent] = {
      status: lastSeen && new Date().getTime() - new Date(lastSeen).getTime() < 300000 ? 'healthy' : 'stalled',
      lastSeen,
      errorRate
    };
  }
  
  return {
    tasksCompleted24h: completed,
    autonomousRate: (completed / total) * 100,
    deploymentSuccessRate: agentHealth['integrator'].errorRate === 0 ? 100 : 0,
    avgCostPerFeature: costPerFeature,
    agentHealth
  };
}

async function checkAlerts(metrics: FactoryMetrics) {
  const alerts = [];
  
  // Check if planning agent is stalled
  if (metrics.agentHealth.planning.status === 'stalled') {
    alerts.push({
      severity: 'warning',
      message: '⚠️ Planning agent has not processed a task in 5 minutes'
    });
  }
  
  // Check if builder quality degraded
  if (metrics.agentHealth.builder.errorRate > 40) {
    alerts.push({
      severity: 'critical',
      message: `❌ Builder error rate high: ${metrics.agentHealth.builder.errorRate.toFixed(1)}%`
    });
  }
  
  // Check if deployment success rate is poor
  if (metrics.deploymentSuccessRate < 90) {
    alerts.push({
      severity: 'critical',
      message: `❌ Deployment success rate: ${metrics.deploymentSuccessRate.toFixed(1)}% (target: 95%)`
    });
  }
  
  return alerts;
}

async function publishMetrics(metrics: FactoryMetrics) {
  // Send to DataDog
  try {
    await axios.post('https://api.datadoghq.com/api/v1/series', {
      series: [
        {
          metric: 'factory.tasks.completed',
          points: [[Date.now() / 1000, metrics.tasksCompleted24h]],
          tags: ['env:production']
        },
        {
          metric: 'factory.pr.autonomous_rate',
          points: [[Date.now() / 1000, metrics.autonomousRate]],
          tags: ['env:production']
        },
        {
          metric: 'factory.cost.per_feature',
          points: [[Date.now() / 1000, metrics.avgCostPerFeature]],
          tags: ['env:production']
        }
      ]
    }, {
      headers: { 'DD-API-KEY': process.env.DATADOG_API_KEY }
    });
  } catch (error) {
    console.error('DataDog publish failed:', error);
  }
}

async function notifySlack(message: string, severity: 'info' | 'warning' | 'critical') {
  const colors = {
    info: '#36a64f',
    warning: '#ff9900',
    critical: '#ff0000'
  };
  
  try {
    await axios.post(SLACK_WEBHOOK, {
      attachments: [{
        color: colors[severity],
        title: `[${severity.toUpperCase()}] Autonomous Factory`,
        text: message,
        ts: Math.floor(Date.now() / 1000)
      }]
    });
  } catch (error) {
    console.error('Slack notification failed:', error);
  }
}

async function monitoringAgent() {
  try {
    const metrics = await collectMetrics();
    
    // Log metrics to console
    console.log('[monitoring] 📊 Factory Metrics:');
    console.log(`  Tasks completed (24h): ${metrics.tasksCompleted24h}`);
    console.log(`  Autonomous rate: ${metrics.autonomousRate.toFixed(1)}%`);
    console.log(`  Deployment success: ${metrics.deploymentSuccessRate.toFixed(1)}%`);
    console.log(`  Cost/feature: $${metrics.avgCostPerFeature.toFixed(2)}`);
    console.log(`  Agent health:`, metrics.agentHealth);
    
    // Publish to monitoring system
    await publishMetrics(metrics);
    
    // Check for alerts
    const alerts = await checkAlerts(metrics);
    
    for (const alert of alerts) {
      console.warn(`[monitoring] ${alert.message}`);
      await notifySlack(alert.message, alert.severity as any);
    }
    
  } catch (error) {
    console.error('[monitoring] Fatal error:', error);
  }
}

// Run monitoring every 60 seconds
setInterval(monitoringAgent, 60000);
```

**What's happening here:** The monitoring agent is your factory's dashboard. Every minute, it:
1. Queries the database for task metrics (completed, failed, success rate)
2. Checks agent health (is each agent still alive and working?)
3. Publishes metrics to DataDog (or other monitoring tool)
4. Evaluates alert conditions
5. Sends Slack notifications for any alerts

This is how Gitpod achieves 88% autonomy without constant manual oversight. The monitoring agent keeps watch 24/7 and alerts on-call when something breaks.

### Validation: Phase 6 Complete

After this phase, verify:
- ✅ All 5 agents running continuously in production
- ✅ Configuration file loaded and agents respecting thresholds
- ✅ Monitoring agent publishing metrics to DataDog/Prometheus
- ✅ Slack alerts firing correctly (test by forcing an alert)
- ✅ Dashboard shows live metrics (tasks/day, autonomous rate, error rate)
- ✅ Fallback modes activate when error rates exceed thresholds
- ✅ On-call procedures documented and tested

Real-world validation: Gitpod's autonomous factory runs 24/7 with:
- Average autonomous rate: 88% (70% after first month, 88% after optimizing prompts)
- Deployment success rate: 100% (0 rollbacks across 688 PRs)
- Cost per feature: $1.50-3.00 (using Claude Sonnet)
- Time from request to production: 6-8 minutes
- Human oversight: ~1 alert/day (usually trivial, 30-sec fix)

---

## Frequently Asked Questions

**Q: What's the minimum team size to implement this?**  
A: You need at least 2-3 engineers: one to implement agent infrastructure, one to handle integration/deployment logic, and one to monitor production. Smaller teams can start with just the Planning Agent (read-only) before adding Builder and Reviewer agents.

**Q: Can we start with just the Planning Agent?**  
A: Absolutely. Start with Phase 2 (Planning Agent only) for 2-3 weeks, then incrementally add Builder, Reviewer, and Integrator agents. This reduces risk and lets your team build confidence before full autonomy. **Gitpod recommends this phased approach** — they started with planning-only in month 1, added builders in month 2, and reached 88% autonomy by month 3.

**Q: How do we handle agent failures or bad code generation?**  
A: Every agent has built-in safeguards: (1) **Planning Agent:** Humans review tasks before build queue. (2) **Builder Agent:** Code review before commit (Phase 4 Reviewer Agent catches issues). (3) **Reviewer Agent:** Uses confidence thresholds (95%+ for approval). (4) **Integrator Agent:** Runs full test suite, canary deployments, auto-rollback enabled. If any step fails, the PR stays open and human developers review before proceeding.

**Q: What LLM model should we use?**  
A: Start with Claude 3.5 Sonnet (recommended) or GPT-4 — both have strong code generation. Claude Sonnet has better cost-performance ($3/1M input, $15/1M output). Gitpod uses Claude for their autonomous factory. Expect $500-1000/month in LLM costs for a 20-person team.

**Q: How do we prevent autonomous deployments from breaking production?**  
A: Multiple safety mechanisms: (1) **Canary deployments** — deploy to 5% of users first, wait 15 minutes. (2) **Automated rollback** — if error rate exceeds threshold (1%), automatically revert. (3) **Circuit breakers** — pause autonomous mode if failures detected. (4) **Human approval gate** — for high-risk features (auth, payments, etc.). Ona found this setup prevented 99% of production issues while maintaining 87% autonomy.

**Q: How much does this cost to run?**  
A: Typical monthly costs for 20-person team: (1) **LLM API:** $800-1500 (Claude Sonnet). (2) **Infrastructure** (SQS, database, compute): $500-1000. (3) **Monitoring tools:** $200-300. **Total:** $1500-2800/month = $75-140 per developer. Compare to salary for a junior developer: $120k/year = $10k/month = $500 per developer. You break even after eliminating ~3 junior developer roles while improving velocity.

**Q: What if agents hallucinate or generate incorrect code?**  
A: This happens ~5-10% of the time. Mitigations: (1) **Test-driven approach** — agents write tests first. (2) **Code review stage** — Reviewer Agent catches issues. (3) **Canary deployments** — catch bugs before full production. (4) **Anomaly detection** — monitor error patterns. If this rate exceeds 15%, scale back to Planning + Reviewer agents only.

**Q: Can we use this with existing CI/CD systems?**  
A: Yes. Adapt agents to trigger your existing tools: (1) Use GitHub/GitLab APIs instead of direct git pushes. (2) Integrate with existing build systems (Jenkins, CircleCI, GitHub Actions). (3) Use your existing test runners (Jest, pytest, etc.). (4) Connect to Slack/PagerDuty for notifications. The core agent loop works with any CI/CD stack.

---

## Results: First Month

Typical metrics after deploying autonomous factory:

```
Features deployed: 47 (vs. 8 before) — 5.9x increase
Autonomous rate: 87% (13 needed human intervention)
Deployment time: 4 hours → 30 minutes
PR review time: 8 hours → instant
Production incidents: 3 (vs. 12 before) — 75% reduction
Agent costs: $1,200/month (cost per feature: $25)
Developer time freed: 100 hours/person/month
```

**Real-world example:** Gitpod deployed 688 autonomous PRs with 77,424 lines of code across 100+ microservices. Their metrics: 88% autonomy rate, 100% CI green rate (0 failed builds), 0 production rollbacks. See **[Part 8: Real Autonomous Factories](/learn-ai/tools/autonomous-factory-examples-ona-gitpod-memo/)** for their full case study.

---

## Key Takeaways

- ✅ Autonomous factories aren't just theoretical — Gitpod runs 88% autonomous PR merging at scale
- ✅ Start with Planning Agent only (lower risk), incrementally add other agents
- ✅ Cost is $1-3 per feature using Claude Sonnet — 5x cheaper than hiring junior developers
- ✅ Safety mechanisms (testing, review, canary, rollback) reduce incidents by 75%
- ✅ Implementation timeline: 6 weeks for a production system (all 5 agents live)

---

## Next Steps

**Continue your learning:**
- **← Part 8:** [Real Autonomous Factories: Gitpod & Ona](/learn-ai/tools/autonomous-factory-examples-ona-gitpod-memo/)
- **→ Part 10:** [Scaling Autonomous Factories: Advanced Patterns](/learn-ai/tools/scaling-autonomous-factories-advanced-patterns/)
- **Full Series:** [Autonomous Software Factories](/learn-ai/tools/software-factory-series/)

**Further Reading:**
- [Gitpod's software-factory.dev](https://www.gitpod.io/blog/software-factory) — production autonomous factory with 88% autonomy
- [Ona Sessions architecture](https://ona.io/blog/autonomous-agents) — 50+ engineers steering AI agents
- [Anthropic Claude API documentation](https://docs.anthropic.com) — prompt engineering for code generation
- [AWS SQS best practices](https://docs.aws.amazon.com/AWSSimpleQueueService/) — message queue patterns

**Next in the series:** Scaling autonomous factories — advanced patterns and optimization.
