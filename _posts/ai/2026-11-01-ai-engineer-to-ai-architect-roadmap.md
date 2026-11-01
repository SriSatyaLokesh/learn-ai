---
layout: post
title: "The AI Engineer to AI Architect Roadmap: Free Courses, Official Sources, Two Career Stages"
date: 2026-11-01 09:00:00 +0530
last_modified_at: 2026-11-01

category: ai
tags: [ai-engineer, ai-architect, careers, rag, agents, evals, llmops, learning-path]

excerpt: "Two stacked roadmaps built only from free, official resources: 8 stages to become an AI Engineer who ships LLM products, then 8 stages to grow into an AI Architect who designs the platform."
description: "Free AI Engineer and AI Architect learning path: Anthropic, OpenAI, DeepLearning.AI, Hugging Face, AWS, Azure, Google Cloud, OWASP, NIST. Verified links, stage order, projects, timeline."

difficulty: intermediate
read_time: true
toc: true
toc_sticky: true

image: https://www.kdnuggets.com/wp-content/uploads/kdn-the-roadmap-to-becoming-an-ai-architect-in-2026.png
header:
  image_credit: "KDnuggets"
  image_credit_url: "https://www.kdnuggets.com/"

seo:
  primary_keyword: "AI engineer roadmap"
  secondary_keywords: [ai architect roadmap, free ai engineering courses, rag course, ai agents course, llm evals, llmops, generative ai architecture]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/ai-engineer-to-ai-architect-roadmap/"

author: satya-k
---

## Why This Roadmap?

The [LLM Engineer Roadmap](/llm-engineer-roadmap-from-ml-basics-to-production/) on this site is for people who want to go *inside* the model: transformers, pretraining, fine-tuning, inference kernels. This post is for the two roles that sit *on top of* the model.

- **AI Engineer**: a software engineer who builds products on foundation models instead of training them. Prompts and context, structured outputs, tool calling, RAG, agents, evals, observability, cost, latency, security. Latent Space's "The Rise of the AI Engineer" put it bluntly: "when it comes to shipping AI products, you want engineers, not researchers."
- **AI Architect**: the person who owns the design of AI systems and platforms across teams. SaaS vs PaaS vs self-host, RAG vs fine-tune, single agent vs multi-agent, gateway and routing, governance, compliance, token economics. Microsoft's new AB-100 "Agentic AI Business Solutions Architect" credential describes the role as defining architecture strategy, designing multi-agent orchestration, working with open protocols like MCP and A2A, securing AI data flows, and doing ROI analysis.

The two roadmaps below stack. Part 1 makes you an AI Engineer. Part 2 assumes Part 1 and makes you an AI Architect.

**Rules used to pick every resource:**

- Full learning content is free. Audit mode or a free tier counts. Paid certificates are fine. Paywalled content is out.
- Official or primary source only: vendor docs and courses (Anthropic, OpenAI, Google, Microsoft, AWS, Hugging Face, DeepLearning.AI), universities, standards bodies (OWASP, NIST, EU Commission), or the practitioners the field actually cites.
- Alive and current. Every link was fetched on 2026-11-01. Anything older than 2024 is flagged.

**Two caveats before you enroll:**

- Every DeepLearning.AI short course below says "free for a limited time during the DeepLearning.AI learning platform beta." Videos and code are free today. Graded assignments and certificates need PRO. That could change, so enroll early.
- Anthropic archived its old `anthropics/courses` GitHub repo on 2026-09-15. The free Anthropic Academy courses on Skilljar replace it. Those may move to academy.claude.com later, so if a link breaks, search the course title.

**Assumption**: You can write Python, use Git, and ship a basic web API. You do not need the LLM Engineer roadmap first.

---

# Part 1 — The AI Engineer Roadmap (8 Stages)

Total: about 24 weeks at 8–10 hours per week.

### Stage 1 — LLM Intuition and the App-Builder Mindset

#### 1. Andrej Karpathy: "Deep Dive into LLMs like ChatGPT" + "How I use LLMs"
**Duration**: 1 week | **Effort**: Low

