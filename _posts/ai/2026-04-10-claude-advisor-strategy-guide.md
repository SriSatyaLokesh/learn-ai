---
layout: post
title: "How to Build Cost-Effective AI Agents with Claude's Advisor Strategy"
date: 2026-04-10
category: ai
tags: [claude-api, agentic-patterns, cost-optimization, ai-agents, advisor-strategy]
excerpt: "Master the Advisor Strategy pattern: pair Claude Opus with Sonnet for intelligent cost reduction without sacrificing agent performance. Complete implementation guide with benchmarks."
description: "Learn Claude's Advisor Strategy: pair Opus advisor with Sonnet executor to reduce agent costs by 11.9% while improving performance by 2.7%. Includes code examples and real-world case studies."
difficulty: intermediate
image: https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69d7a8216b96ea826922fcf4_e9f8286d.png
header:
  credit: "Anthropic/Claude.com"
  credit_url: "https://claude.com/blog/the-advisor-strategy"
author: satya-k
seo:
  primary_keyword: "Claude Advisory Strategy"
  secondary_keywords: [Advisory tool, claude code advisory,]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/claude-advisor-strategy-guide/"
---

## Introduction

Building effective AI agents requires balancing two competing demands: intelligence and cost. For months, teams building production agents faced a hard choice: deploy Claude 3.5 Sonnet for reasonable performance at moderate cost, or pay premium prices for Claude 3 Opus and enjoy superior reasoning at the expense of your token budget.

Claude's new Advisor Strategy changes this equation. By pairing Opus (advisor) with Sonnet/Haiku (executor) in an intelligent two-tier system, you get 2.7% performance improvement on complex engineering tasks while reducing costs by 11.9% compared to Sonnet alone ([Anthropic, 2026](https://claude.com/blog/the-advisor-strategy)).

This guide walks you through the complete strategy: the pattern itself, implementation details, real-world case studies from Eve Legal and Bolt, and practical guidance on when to use advisor configurations for your own agents.

> **TL;DR:** The Advisor Strategy pairs a fast, cheaper model (executor) for routine work with an expert model (Opus advisor) for tough decisions. It cuts costs by 11.9% while improving reasoning by 2.7% on complex tasks, using the new `advisor_20260301` tool in the Anthropic API. Best for multi-step agents where decisions vary in difficulty.

---

## What Is the Advisor Strategy and Why It Matters

### Traditional Agent Patterns

For the past year, teams building autonomous agents made a simple architectural choice: which Claude model handles the entire workflow?

```
User Input → Single Model (Opus OR Sonnet) → Output
```

Each approach had tradeoffs:

- **Sonnet everywhere:** Fast, cost-effective ($1.50 per million input tokens), but struggles with complex reasoning and multi-step planning
- **Opus everywhere:** Superior reasoning across all tasks, but expensive ($15/million input tokens — 10x Sonnet's cost) and unnecessarily powerful for routine decisions
- **Routing logic:** Some teams built sophisticated routers to switch models based on query complexity, but this added architectural complexity and still required defining what "complex" means

The core insight behind the Advisor Strategy is that agent work isn't uniform. Most decisions in a multi-step workflow are straightforward; only a few require sophisticated reasoning.

### How the Advisor Strategy Works

The new pattern is elegant: let the fast executor handle 90% of the work, and escalate only the decisions it can't confidently solve.

```
User Input → Executor (Sonnet/Haiku)
              ├─ Makes routine decision → Output
              └─ Unsure? Calls Advisor (Opus)
                        ├─ Complex reasoning
                        └─ Returns guidance → Executor proceeds
```

According to Anthropic's benchmarking on SWE-bench (a standard for evaluating AI software engineers), this pattern achieved ([Anthropic, 2026](https://claude.com/blog/the-advisor-strategy)):
- **2.7% improvement** in task success rate vs. Sonnet alone
- **11.9% cost reduction** compared to running Sonnet end-to-end
- **Same latency profile** as Sonnet, since Opus is called infrequently

The reason this works: about 80-90% of agent decisions happen in the "easy" category (following established patterns, applying rules, extracting data). Executor models handle these well. The remaining 10-20% involve novel combinations, architectural decisions, or reasoning about edge cases—where Opus excels and more than pays for itself through better decisions and fewer retries.

---

## The Cost vs. Quality Tradeoff Explained

### Why Model Costs Don't Scale Linearly

One misconception about the Advisor Strategy: people assume a two-model system must cost more than using a single model. In practice, the opposite happens.

When you use Sonnet alone for all tasks, you're paying `full_task_cost = sonnet_cost × all_work`. Some of this work is genuinely difficult (where Sonnet might fail or require multiple retries), but you still pay full price.

When you use the Advisor Strategy, you pay:
```
advisor_cost = (executor_cost × routing_work) + (opus_cost × hard_decisions)
```

The key: `hard_decisions` (calls to Opus) are typically **2-5% of total tokens** in well-designed agents, not 100%.

### Real Cost Numbers

Let me break down actual economics on a typical agentic workflow (document analysis task):

**Scenario 1: Sonnet Only**
```
Average task: 50,000 input tokens (context + history)
- Sonnet processing: 50,000 × $1.50/M = $0.075
- Multiple task failures/retries: 30% retry rate × $0.075 = $0.025 extra
- Total per task: $0.10
- 1,000 tasks per day: $100 cost
```

**Scenario 2: Advisor Strategy (Executor Sonnet + Advisor Opus)**
```
Average task: 50,000 tokens total
- Executor routing: 48,000 tokens (96% of work) × $1.50/M = $0.072
- Advisor calls: 2,000 tokens (4% escalations) × $15.00/M = $0.030
- Improved decision quality: 5% fewer retries vs. Sonnet alone
- Total per task: $0.102 - (5% retry savings) ≈ $0.097
- 1,000 tasks per day: $97 cost
- **Monthly savings: $90** (for a small operation) — **$3,000 for larger teams**
```

This is why Anthropic saw 11.9% cost reduction in benchmarks: not from using Sonnet 100% of the time, but from the compound effect of (a) lower costs on routine work + (b) dramatically better decisions on hard work + (c) fewer failures overall.

### Decision Quality Over Token Count

The other advantage: better decisions often prevent expensive failures downstream. Eve Legal (case study below) found that routing complex document interpretation to Opus prevented extraction errors that would have required manual review and correction—a cost that dwarfs advisor API calls.

---

## How the Advisor Pattern Actually Works: The Flow

### The Executor's Decision Points

When an executor encounters a decision, it has two choices:

1. **Solve it directly** — Use its own reasoning to make a decision and proceed
2. **Escalate to advisor** — Call Opus for guidance, then continue

The executor doesn't need heuristics to decide; the new `advisor_20260301` tool handles this. The executor literally calls a tool named "advisor" when uncertain:

```
Executor reasoning:
"I see a document with mixed formatting. The field extraction rules 
are ambiguous. This requires judgment about what the author intended. 
I don't have enough confidence. Let me call the advisor."

→ Opus receives: (context + the specific decision point)
→ Opus reasons: "Given X document style, field Y should map to..."
→ Executor receives guidance + proceeds
```

From the executor's perspective, the advisor is just another tool in its toolkit, like `extract_text` or `check_database`. But it's an intelligent tool that can reason.

### Token Usage and Billing

This is important for cost modeling: **split token billing** means:

- **Executor input tokens** (all context passed to executor): Charged at Sonnet rate ($1.50/M)
- **Advisor input tokens** (only the escalated context): Charged at Opus rate ($15/M)
- **Output tokens from both**: Charged at the respective model's rate

So if your executor sees a 50K context window but only passes 2K of relevant context to the advisor, you pay Sonnet rates for 50K and Opus rates for only the 2K.

---

## The Advisor Tool API: Implementation Details

### The `advisor_20260301` Tool

Claude's new tool for this pattern is called `advisor_20260301` (date-stamped for API versioning). Here's what you need to know:

**Tool Definition:**
```json
{
  "type": "tool",
  "name": "advisor_20260301",
  "description": "Request advice from Claude 3 Opus on a complex decision or reasoning task. Use when current reasoning is insufficient.",
  "input_schema": {
    "type": "object",
    "properties": {
      "question": {
        "type": "string",
        "description": "The specific question or decision you're uncertain about"
      },
      "context": {
        "type": "string",
        "description": "Relevant context for the advisor to consider"
      },
      "previous_attempts": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Previous approaches you've tried (optional)"
      }
    },
    "required": ["question", "context"]
  }
}
```

**Key characteristics:**

- Available for all Claude 3.5 Sonnet and Haiku instances
- Accessible via new `tools` parameter in the API (same as custom tools)
- Latency: ~500-1000ms median (Opus reasoning over focused context)
- Works with both streaming and non-streaming requests
- Tool calls are logged in `stop_reason: "tool_calls"` like any other tool use

---

## Implementation: Code Examples

### Example 1: Basic Executor with Advisor Tool Setup

This example shows the advisor tool definition:

```javascript
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Define the advisor tool
const tools = [
  {
    name: "advisor_20260301",
    description:
      "Request reasoning from Claude Opus for complex document decisions",
    input_schema: {
      type: "object",
      properties: {
        question: {
          type: "string",
          description: "The specific extraction or interpretation question",
        },
        context: {
          type: "string",
          description: "Document context relevant to the decision",
        },
      },
      required: ["question", "context"],
    },
  },
];

const systemPrompt = `You are a document analysis agent. Extract and structure data based on the rules provided.

When you encounter ambiguity in the document that makes you unsure about field interpretation,
use the advisor_20260301 tool to get guidance from an expert before proceeding.`;
```

**Key points:**
- The executor (Sonnet) processes documents
- When encountering ambiguous fields, it calls `advisor_20260301`
- The advisor (Opus) reasons about the ambiguity
- The executor uses the guidance to finalize extraction

### Example 1b: Processing Document with Advisor

Here's how the executor handles an ambiguous document:

```javascript
async function documentAnalyzer(document, extractionRules) {
  const messages = [];
  
  messages.push({
    role: "user",
    content: `Analyze this document and extract structured data.
    Use the advisor for any ambiguous field mappings.
    
    Document: ${document}`,
  });

  let response = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 2048,
    system: systemPrompt,
    tools: tools,
    messages: messages,
  });

  // Process tool calls (advisor invocations)
  while (response.stop_reason === "tool_calls") {
    const toolUses = response.content.filter((block) => block.type === "tool_use");
    messages.push({ role: "assistant", content: response.content });

    const toolResults = [];
    for (const toolUse of toolUses) {
      if (toolUse.name === "advisor_20260301") {
        const advisorResponse = await client.messages.create({
          model: "claude-3-opus-20250729",
          max_tokens: 1024,
          system: `Expert guidance: ${toolUse.input.question}\n\nContext: ${toolUse.input.context}`,
          messages: [{ role: "user", content: toolUse.input.question }],
        });
        
        toolResults.push({
          type: "tool_result",
          tool_use_id: toolUse.id,
          content: advisorResponse.content[0].text,
        });
      }
    }

    messages.push({ role: "user", content: toolResults });
    response = await client.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 2048,
      system: systemPrompt,
      tools: tools,
      messages: messages,
    });
  }

  return response.content
    .filter((block) => block.type === "text")
    .map((block) => block.text)
    .join("\n");
}
```

**Important:** The executor doesn't blindly call the advisor—it uses judgment about when guidance is needed, which is the core value of the pattern.

### Example 2: Building a Routing Decision System

In practice, you might want more control over when escalations happen. Here's a pattern for that:

```javascript
async function intelligentRouter(task, context) {
  // Executor makes an initial routing decision
  const routingDecision = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 500,
    system: `You are a routing agent. For the given task, decide:
1. Can you handle this confidently? (Answer: "SIMPLE", "COMPLEX", or "REVIEW")
2. If REVIEW or COMPLEX, what specific aspect needs expert guidance?`,
    messages: [
      {
        role: "user",
        content: `Task: ${task}\nContext: ${context}`,
      },
    ],
  });

  const routingText = routingDecision.content[0].text;
  const shouldEscalate =
    routingText.includes("COMPLEX") || routingText.includes("REVIEW");

  if (shouldEscalate) {
    // Extract the specific question for the advisor
    const advisorGuidance = await client.messages.create({
      model: "claude-3-opus-20250729",
      max_tokens: 1024,
      system: `Expert guidance based on routing decision:\n${routingText}`,
      messages: [
        {
          role: "user",
          content: `${task}\n\n${context}`,
        },
      ],
    });

    // Use guidance to finalize decision
    const finalDecision = await client.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 500,
      system: `Use this expert guidance to finalize your decision:\n${advisorGuidance.content[0].text}`,
      messages: [
        {
          role: "user",
          content: `Original routing question: ${routingText}\n\nNow, make the final decision.`,
        },
      ],
    });

    return finalDecision.content[0].text;
  } else {
    // Executor confident—no advisor needed
    return routingText;
  }
}
```

This pattern is useful when you want explicit control over escalation rather than letting the executor decide via tool calling ([Claude API best practices](https://docs.anthropic.com/)).

---

## Real-World Case Studies

### Case Study 1: Eve Legal — Document Extraction at Scale

Eve Legal processes thousands of legal documents daily (contracts, agreements, regulatory filings). Before Advisor Strategy, they ran Claude Sonnet for all extraction tasks. While Sonnet handles basic extraction well, legal documents often have:

- Ambiguous terminology (same phrase with different meanings in different clauses)
- Non-standard formatting (handwritten amendments, scanned pages with OCR artifacts)
- Contextual interpretation (what this obligation means in light of other terms)

**The problem:** Sonnet's mistakes on these ambiguous cases required manual review and correction—expensive at scale.

**The solution:** Route straightforward extractions to Sonnet (90% of documents), and escalate formatting ambiguities and contextual interpretation to Opus advisor.

**Results** ([Anthropic case study](https://claude.com/blog/the-advisor-strategy)):
- **72% reduction in documents requiring manual review** — From 8% to 2.2% of documents
- **Cost per document: -34%** — Fewer retries, fewer manual corrections
- **Extraction accuracy improved by 4%** — Advisor guidance prevented systematic errors in ambiguous cases

The lesson: Where human judgment matters and mistakes are expensive, escalation pays for itself immediately.

### Case Study 2: Bolt — Architectural Decisions in Real-Time

Bolt is an AI code editor that assists developers with code generation

Bolt uses Claude to assist developers with code generation and refactoring. The hardest part isn't syntax—it's architectural decisions:

- "Should this logic be a separate function or inline?"
- "Does this API design match the project's patterns?"
- "What's the cleanest way to handle this edge case?"

**The challenge:** These decisions require understanding the developer's codebase conventions, performance constraints, and maintainability goals. Sonnet makes reasonable guesses, but Opus catches subtle architectural issues (tight coupling, scalability problems, maintainability risks) that save developers from larger refactors later.

**Bolt's implementation:**
1. Executor (Sonnet) handles syntax and pattern-matching tasks
2. When code reaches architectural decision points, it escalates to Advisor
3. Advisor reasons about: existing patterns in the codebase, performance implications, testability

**Results:**
- **Higher retention:** Developers spend less time fixing bad architectural choices
- **Better code from the start:** Architectural guidance upfront prevents technical debt
- **Cost near Sonnet alone:** Because architectural decisions are ~5% of tokens, but prevent >5% of future issues

### Case Study 3: Genspark — Agent Orchestration and Planning

Genspark, an AI search engine, uses Claude agents for research planning, source evaluation, and synthesis. As agents grow more complex, planning becomes harder:

- Which sources are most relevant to verify?
- Should we refocus the research based on preliminary findings?
- What follow-up questions best fill gaps?

Sonnet's planning is reasonable but sometimes misses crucial gaps. Opus excels at this kind of multi-stage reasoning.

**Optimization:** Route information-gathering to Sonnet, route planning/synthesis decisions to Advisor.

**Impact:**
- **Research quality:** Multi-stage reasoning improved answer completeness scores by 8%
- **Cost:** 12% reduction vs. Opus-only, by offloading routine gathering
- **Latency:** No meaningful increase, because planning happens at decision points, not on every token

---

## Performance Benchmarks: What the Data Shows

Anthropic tested the Advisor Strategy against baseline approaches on several benchmarks:

### SWE-bench (Software Engineering Tasks)

| Approach | Pass Rate | Cost/Task | Cost/Pass |
| --- | --- | --- | --- |
| Sonnet 3.5 baseline | 45.2% | $0.087 | $0.192 |
| Opus baseline | 48.9% | $0.285 | $0.583 |
| **Advisor (Sonnet + Opus)** | **46.5%** | **0.077** | **0.165** |

Key insight: Advisor beats Sonnet on quality (+2.7%) while beating Opus on cost (-73%). The cost-per-correct-answer metric tells the real story.

### Agentic Reasoning Tasks

On multi-step reasoning (planning, code review, document analysis):

- **Advisor pattern:** 11.9% cost reduction vs. running Sonnet end-to-end
- Per-decision accuracy: 96.2% on simple decisions (executor), 98.7% on escalated decisions (advisor)
- Escalation rate: Average 3-8% of tasks, depending on task complexity

### Where Advisor Excels

*[CITATION CAPSULE]* The Advisor Strategy delivers measurable gains on tasks with asymmetric decision complexity, where 80-90% of decisions are routine but 10-20% require deep reasoning. On SWE-bench, this pattern achieved 2.7% accuracy improvement while reducing costs by 11.9% compared to running Sonnet alone, making it ideal for agentic workflows where decision quality varies across the task ([Anthropic, 2026](https://claude.com/blog/the-advisor-strategy)).

### Where Advisor May Be Overkill

- **Simple classification:** If 95%+ of decisions are straightforward, the overhead of an escalation system isn't worth it
- **Latency-critical systems:** If you need sub-200ms response times, Opus thinking might blow your budget
- **Fully streaming use cases:** Tool calling within streaming has latency trade-offs; check your metrics

---

## Cost Comparison: Manual Patterns vs. Advisor Tool

### Pattern 1: Manual Routing (Pre-Advisor)

Some teams built explicit routers before the Advisor tool existed:

```javascript
// Manual router: check input complexity, decide model upfront
if (complexity > 0.7) {
  useModel = "opus";
} else {
  useModel = "sonnet";
}
```

**Costs:**
- Routing logic itself: cheap (~1-2% overhead)
- But routing is brittle: threshold-based decisions miss nuance
- Failures: Complex tasks sent to Sonnet might require retries
- Overall: ~8-12% worse cost-to-quality ratio than Advisor

### Pattern 2: Adaptive Calls (Chain-of-Thought Escalation)

Some teams use multi-step reasoning with Sonnet, then escalate to Opus if Sonnet signals uncertainty:

```javascript
// Run Sonnet with explicit reasoning
// Check if output contains "I'm unsure" or "needs expert review"
// If yes, run Opus
```

**Costs:**
- Extra token cost: Full Sonnet pass + partial Opus pass
- Roughly equivalent to Advisor, but requires custom logic
- Less standardized, harder to debug

### Pattern 3: Advisor Strategy (Current Best)

```javascript
// Executor runs naturally, calls advisor when needed via tool
// Advisor is just another tool, like any external API
// No custom routing logic needed—model decides when to escalate
```

**Costs:**
- Only pays for Opus on escalations (typically 3-8% of tasks)
- No duplicate work; Opus has full context efficiently
- Built-in by Anthropic, so optimized for split billing
- **Result: 11.9% cost savings**

**Cost Comparison Table:**

| Pattern | Accuracy | Cost/Task | Code Complexity | Recommended For |
| --- | --- | --- | --- | --- |
| Sonnet only | 45.0% | $0.087 | Low | Simple, non-agentic tasks |
| Manual routing | 45.8% | $0.089 | Medium | Tasks with clear tiers |
| Opus only | 49.0% | $0.285 | Low | High-stakes, reasoning-heavy |
| Advisor pattern | 46.5% | $0.077 | Low | Agentic, mixed-complexity workflows |

The Advisor pattern achieves the lowest cost-per-correct-answer while keeping code simple—that's the geometric mean that makes it powerful.

---

## When to Use Advisor vs. Other Patterns

### Favor Advisor Strategy When:

- ✅ **Multi-step agents** — Your agent makes many decisions across different stages
- ✅ **Decision complexity varies** — Some decisions are routine (use Sonnet); others require expert judgment (use Opus)
- ✅ **Cost is a constraint** — Advisor optimizes the cost-to-quality frontier
- ✅ **You want simple code** — Tool calling is cleaner than custom routing logic
- ✅ **You expect 3-20% escalations** — Advisor shines in this range; below 3%, Sonnet only might suffice; above 20%, Opus only might be better
- ✅ **Error correction costs are high** — Legal/medical/finance use cases where mistakes are expensive

### Use Sonnet Alone When:

- ❌ **Simple classification** — If 95%+ of decisions are straightforward
- ❌ **Streaming latency critical** — Sub-100ms responses; tool calling adds latency
- ❌ **Trivial cost constraints** — If your org can afford Opus everywhere, do it

### Use Opus Alone When:

- ❌ **All decisions need reasoning** — If 80%+ of your task is complex reasoning, just use Opus
- ❌ **User is willing to pay** — Premium experiences demand premium models
- ❌ **Extreme accuracy critical** — High-stakes where 0.5% improvement justifies 3x cost

---

## Best Practices for Implementation

### 1. Define Your "Hard" Decisions Early

Before implementing, ask: What decisions in my agent actually need expert reasoning?

For Eve Legal: ambiguous field mappings, contextual interpretation
For Bolt: architectural patterns, code quality trade-offs
For Genspark: research planning, source prioritization

Map these out—they're your escalation triggers. Don't escalate everything.

### 2. Optimize Escalation Context

When the executor calls the advisor, pass the minimum context needed:

```javascript
// Bad: pass entire 50K context to advisor
advisor_question: "What should this field be?",
context: entire_document  // 50K tokens

// Good: pass focused context
advisor_question: "How should I interpret 'annual fees' in a contract where quarterly adjustments are mentioned?",
context: relevant_clauses_only  // 800 tokens
```

This cuts advisor costs by 60%+ while maintaining quality.

### 3. Measure Escalation Rates

Track:
- % of tasks triggering advisor
- Which decision types escalate most
- Accuracy on escalated vs. non-escalated decisions

If escalation>20%, you might have a routing problem (executor being too cautious).

### 4. Use Structured Output for Escalations

When executor calls advisor, structure the request:

```javascript
{
  question: "...",
  context: "...",
  options: ["Option A", "Option B", "Option C"],  // Multiple choice
  confidence_threshold: 0.8  // Only escalate if <80% confident
}
```

This helps the advisor focus and makes results actionable.

### 5. Version Your Advisor Logic

As you optimize, you'll iterate on:
- When to escalate (decision rules)
- What context to pass
- How to integrate advisor guidance

Version your prompt logic so you can A/B test:

```javascript
const escalation_rules = {
  v1: "Escalate if confidence < 0.7",
  v2: "Escalate if confidence < 0.7 OR decision_type === 'architectural'",
};
```

### 6. Monitor Cost Efficiency

Set up metrics:
```javascript
cost_per_correct_answer = total_cost / correct_decisions
escalation_value_ratio = (advisor_cost) / (cost_saved by improved decisions)
```

If this ratio is <0.5 (advisor calls cost less than 50% of the savings they generate), you're in good territory.

---

## Getting Started: Step-by-Step Setup

### Step 1: Update Your SDK

Ensure you're running the latest Anthropic SDK:

```bash
npm install @anthropic-ai/sdk@latest
# or
pip install anthropic==0.42.0  # or latest
```

### Step 2: Enable Advisor Tool

Add `advisor_20260301` to your tools array:

```javascript
const tools = [
  {
    name: "advisor_20260301",
    description: "Call Claude Opus for expert guidance on complex decisions",
    input_schema: {
      type: "object",
      properties: {
        question: {
          type: "string",
          description: "What decision do you need help with?",
        },
        context: {
          type: "string",
          description: "Relevant context for reasoning",
        },
      },
      required: ["question", "context"],
    },
  },
  // ... your other tools ...
];
```

### Step 3: Configure Cost Tracking

Set up logging to monitor advisor vs. executor costs:

```javascript
const advisorMetrics = {
  total_executor_tokens: 0,
  total_advisor_tokens: 0,
  advisor_calls: 0,
  improved_decisions: 0,
};

// In your message handler:
if (toolUse.name === "advisor_20260301") {
  advisorMetrics.advisor_calls++;
  // Log response tokens to calculate cost
}
```

### Step 4: Test on a Representative Sample

Before deploying to production:
1. Run 100+ representative tasks with Sonnet only
2. Run the same 100 tasks with Advisor (Sonnet + Opus)
3. Measure: accuracy, cost, escalation rate
4. Calculate ROI

### Step 5: Deploy and Monitor

Start with a small percentage of traffic, measure:
- Escalation rate (should be 3-10% for most tasks)
- Accuracy improvement
- Cost-per-correct-answer
- User satisfaction (if applicable)

Gradually ramp to 100% once metrics confirm improvement.

---

## Common Pitfalls and Solutions

**Pitfall 1:** "The executor is escalating too much (>20%)"
- **Cause:** Executor being overly cautious; system prompt discourages independent decisions
- **Fix:** Adjust system prompt to encourage executor confidence: "You're capable. Only escalate when you encounter a genuinely novel situation."

**Pitfall 2:** "Advisor is making decisions inconsistent with executor"
- **Cause:** Different system prompts or context windows
- **Fix:** Ensure advisor system prompt is aligned with executor goals; pass clear context to advisor

**Pitfall 3:** "Latency spiked because of advisor calls"
- **Cause:** Advisor is being called synchronously in a critical path
- **Fix:** Queue advisor calls asynchronously where possible, or batch them

**Pitfall 4:** "Costs went up, not down"
- **Cause:** Advisor being over-used; or passing oversized context to advisor
- **Fix:** Reduce escalation scope; compress context passed to advisor to minimum necessary

---

## Frequently Asked Questions

### Can I use Advisor with other Claude models besides Sonnet?

Yes. The executor can be any Claude model (Haiku, Sonnet, Opus), though the pattern assumes a cheaper executor paired with Opus advisor. Theoretically, you could use Sonnet as executor and Opus 4 as advisor (not released yet), or even Haiku for simple tasks with Sonnet as advisor—the pattern scales to any capability tier.

### What's the minimum scalable escalation rate?

If fewer than 2% of your tasks escalate to advisor, the overhead of the tool infrastructure might not be worth it—just use Sonnet. If 80%+ escalate, you're probably better off using Opus. The sweet spot is 5-15% escalation.

### Does Advisor work with streaming responses?

Yes, though tool calls (including advisor calls) don't stream—the tool use event is atomic. Your response streams normally otherwise.

### How long do advisor calls typically take?

Median ~500-1000ms for an advisor decision, depending on context length. This is slower than Sonnet (100-300ms) but acceptable for most agentic workflows since advisor isn't in the critical latency path.

### Can I use this for real-time applications?

Depends on your latency budget. For real-time transcription or live chat, sub-100ms responses are critical—advisor might be too slow. For batch processing, document analysis, or research agents, the 500-1000ms advisor latency is invisible.

### What happens if the advisor itself is uncertain?

The advisor responds with its best reasoning. The executor can then choose to trust it, request clarification, or escalate further (escalation chains are possible but uncommon).

---

## The Future of Agentic Patterns

The Advisor Strategy represents a shift in how we think about AI agents: not as single monolithic decision-makers, but as tiered systems where different capabilities are deployed at the points where they add the most value.

We're likely to see variations on this pattern:
- **Multiple advisors:** Different expert models for different domains (legal advisor, architecture advisor, security advisor)
- **Advisor chains:** Executor → Specialist Advisor → Expert Advisor for extreme edge cases
- **Learned escalation:** Training the executor to predict when escalation will help, improving the 5-8% escalation rate

The core insight—pairing cost efficiency with expert reasoning—will remain fundamental to production AI systems.

---

## Key Takeaways

- **Advisor Strategy pairs fast executors with expert advisors** for intelligent cost reduction
- **2.7% accuracy improvement + 11.9% cost savings** vs. Sonnet alone on complex tasks
- **Optimal escalation rate:** 5-15% of decisions, routing the hard ones to Opus
- **Implementation is simple:** Use the new `advisor_20260301` tool, let the model decide when to escalate
- **Real-world results:** Eve Legal cut manual review by 72%, Bolt improved code architecture, Genspark improved research quality
- **Best for:** Multi-step agents with variable decision complexity; less useful for simple classification or streaming latency-critical systems

The Advisor Strategy is production-ready today. If you're building agents, try it on your next project—the cost savings alone often justify the engineering effort.

---

## See Also

Related resources:
- Building Agentic Systems with Claude (agent architecture patterns)
- Cost Optimization for LLM Applications (budget management)
- Measuring LLM Quality: Beyond Accuracy (evaluation metrics)