**YouTube**: [Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI) (3h31m) | [How I use LLMs](https://www.youtube.com/watch?v=EWvNQjAaOHw) (2h11m)

**Why first?**

Before prompts make sense you need a working model of tokens, context windows, sampling, post-training, and why models hallucinate and refuse. Karpathy gives you exactly that in under six hours, from a top-tier practitioner, with no math prerequisite. This is the application-first substitute for the MIT and Stanford theory courses in the LLM Engineer path.

**What you'll learn**:
- Pretraining, tokenization and next-token prediction at the level an app builder needs
- SFT and RLHF, and why models follow system prompts
- Context windows as working memory versus knowledge
- Tool use in practice: search, code interpreter, file uploads
- Choosing a model tier for a task

**Project idea**: Write a one-page "LLM failure modes" cheat sheet with five reproducible examples you found yourself. You will reuse them as eval seeds in Stage 6.

#### 2. Microsoft "Generative AI for Beginners" (v3)
**Duration**: 2 weeks (lessons 1–8, 11–15) | **Effort**: Low–Medium

**Official repo**: [microsoft/generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners). 21 lessons, most with their own video, Python and TypeScript.

**Why?**

The broadest structured on-ramp that is explicitly about *building apps*. Use it as a map, not a destination. Weakness: Azure-centric, and some samples depend on the GitHub Models endpoint that retires in July 2026.

**What you'll learn**:
- Prompt engineering fundamentals and advanced prompts
- Chat apps, search apps with vector DBs, function calling
- UX for AI apps, securing GenAI apps, application lifecycle
- RAG with vector databases, open models via Hugging Face

**Project idea**: A small chat app (FastAPI or Streamlit) that runs against two providers behind one interface.

**Next**: Learn one vendor SDK deeply in Stage 2.

---

### Stage 2 — LLM APIs and Prompt Engineering

#### 3. Anthropic Academy: "Building with the Claude API"
**Duration**: 2–3 weeks | **Effort**: Medium

**Official course**: [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api). Free, with a completion certificate. About 85 items across 12 sections.

**Why this one?**

It is the only free vendor-official course that walks the entire AI Engineer stack in one arc: API basics, prompting, prompt evals with code-based and model-based graders, tool use, RAG and agentic search, extended thinking, citations, prompt caching, MCP, and agents versus workflows. Everything later in this roadmap gets introduced here first. Weakness: Claude-specific. Pair it with the OpenAI side below.

**What you'll learn**:
- Multi-turn chat, system prompts, streaming, structured data
- Prompt evaluation with test datasets
- Tool schemas and multi-turn tool loops
- Chunking, embeddings, BM25, multi-index retrieval
- Workflow patterns: chaining, routing, parallelization

**Project idea**: A support-ticket triager CLI that classifies, extracts fields and drafts replies, with a 30-example test set and a code-based grader.

#### 4. DeepLearning.AI: "ChatGPT Prompt Engineering for Developers"
**Duration**: A weekend | **Effort**: Low

**Official course**: [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/). Isa Fulford (OpenAI) and Andrew Ng. 1h40m.

**Why?**

The canonical short course on the OpenAI side, which gives you a second SDK. Flag: the core material dates from 2023 and predates the Responses API and reasoning models. Treat it as fundamentals only.

**Project idea**: Port the triager to the OpenAI SDK and compare outputs on the same test set.

**Reference shelf** (read alongside, not courses):
- [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Google "Prompt Engineering" whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering) by Lee Boonstra (2025)
- [Prompt Engineering Guide](https://www.promptingguide.ai/) by DAIR.AI

**Next**: Learn the primitive under RAG and agents in Stage 3.

---

### Stage 3 — Structured Outputs, Tool Use and MCP

#### 5. DeepLearning.AI: "Getting Structured LLM Output"
**Duration**: 1 week | **Effort**: Medium

**Official course**: [Getting Structured LLM Output](https://www.deeplearning.ai/short-courses/getting-structured-llm-output/). Will Kurt and Cameron Pfiffer (.txt). 1h21m, updated July 2026.

**Why?**

RAG and agents are both "the model calls functions and returns typed data." This is the only free course that explains all three ways to get that reliably: API-native JSON Schema, retry-and-validate libraries, and constrained decoding on open-weight models.

**Companion docs**: [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | [Instructor](https://python.useinstructor.com/) by Jason Liu

**Project idea**: An invoice extractor with a Pydantic schema. Compare validation-failure rates across native structured output, Instructor retries and Outlines on a local model.

#### 6. Anthropic Academy: "Introduction to Model Context Protocol" (+ Advanced Topics)
**Duration**: 1 week | **Effort**: Medium

**Official courses**: [Introduction to MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | [MCP Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics). Both free.

**Why?**

Protocol-author official and hands-on: architecture, servers with the Python SDK, tools, resources, prompts, clients, the MCP Inspector. The LLM Engineer roadmap lists the DeepLearning.AI MCP course. This is the non-duplicating pick.

**Required reading**: [Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (Anthropic, September 2025). Tool consolidation, namespacing, token-efficient responses, tool evals.

**Project idea**: Expose the Stage 3 extractor plus a SQLite expenses DB as an MCP server with three well-designed tools. Drive it from Claude Desktop or an IDE.

**Next**: The most common production pattern, in Stage 4.

---

### Stage 4 — RAG and Retrieval

#### 7. DataTalks.Club: LLM Zoomcamp (2026)
**Duration**: 4 weeks modules + 2–3 weeks capstone | **Effort**: High

**Official repo**: [llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) | **YouTube**: [LLM Zoomcamp playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv)

**Why?**

The most complete fully free RAG course, refreshed yearly, with a peer-reviewed capstone rubric. It bakes evals and monitoring into RAG from day one, which most RAG tutorials skip. Expect a few dollars of API credits. Weakness: community-run rather than university or vendor.

**What you'll learn**:
- Keyword-search RAG, then made agentic with function calling
- Vector search with embeddings (minsearch, sqlitesearch, pgvector)
- Retrieval evals (hit rate, MRR) and answer evals (LLM-as-judge), offline and online
- Monitoring with user feedback and dashboards
- Hybrid search, reranking, LangChain

**Project idea**: The course capstone. A RAG assistant over a corpus you care about, with a retrieval eval set and a monitoring dashboard.

#### 8. Jason Liu: "Systematically Improving RAG Applications" (open materials)
**Duration**: 2–3 weeks | **Effort**: High

**Official repo**: [jxnl/systematically-improving-rag](https://github.com/jxnl/systematically-improving-rag). Workshop chapters 0–7, weekly notebooks, case studies. Readable for free. No license stated, so read, don't republish.

**Why?**

The best practitioner material on improving RAG *after* v1: evaluate retrieval first, synthetic questions, cluster user queries to find the worst segment, fine-tune embeddings and rerankers, metadata routing, feedback UX. Exactly what Zoomcamp does not cover.

**Project idea**: Cluster 200 real or synthetic queries against your capstone. Find the worst segment. Ship one targeted fix with a before/after recall chart.

**Paid but excellent**: DeepLearning.AI's [Retrieval Augmented Generation](https://www.deeplearning.ai/courses/retrieval-augmented-generation-rag/) by Zain Hasan (26h). Only module 1 is free. Listed here for budget holders only.

**Next**: Tool use plus retrieval in a loop, in Stage 5.

---

### Stage 5 — Agents and Context Engineering

#### 9. The three agent essays (half a day, required)

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic, December 2024. Workflows before agents: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. When *not* to build an agent.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic, September 2025. Context rot, just-in-time retrieval, compaction, sub-agents.
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — OpenAI, 34-page PDF. When to build, design foundations, guardrails.

**Project idea**: Reimplement three of the five workflow patterns in plain Python against your Stage 3 tools. No framework.

#### 10. DeepLearning.AI: "Agentic AI" (Andrew Ng)
**Duration**: 3 weeks | **Effort**: Medium

**Official course**: [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/). 9h55m, 31 videos. Free to audit (videos and forum). Graded labs and certificate need PRO.

**Why?**

Framework-agnostic. Every pattern (reflection, tool use, planning, multi-agent) is built from first principles before any framework. The error-analysis and eval sections are the ones engineers actually need.

**Project idea**: A research-report agent (plan, search, reflect, write) with a trace log and a 20-task eval set measuring task success and steps per task.

#### 11. Hugging Face: AI Agents Course
**Duration**: 3–5 weeks | **Effort**: Medium–High

**Official course**: [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction). Free, both certificates included.

**Why?**

The best free framework-comparison course: smolagents, LlamaIndex and LangGraph side by side. The final assignment scores your agent on a GAIA-style leaderboard, which makes it portfolio-worthy. Bonus units cover function-calling fine-tuning and agent observability. Weakness: leans toward open-weight models.

**Project idea**: Pass the Unit 4 benchmark, then port the same agent to a second framework and compare reliability.

**Stack-specific alternates** (pick one if your target job uses it):
- [Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) — LangChain Academy, free, about 6h.
- [Kaggle × Google 5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents) — whitepapers plus ADK/Gemini codelabs, self-paced.
- [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) — 18 lessons incl. MCP/A2A, memory, securing agents. Best for Azure shops.
- [UC Berkeley Agentic AI MOOC, Fall 2025](https://agenticai-learning.org/f25) — [YouTube playlist](https://www.youtube.com/playlist?list=PLS01nW3RtgoqGkm4UeqNeZLccW-OGc1fJ). Research-leaning guest lectures from OpenAI, DeepMind, NVIDIA, Sierra. Watch selectively.

**Next**: Turn "it seems to work" into numbers, in Stage 6.

---

### Stage 6 — Evals and Observability

#### 12. Hamel Husain and Shreya Shankar: the free evals corpus
**Duration**: 1.5 weeks | **Effort**: Medium

Read in this order:
1. [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) (2024)
2. [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) (2025)
3. [Using LLM-as-a-Judge for Evaluation](https://hamel.dev/blog/posts/llm-judge/) (updated September 2026)
4. [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) (September 2026)

**Why?**

This is the practitioner canon on product evals, updated in 2026 and free. Error analysis first. Read traces, open-code failures, build a failure taxonomy. Binary pass/fail with critiques instead of Likert scales. Validate your LLM judge against a domain expert. Their Maven course is paid and not required.

**Project idea**: Run a 100-trace error analysis on your Stage 5 agent. Produce a failure taxonomy, two code assertions and one LLM judge. Report the judge's true-positive and true-negative rates against your own labels.

#### 13. DeepLearning.AI: "Evaluating AI Agents"
**Duration**: 1 week | **Effort**: Medium

**Official course**: [Evaluating AI Agents](https://www.deeplearning.ai/short-courses/evaluating-ai-agents/). John Gilhuly and Aman Khan (Arize). 2h36m, updated July 2026.

**Why?**

The most hands-on free course on agent evals specifically: tracing with OpenTelemetry-style spans, code versus LLM-judge evaluators per component, router and trajectory evaluation, convergence scoring, production monitoring. Uses Arize Phoenix, but the concepts transfer.

**Optional**: [LangSmith Essentials](https://academy.langchain.com/courses/quickstart-langsmith-essentials) from LangChain Academy. Half an hour of video on what an eval-and-observability platform does end to end.

**Project idea**: Add tracing to your agent and build a trajectory eval. Track convergence across two prompt versions.

**Next**: Harden the system in Stage 7.

---

### Stage 7 — Production: Cost, Latency, Serving, Guardrails, Security

#### 14. The production reading pack
**Duration**: 1 week | **Effort**: Medium

- [Building A Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html) — Chip Huyen, 2024. The best single free architecture diagram of a production LLM app: context construction, guardrails, router and gateway, three kinds of caching, write actions, observability.
- [What We've Learned From A Year of Building with LLMs](https://applied-llms.org/) — Eugene Yan, Bryan Bischof, Charles Frye, Hamel Husain, Jason Liu, Shreya Shankar, 2024. Tactical, operational and strategic lessons.
- [OpenAI latency optimization](https://developers.openai.com/api/docs/guides/latency-optimization) and [Claude prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

Flag: the first two are 2024. Principles hold, model and price examples are dated.

**Project idea**: Add a gateway layer to your capstone: cheap-vs-strong model routing, prompt caching, a semantic cache, and a dashboard with p50/p95 latency and dollars per successful task.

#### 15. DeepLearning.AI: "Semantic Caching for AI Agents"
**Duration**: 2–3 days | **Effort**: Medium

**Official course**: [Semantic Caching for AI Agents](https://www.deeplearning.ai/short-courses/semantic-caching-for-ai-agents). Redis. 1h14m.

**Why?** The only free course that treats cache correctness as an eval problem: hit rate, precision/recall, threshold tuning, false hits.

#### 16. Security and guardrails
**Duration**: 1 week | **Effort**: Medium

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [Simon Willison on prompt injection](https://simonwillison.net/tags/prompt-injection/), including the "lethal trifecta". Still an unsolved problem. Read him.
- DeepLearning.AI [Red Teaming LLM Applications](https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/) (Giskard, 1h39m) and [Safe and Reliable AI via Guardrails](https://www.deeplearning.ai/short-courses/safe-and-reliable-ai-via-guardrails/) (Guardrails AI, 1h42m).

**Project idea**: Red-team your capstone with 30 attacks mapped to OWASP IDs. Add input/output guards. Report attack success rate before and after.

#### 17. Open-weight serving, just enough
**Duration**: 1 week | **Effort**: Medium–High

- [vLLM docs](https://docs.vllm.ai/en/latest/): quickstart and the OpenAI-compatible server.
- [LLM Inference Handbook](https://handbook.modular.com/): TTFT and goodput, quantization, continuous batching, prefix caching, cost.

An AI Engineer must be able to self-host an open-weight model behind an OpenAI-compatible endpoint and reason about cost. Kernel-level depth belongs to the LLM Engineer roadmap.

**Project idea**: Serve an 8B-class model with vLLM. Point your capstone at it. Compare quality (your eval suite), p95 latency and cost per 1k requests against a hosted API.

**Next**: Put it all together in Stage 8.

---

### Stage 8 — Capstone and Staying Current

**Capstone spec**: a domain assistant that combines RAG over a real corpus, three or more MCP tools (one a write action with human approval), a workflow-first agent loop, an eval suite in CI (failure taxonomy, assertions, validated LLM judge), tracing, prompt caching, model routing, a self-hosted fallback model, and OWASP-mapped guardrails. Deploy it publicly. Write a README with cost, latency and quality numbers and a failure-analysis section.

**Staying current**:
- [AI Engineer YouTube channel](https://www.youtube.com/@aiDotEngineer): Summit and World's Fair talks.
- [Simon Willison's blog](https://simonwillison.net/) and his [`llm` CLI](https://llm.datasette.io/).
- [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks) and the [OpenAI Cookbook](https://developers.openai.com/cookbook).

---

### AI Engineer: The Compressed Top 10

| # | Resource | Stage | Time |
|---|----------|-------|------|
| 1 | Karpathy, Deep Dive into LLMs + How I use LLMs | 1 | 1 wk |
| 2 | Anthropic Academy, Building with the Claude API | 2 | 3 wk |
| 3 | DL.AI Getting Structured LLM Output + Instructor | 3 | 1 wk |
| 4 | Anthropic Academy Intro to MCP + Writing effective tools | 3 | 1 wk |
| 5 | LLM Zoomcamp incl. capstone | 4 | 5–6 wk |
| 6 | Building effective agents + context engineering + OpenAI guide | 5 | 0.5 wk |
| 7 | DL.AI Agentic AI (audit) | 5 | 3 wk |
| 8 | Hugging Face Agents Course | 5 | 3–5 wk |
| 9 | Husain/Shankar evals corpus + DL.AI Evaluating AI Agents | 6 | 2.5 wk |
| 10 | Production pack + OWASP LLM and Agentic Top 10 | 7 | 1.5 wk |

About 22–25 weeks at 8–10 h/week. If time is short, cut #8 to Unit 1 plus the final assignment. Never skip #9.

### AI Engineer: Timeline

One growing codebase, not isolated toys. Each stage extends the last.

| Month | Stages | Milestone |
|-------|--------|-----------|
| 1 | 1–2 | Multi-provider triager with a 30-case test set |
| 2 | 3 + start of 4 | Typed extractor, MCP server, first RAG baseline |
| 3 | 4 | RAG with retrieval evals and monitoring |
| 4 | 5 | Workflow-first agent with traces |
| 5 | 6–7 | Eval suite in CI, cost/latency dashboard, red-team report |
| 6 | 8 | Public capstone with README metrics |

---

# Part 2 — The AI Architect Roadmap (8 Stages)

Total: about 5 months at 6–8 hours per week. Assumes Part 1.

The engineer builds the components. The architect decides which components exist, who owns them, what they cost, and what happens when they fail. The output of this track is not code. It is a portfolio of architecture artifacts: ADRs, a reference architecture, a threat model, a risk register, a cost model, an eval strategy, an observability standard, a strategy deck.

### Stage 0 — Prerequisite Check (1 week)

You are ready if you can, without notes: explain Anthropic's five workflow patterns and when not to use an agent; build a RAG app with hybrid retrieval and an LLM-judge eval; deploy an LLM service behind an API. If not, finish Part 1.

**Deliverable**: a one-page current-state diagram of an LLM app you built, every component labelled with owner and failure mode. You will redraw it in every later stage.

---

### Stage 1 — Architecture Foundations

#### A1. Martin Kleppmann: Distributed Systems (University of Cambridge)
**Duration**: 2 weeks | **Effort**: Medium

**Official course**: [Concurrent and Distributed Systems, 2025–26](https://www.cl.cam.ac.uk/teaching/2526/ConcDisSys/) | **Notes (PDF)**: [dist-sys-notes.pdf](https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf) | **YouTube**: [Distributed Systems lecture series](https://www.youtube.com/playlist?list=PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB) (23 videos, about 7h)

**Why?**

Consistency, replication, failure and consensus underlie every vector store, queue, agent-memory store and multi-region gateway you will design. This is the clearest short treatment by the author of *Designing Data-Intensive Applications*. Flag: recorded 2020. The fundamentals are timeless. You have to make the link to AI systems yourself.

**Deliverable**: a two-page note. Pick a vector store and an agent-memory store you use. State each one's consistency model and what a user sees during a partition or failover. Log it as ADR-001.

#### A2. The architect's toolkit: Azure Well-Architected "Architect role" + ADRs
**Duration**: 1 week | **Effort**: Low

- [Solution architect's responsibilities](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/fundamentals) (Microsoft Learn, updated 2026)
- [Architecture decision records](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [adr.github.io](https://adr.github.io/): templates, MADR, Y-statements

**Why?** The only free official text that describes the architect's actual outputs: requirement alignment, design spec, diagrams, ADR log, PoCs, cost and health models. Vendor-neutral in substance.

**Deliverable**: an `adr/` folder using MADR. Write ADR-000 ("we record decisions") and ADR-001 from A1. Every later stage adds to it.

---

### Stage 2 — MLOps and LLMOps Platforms

#### A3. Made With ML (or MLOps Zoomcamp)
**Duration**: 4–5 weeks | **Effort**: High

**Official course**: [madewithml.com](https://madewithml.com/) by Goku Mohandas | **Repo**: [GokuMohandas/Made-With-ML](https://github.com/GokuMohandas/Made-With-ML)

**Why?** The only free course that treats ML as a software-engineering *system* with an explicit systems-design lesson: product and systems design, distributed data and training, experiment tracking, serving, testing code/data/models, CI/CD, monitoring. Flag: core lessons date from 2023 and predate LLMOps. Bolt on A4.

**Alternative**: [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) from DataTalks.Club, [YouTube playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK) (43 videos). More hands-on and tool-centric (MLflow, Prefect).

**Deliverable**: a platform design doc for "the ML/LLM platform for a five-team org": registry, grounding data store, CI/CD/CT, environments and promotion, on-call ownership.

#### A4. MLOps and GenAIOps maturity guidance
**Duration**: 1 week | **Effort**: Low–Medium

- Google: [MLOps continuous delivery and automation pipelines](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) (levels 0, 1, 2)
- Azure: [MLOps and GenAIOps for AI workloads](https://learn.microsoft.com/en-us/azure/well-architected/ai/mlops-genaiops) and the [MLOps maturity model](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/mlops-maturity-model)

**Why?** The canonical vendor-maintained vocabulary executives and platform teams already use. Google's piece is predictive-ML only, so pair it with the Azure GenAIOps page.

**Deliverable**: score your org on both maturity models. Write a two-quarter roadmap to move up one level.

---

### Stage 3 — GenAI System Patterns at Scale (the core stage, 5 weeks)

#### A5. Chip Huyen: "Building A Generative AI Platform"
**Duration**: 1 week | **Effort**: Low–Medium

[huyenchip.com/2024/07/25/genai-platform.html](https://huyenchip.com/2024/07/25/genai-platform.html). You read it as an engineer in Part 1. Now reread it as the platform owner.

**Deliverable**: redraw your Stage 0 diagram as a target-state platform. For each component decide: shared platform service or per-app.

#### A6. Martin Fowler and Bharani Subramaniam: "Emerging Patterns in Building GenAI Products"
**Duration**: 3 days | **Effort**: Low

[martinfowler.com/articles/gen-ai-patterns/](https://martinfowler.com/articles/gen-ai-patterns/) (2025). Direct Prompting, Evals, Embeddings, RAG, Hybrid Retriever, Query Rewriting, Reranker, Guardrails, Fine Tuning. Each as problem, solution, when to use.

**Why?** A pattern language with explicit "when to use" reasoning is what an architect hands to teams. No agent patterns, so A7 fills that.

**Deliverable**: a "RAG vs fine-tune vs prompt-only" decision tree as an ADR template teams fill in.

#### A7. Agent orchestration patterns (read all three together)
**Duration**: 1.5 weeks | **Effort**: Medium

- Azure: [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) (2026): sequential, concurrent, group chat, handoff, magentic.
- Google Cloud: [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (2026): coordinator, hierarchical, swarm, review-and-critique, human-in-the-loop.
- Anthropic: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (2025). A candid production post-mortem with real numbers: about 15x the tokens of a chat, when multi-agent is wrong, context isolation, rainbow deployments.

**Deliverable**: for one business process, compare a single agent, a sequential pipeline and an orchestrator-workers design on cost per task, latency, failure blast radius and debuggability. Record the choice in an ADR.

#### A8. RAG at scale: Azure "Design and develop a RAG solution" series
**Duration**: 1 week | **Effort**: Medium

[RAG solution design and evaluation guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide) (8–9 articles, updated 2026). Chunking economics, enrichment, embedding selection, index configuration, per-step and end-to-end evaluation, when to go agentic. The most systematic free experiment-driven RAG design method. Examples use Azure AI Search, the method transfers.

**Deliverable**: a grounding-data architecture: ingestion SLAs, re-index strategy, ACL propagation, per-tenant isolation, plus a chunking cost model for 10M documents.

#### A9. Model gateway, routing and interoperability protocols
**Duration**: 1 week | **Effort**: Medium

- Azure: [Access language models through a gateway](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/generative-ai-gateway) (2026). Failover, 429 handling, federated auth, chargeback, semantic caching, and explicitly when *not* to add a gateway.
- [MCP specification](https://modelcontextprotocol.io/specification/latest) (2026-07-28 revision)
- [A2A protocol](https://a2a-protocol.org/latest/)

**Deliverable**: a model-gateway reference architecture: routing policy, fallback chain, quota per team, cost attribution tags, MCP server trust boundary.

---

### Stage 4 — Cloud AI Architecture

Go deep on your primary cloud, skim the other two for trade-offs.

#### A10. AWS Well-Architected Generative AI Lens
**Duration**: 2 weeks | **Effort**: Medium–High

[Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) (published 2025-11-19) and the [Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html). Six pillars applied to GenAI: excessive agency, prompt security, distributed inference, cost-optimized model selection, vector-store and agent-workflow cost. The lens JSON imports into the free AWS WA Tool.

**Why?** The most complete pillar-by-pillar GenAI review checklist from any vendor. Implementation steps assume Bedrock and SageMaker.

**Optional exam**: AWS Certified Generative AI Developer – Professional (AIP-C01), USD 300.

**Deliverable**: run a Well-Architected review of your Stage 3 design. Produce a risk register with remediation.

#### A11. Azure Well-Architected: AI workloads + baseline reference architecture
**Duration**: 1.5 weeks | **Effort**: Medium

[AI workloads on Azure](https://learn.microsoft.com/en-us/azure/well-architected/ai/) and the [baseline Foundry chat reference architecture](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat) (2026). Strongest free coverage of *data* architecture for AI (training vs grounding data) and of workload personas, including agentic personas with just-in-time permissions.

**Optional exams**: Microsoft AB-100 (Agentic AI Business Solutions Architect Expert; learning paths not yet published as of November 2026, exam updates 2026-11-16) or AI-300.

**Deliverable**: adapt the baseline architecture to your own stack. Write a "deltas" ADR for each substitution.

#### A12. Google Cloud Well-Architected Framework: AI and ML perspective
**Duration**: 1 week | **Effort**: Medium

[AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml) (updated 2026-10-29, the freshest of the three). Use it as the cross-check against A10 and A11.

**Deliverable**: a one-page AWS vs Azure vs GCP comparison: model hosting options, data residency controls, gateway options. Feed it into a cloud-selection ADR.

---

### Stage 5 — Security, Safety, Governance and Compliance

#### A13. OWASP Top 10 for LLM (2025) + Top 10 for Agentic Applications (2026)
**Duration**: 1 week | **Effort**: Medium

[LLM Top 10](https://genai.owasp.org/llm-top-10/) | [Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | [Agentic AI threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)

In Part 1 you used these as a red-team checklist. Here they become the shared vocabulary your security team and auditors will use. They are lists, not architecture. You map each item to a control.

**Deliverable**: a STRIDE-style threat model of your Stage 3 architecture, every OWASP LLM and ASI item mapped to a control and an owner.

#### A14. MITRE ATLAS + Microsoft's red-teaming lessons
**Duration**: 1 week | **Effort**: Medium

[atlas.mitre.org](https://atlas.mitre.org/) (data release v2026.10: 16 tactics, 129 techniques, 77 case studies; the [GitHub data](https://github.com/mitre-atlas/atlas-data) is easier to read than the JS-heavy site) and [Lessons from red teaming 100 generative AI products](https://arxiv.org/abs/2501.07238) (Microsoft AI Red Team, 2025).

**Deliverable**: a red-team plan: scope, ATLAS techniques to test, success criteria, how findings flow back into ADRs.

#### A15. NIST AI Risk Management Framework + Generative AI Profile
**Duration**: 1.5 weeks | **Effort**: Medium–High

[AI RMF overview](https://www.nist.gov/itl/ai-risk-management-framework) | [NIST AI 600-1, Generative AI Profile (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | [Playbook](https://airc.nist.gov/airmf-resources/playbook/)

Govern, Map, Measure, Manage. Twelve GenAI-specific risks with suggested actions. The de-facto US governance reference, and it maps to ISO 42001 and the EU AI Act. Flag: AI RMF 1.0 (2023) is being revised under the White House AI Action Plan. Re-check before you cite it in a deliverable.

**Deliverable**: an AI risk register and RACI for one use case, organized by the four functions, each risk linked to a control from A13 and A14.

#### A16. EU AI Act, primary source
**Duration**: 1 week | **Effort**: Medium

[European Commission regulatory framework page](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | [AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/)

Risk tiers, prohibited practices (in force since February 2025), GPAI obligations (since August 2025), transparency obligations. Important: the "AI Omnibus" in force since 2026-07-27 moved high-risk Annex III obligations to 2027-12-02 and Annex I to 2028-08-02. Any summary written before mid-2026 has the wrong dates. Read the primary source.

**Deliverable**: a classification memo for three of your use cases with an architecture-requirements appendix: logging, human oversight, transparency labels, data governance.

#### A17. Google Secure AI Framework (SAIF)
**Duration**: 3 days | **Effort**: Low

[saif.google](https://saif.google/). Lifecycle-oriented security map, 15 risks with controls, an agent-specific section and an interactive Agent Risk Self Assessment.

**Deliverable**: run the self-assessment on your design and reconcile it with your A13 threat model.

**ISO/IEC 42001 note**: the standard itself is paid. Read [ISO's free explainer](https://www.iso.org/insights/iso-42001-explained) for context only.

---

### Stage 6 — Cost, Evaluation Strategy and Observability at Org Scale

#### A18. FinOps Foundation: FinOps for AI
**Duration**: 3 days | **Effort**: Low–Medium

[FinOps for AI overview](https://www.finops.org/wg/finops-for-ai-overview/) (updated 2026-10-28). Where AI spend appears, "allocate first, then optimize", and the key metric: **cost per successful outcome**, not cost per token. Companion: [Google Cloud AI/ML cost optimization pillar](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml/cost-optimization).

**Deliverable**: a cost model for your Stage 3 system: tokens per task, cache hit rate, routing mix, cost per successful outcome under three load scenarios, plus a showback design using gateway tags.

#### A19. Evaluation as owned infrastructure
**Duration**: 1 week | **Effort**: Medium

- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Anthropic, January 2026): capability vs regression suites, pass@k vs pass^k, grader calibration, evals owned like unit tests.
- [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) (Husain and Shankar, September 2026). You read it in Part 1 for technique. Reread for governance: ownership, budgets, release gates.

**Deliverable**: an org eval strategy (2–3 pages): eval tiers per release gate, dataset ownership, production sampling policy, judge calibration cadence.

#### A20. OpenTelemetry GenAI semantic conventions
**Duration**: 2 days | **Effort**: Low

[semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai) (CNCF, active as of October 2026). GenAI spans, agent spans, metrics, provider-specific and MCP conventions. A vendor-neutral telemetry contract is how an architect avoids observability lock-in. Pin a version, the spec still moves.

**Deliverable**: a one-page observability standard: required span attributes for every LLM, tool and agent call, PII redaction rules, retention, dashboards and SLOs.

---

### Stage 7 — Strategy, Leadership and Case Studies

#### A21. Microsoft Cloud Adoption Framework: AI adoption
**Duration**: 1 week | **Effort**: Medium

[Strategy](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/strategy) | [Plan](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/plan) | [Govern](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/govern) (all updated October 2026)

The AI decision tree (SaaS, then PaaS, then IaaS, guided by "least operational responsibility"), AI Center of Excellence, turning use cases into production plans, responsible-AI policies. The most current free executive-grade build-vs-buy framework. Abstract the Microsoft product names to SaaS, managed platform or self-host.

**Deliverable**: a three-page AI strategy memo for leadership: use-case portfolio, build/buy/partner decision for each, governance operating model, 12-month architecture runway. Present it as a 10-slide deck.

#### A22. Google: Rules of Machine Learning
**Duration**: 2 days | **Effort**: Low

[Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) by Martin Zinkevich. Rule 1: don't be afraid to launch without ML. Heuristics first, pipeline before sophistication. Classic predictive-ML content, but the best short text on *judgment*. Architects need to say "no" credibly.

**Deliverable**: add a "Could this be done without an LLM?" gate to your ADR template.

#### A23. Case-study libraries (ongoing)

- [Evidently AI: ML and LLM system design, 800 case studies](https://www.evidentlyai.com/ml-system-design)
- [ZenML LLMOps Database](https://www.zenml.io/llmops-database) (2,000+ entries, filter by industry or tech)

**Deliverable**: a monthly architecture teardown. Pick one case study, redraw its architecture, write the three ADRs you think they made, and what you would do differently.

---

### AI Architect: The Compressed Top 10

| # | Resource | Stage | Time |
|---|----------|-------|------|
| 1 | Kleppmann, Distributed Systems (Cambridge) | 1 | 2 wk |
| 2 | Azure WAF Architect role + ADR practice | 1 | 1 wk, then ongoing |
| 3 | Made With ML (or MLOps Zoomcamp) | 2 | 4 wk |
| 4 | Chip Huyen, Building a GenAI Platform | 3 | 1 wk |
| 5 | Agent orchestration patterns (Azure, Google, Anthropic) | 3 | 1.5 wk |
| 6 | AWS Generative AI Lens (or your cloud's equivalent) | 4 | 2 wk |
| 7 | OWASP LLM Top 10 + Agentic Top 10 | 5 | 1 wk |
| 8 | NIST AI RMF + Generative AI Profile | 5 | 1.5 wk |
| 9 | FinOps for AI | 6 | 0.5 wk |
| 10 | Microsoft CAF AI adoption | 7 | 1 wk |

Swap in by context: EU AI Act (A16) if you ship in or to the EU, the RAG design series (A8) for data-heavy orgs, evals as infrastructure (A19).

### AI Architect: Timeline

| Month | Stages | Capstone artifact |
|-------|--------|-------------------|
| 1 | 0–1 | Current-state diagram, ADR log started, consistency note |
| 2 | 2 | Platform design doc, maturity roadmap |
| 3 | 3 | Target GenAI platform reference architecture (gateway, RAG, agents) |
| 4 | 4–5 | Well-Architected review, threat model, risk register, EU AI Act memo |
| 5 | 6–7 | Cost model, eval strategy, observability standard, strategy memo and deck |
| ongoing | 7 | Monthly case-study teardown |

---

## What Was Rejected and Why

Some well-known resources did not make the cut. Knowing why saves you time.

- **Weights & Biases courses**: the evals course URL returns 404 and the courses page redirects to CoreWeave, which has no catalog.
- **Full Stack LLM Bootcamp**: April 2023. Predates tool calling, MCP and modern agents. The LLM Engineer roadmap already lists FSDL.
- **Stanford CS329S (ML Systems Design)**: last run 2022, pre-LLM.
- **a16z "Emerging Architectures for LLM Applications"**: a 2023 snapshot, historically interesting, stale.
- **AWS Cloud Adoption Framework for AI whitepaper**: the page now says "for historical reference only."
- **Anthropic `courses` repo**: archived September 2026, written for Claude 3. Replaced by Anthropic Academy.
- **DeepLearning.AI RAG course (Zain Hasan)** and **Husain/Shankar AI Evals course (Maven)**: excellent, paid. Their free material is in the roadmap instead.
- **Pinecone Learn**: no longer a structured series.
- **ISO/IEC 42001**: paywalled standard.
- **Hugging Face LLM course, DL.AI MCP/A2A/Agent Memory/vLLM courses**: already in the LLM Engineer roadmap.

---

## How This Roadmap Is Different

**What you're NOT doing**:
- ❌ Paying for anything except optional certificates and a few dollars of API credits
- ❌ Learning from listicles and "AI educator" YouTube channels
- ❌ Collecting framework tutorials without evals
- ❌ Reading 2023 architecture essays as if the field had not moved
- ❌ Treating security and governance as someone else's job

**What you ARE doing**:
- ✅ Learning from the vendors who build the models and the clouds that run them
- ✅ Treating evals as the job, from Stage 2 onward
- ✅ Growing one codebase across all eight engineer stages
- ✅ Producing architect artifacts (ADRs, threat models, cost models), not more code
- ✅ Reading primary sources for regulation and security

---

## The Outcome

After Part 1 you can ship LLM features against any major API with structured outputs and tools, design and evaluate RAG systems, build workflow-first agents and MCP servers, run error analysis and validated LLM judges, reason about cost, latency and OWASP-class risks, and self-host an open-weight model behind an OpenAI-compatible endpoint.

After Part 2 you have an ADR log, a reference architecture, a Well-Architected review and risk register, a threat model, a compliance memo, a cost model, an eval strategy, an observability standard and a strategy deck. That portfolio maps directly to what Microsoft's architect-role guidance and the AB-100 profile describe.

---

## Start Now

Engineer: open [Karpathy's Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI) today and enroll in [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api) while it is free.

Architect: draw your current-state diagram this week and write ADR-000.

---

## Key Takeaways

- **Two roles, one stack.** Engineer builds the components. Architect decides which exist, who owns them, what they cost and how they fail.
- **Evals are the job**, not a stage. They start in Stage 2 and never stop.
- **One growing codebase** beats ten toy projects.
- **Architects ship documents.** ADRs, threat models and cost models are the portfolio.
- **Primary sources only** for security and regulation. The EU AI Act dates moved in 2026. Summaries lie.
- **Enroll early.** DeepLearning.AI's free access is tied to its platform beta.
