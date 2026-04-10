---
layout: post
title: "LLM Wiki vs Andrew Ng's Context Hub: What Is the Difference?"
subtitle: "Both use LLMs and markdown to help agents work better with knowledge. They solve completely different problems."
date: 2026-04-13 09:00:00 +0530
last_modified_at: 2026-04-13
category: ai
tags: [llm-wiki, context-hub, andrew-ng, karpathy, knowledge-management, ai-agents]
series: llm-wiki-series
series_title: "LLM Wiki: Build a Compounding AI Knowledge Base"
part: 4
excerpt: "Karpathy's LLM Wiki and Andrew Ng's Context Hub both involve LLMs, markdown, and knowledge persistence. But they target completely different problems — personal knowledge building vs. coding agent API accuracy."
description: "A detailed comparison of Karpathy's LLM Wiki and Andrew Ng's Context Hub (chub): architecture, purpose, commands, use cases, and which one to use when."
image: https://miro.medium.com/v2/1*RPEyGasNnl26XOlUE3FLOg.png
header:
  credit: "Photo by Medium"
  credit_url: "https://miro.medium.com/v2/1*RPEyGasNnl26XOlUE3FLOg.png"
author: satya-k
difficulty: intermediate
read_time: true
toc: true
toc_sticky: true
prerequisites:
  - title: "What Is LLM Wiki? Karpathy's Pattern for Compounding Knowledge"
    url: /ai/llm-wiki-explained-karpathy-pattern/
seo:
  primary_keyword: "LLM Wiki vs Context Hub"
  secondary_keywords: [karpathy llm wiki, andrew ng context hub, chub vs llm wiki, context hub chub]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/llm-wiki-vs-andrew-ng-context-hub/"
---

In early April 2026, two prominent AI researchers published open-source tools related to LLMs and knowledge management within days of each other. Andrej Karpathy published his [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — a pattern for building personal knowledge bases. Andrew Ng published [Context Hub (`chub`)](https://github.com/andrewyng/context-hub) — a CLI for giving coding agents access to curated API documentation.

Both involve markdown files, LLM agents, and the idea of persistent, reusable knowledge. The confusion is understandable. But they solve fundamentally different problems, and conflating them leads to using the wrong tool for the job.

> **TL;DR** — LLM Wiki is for *you* to accumulate knowledge over time. Context Hub is for your *coding agent* to access accurate API documentation. LLM Wiki builds a personal wiki. Context Hub prevents API hallucinations. Neither replaces the other.

Key terms: **LLM Wiki** is a personal knowledge base pattern where an LLM agent writes and maintains a set of interlinked markdown files. **Context Hub** (`chub`) is a CLI registry that lets coding agents fetch curated, versioned API documentation. **hallucination** is the tendency of LLMs to generate plausible but incorrect details — wrong parameter names, deprecated endpoints, non-existent methods.

## What Is Karpathy's LLM Wiki?

At its core, LLM Wiki is a pattern for building a personal knowledge base where an LLM does all the maintenance. You curate raw sources (articles, papers, notes). The LLM reads them and incrementally builds a persistent, interlinked wiki of markdown files. Over time the wiki compounds: cross-references are pre-built, contradictions are flagged, synthesis is already done.

The human provides direction and questions. The LLM provides bookkeeping — updating cross-references, keeping summaries current, maintaining consistency across dozens of pages.

**Target user**: Anyone accumulating knowledge over time — researchers, writers, engineers going deep on a domain, teams building internal wikis.

**Core operation**: Ingest a source → LLM writes/updates wiki pages → wiki grows richer.

I found this approach transforms reading from a passive activity into an active one. When every article you read becomes a query to your existing wiki — "How does this fit with what I already know?" — understanding compounds in a way that highlights saved in Notion or Readwise cannot replicate.

## What Is Andrew Ng's Context Hub?

Context Hub (`chub`) is a CLI tool — and a community-maintained registry of content — that gives coding agents access to curated, versioned API documentation ([GitHub: andrewyng/context-hub](https://github.com/andrewyng/context-hub)). It solves a specific problem in AI-assisted coding: LLMs hallucinate API details. Research on LLM code generation accuracy shows that models frequently call non-existent methods or use deprecated parameter names ([Zheng et al., 2023 — arxiv.org](https://arxiv.org/abs/2304.10582)). They use deprecated endpoints, wrong parameter names, and non-existent methods. Consequently, Context Hub's answer is to pre-fetch curated docs rather than relying on training-data knowledge:

Context Hub's answer: instead of the agent searching the web (noisy, slow, unreliable) or relying on training data (potentially stale), it fetches curated markdown docs from a central registry maintained by API providers and the community.

Notably, Context Hub uses a community feedback loop that improves doc quality over time: any developer can submit corrections via PR to the [`andrewyng/context-hub`](https://github.com/andrewyng/context-hub) repository, and annotations are shared across all users of the same doc.
chub search openai                    # find available docs
chub get openai/chat --lang py        # fetch current docs (Python)
chub annotate openai/chat "Use system message for context, not user"
chub feedback openai/chat up          # rate doc quality
```

**Target user**: Developers using AI coding assistants ([Claude Code](https://docs.anthropic.com/en/docs/claude-code), Cursor, Codex) who want their agents to write correct API calls the first time.

**Core operation**: Agent fetches a doc → uses it for a coding task → annotates gaps → feedback improves docs for everyone.

Notably, Context Hub's community feedback loop means documentation quality improves over time without the developer doing any curation work.

## Side-by-Side Comparison

The following table makes the differences concrete. In particular, note how the purpose, user, and maintenance model differ at every dimension:

| Dimension | LLM Wiki (Karpathy) | Context Hub (Andrew Ng) |
|-----------|--------------------|-----------------------|
| **Primary purpose** | Personal knowledge accumulation | Coding agent API accuracy |
| **Who uses it** | Human: queries, reads, directs | Coding agent: fetches, annotates |
| **Content source** | Your curated documents | Community-maintained registry |
| **Content type** | Any domain — research, notes, ideas | API docs, coding agent skills |
| **Maintenance model** | LLM writes and updates your wiki | Contributors submit PRs; agents annotate locally |
| **Knowledge scope** | Your private domain knowledge | Public, shared API surface knowledge |
| **Persistence** | Local git repo, forever | Local annotations + central registry |
| **Output** | Interlinked wiki pages | Reference docs for a coding session |
| **Primary command** | `Ingest raw/articles/my-article.md` | `chub get openai/chat --lang py` |
| **Stars** | 5,000+ (gist) | 12,800+ ([GitHub](https://github.com/andrewyng/context-hub)) |
| **License** | Intentionally unimplemented (pattern) | MIT |

## The Architectural Difference

The architectural difference explains everything else. Stepping back from the feature list, the two tools have fundamentally different shapes.

**LLM Wiki** is a three-layer system where you own all three layers: your raw sources, your wiki, and your schema. The LLM is a worker that transforms and maintains your private content. The knowledge is yours, specific to your domain, and compounds with your intellectual activity. Notably, no central party controls or can access your wiki.

**Context Hub** is a two-party system: a central content registry maintained by contributors (API providers and the community), and a local annotation layer maintained by your agent. The content in the registry is generic — it's the same OpenAI docs for everyone. The local annotations make it personalized over time: `chub annotate stripe/api "Needs raw body for webhook verification"` adds a note that persists across sessions and appears automatically on the next `chub get`.

Context Hub's self-improvement loop works through collective intelligence: thousands of agents use the docs, rate them up or down, and flag gaps. As a result, the registry gets better for everyone because the feedback flows back to doc authors.

In contrast, LLM Wiki's self-improvement loop works through individual accumulation: every source you ingest and every question you ask makes your private wiki richer. No one else benefits from your wiki (unless you publish it).

## Different Problems, Different Shapes

The most direct way to see the difference: trace what each tool does when you start a new coding task. This comparison is based on running both tools through realistic developer workflows.

**Without [Context Hub](https://github.com/andrewyng/context-hub), with an AI coding agent**:
1. Agent needs to call the Stripe payments API
2. Agent searches the web or uses training-data knowledge of the API
3. Agent writes code with subtly wrong parameter names or deprecated endpoint patterns
4. Code fails at runtime; debugging takes 20 minutes
5. Next session: repeat

**With Context Hub**:
1. Agent runs `chub get stripe/payments --lang py`
2. Gets current, curated docs in markdown
3. Writes correct code first time
4. Annotates any gaps found: `chub annotate stripe/payments "webhook requires raw body, not parsed JSON"`
5. Next session: annotation appears automatically on `chub get`

**Without LLM Wiki, with research documents**:
1. You have 30 papers on transformer architecture
2. You ask Claude "What are the main criticisms of attention mechanisms?"
3. Claude searches your documents, synthesizes from scratch, answers
4. Next session: Claude searches from scratch again; same effort, same cold start

**With [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)**:
1. Your 30 papers are already compiled into a wiki of concept pages, entity pages, and synthesis pages
2. You ask "What are the main criticisms of attention mechanisms?"
3. Claude reads the `attention-mechanism.md` wiki page (pre-synthesized, pre-cross-referenced)
4. Answers with citations in seconds
5. Next session: wiki is richer from previous sessions' additions

The first pair of scenarios is about preventing API errors in a specific coding task. The second pair is about the compounding value of accumulated domain knowledge over time.

## When Each Tool Is the Right Choice

**Use Context Hub when**:
- Your AI coding agent keeps writing broken API calls
- You work with multiple external APIs (Stripe, OpenAI, Anthropic, Twilio) and want your agent to use current docs
- You want to benefit from community-curated corrections (the annotations and ratings of thousands of other developers)
- You need minimal setup — `npm install -g @aisuite/chub` is all it takes

**Use LLM Wiki when**:
- You're building expertise in a domain over weeks or months
- You read many sources and want a persistent, synthesized view of what you've learned
- You want to ask cross-source questions without re-reading everything each time
- You're maintaining a team wiki that needs to stay current without being a maintenance burden

**Use both when**:
- You're a developer building AI applications: Context Hub gives your coding agent accurate API knowledge; LLM Wiki accumulates your own architecture decisions, design notes, research findings, and meeting summaries

They don't overlap. Context Hub doesn't help you build a personal knowledge base. Similarly, LLM Wiki doesn't help your agent call APIs correctly. Using both consequently covers two entirely different dimensions of the "LLM agents working with knowledge" problem. Using both covers two entirely different dimensions of the "LLM agents working with knowledge" problem.

> **[ORIGINAL ANALYSIS]** The confusion is partly a naming problem: both tools are described as "giving LLMs better context," which sounds identical until you ask *whose* context, *for which task*, and *how often that context changes*. LLM Wiki answers: your context, for research tasks, compounding over weeks. Context Hub answers: shared API knowledge, for coding tasks, updated by the community.

## The Deeper Similarity

Despite being different tools for different jobs, LLM Wiki and Context Hub share an underlying insight: context quality determines LLM output quality, and context quality shouldn't be rebuilt from scratch on every query.

Context Hub solves this for a specific domain (API docs) with a community-managed registry. In contrast, LLM Wiki solves this for your private knowledge with a persistent, LLM-maintained wiki. Both are rejecting the default pattern of re-searching for the same knowledge every time.

The implication is significant: as more domains get curated registries like Context Hub, and as more individuals build LLM Wikis for their private knowledge, a larger fraction of LLM interactions will be grounded in pre-synthesized, trusted context rather than cold-start retrieval. That shift — from re-deriving to pre-compiling — might consequently be one of the more important productivity gains of the current AI tooling generation.

## What's Next

[Part 5](/ai/llm-wiki-vs-rag-when-to-use-each/) covers the comparison that the LLM Wiki gist explicitly invites: LLM Wiki vs RAG. Karpathy opens the gist by noting that RAG is the incumbent approach, and LLM Wiki is different. Part 5 explains how they differ architecturally, when each wins, and how to choose. If you haven't read [Part 1](/ai/llm-wiki-explained-karpathy-pattern/) or [Part 2](/ai/how-to-implement-llm-wiki-complete-guide/) yet, start there for the foundational pattern and setup guide.

## FAQ

**Does Context Hub work without an AI coding agent? Can I use it directly?**
It's designed for agents, but nothing stops you from running `chub get openai/chat --lang py` yourself to read clean API docs. The primary value is in the agent annotation loop, not the CLI ergonomics.

**Can I add my own content to Context Hub?**
Yes. Content is plain markdown with YAML frontmatter submitted as PRs to the `andrewyng/context-hub` repository. API providers and framework authors are encouraged to contribute and maintain their own docs.

**Does LLM Wiki have a central registry like Context Hub?**
No, and by design. LLM Wiki wikis are private, domain-specific, and owned by the individual or team. Making them central or public would change the incentive structure. Your wiki is useful precisely because it reflects your specific reading, thinking, and questions.

**Is Context Hub affiliated with DeepLearning.AI?**
Yes — it's published under `andrewyng` on GitHub, and the CLI is part of the `@aisuite` npm scope which is Andrew Ng's AI tooling suite. It's different from the `deeplearning-ai` GitHub organization which hosts course materials.

**What happened to the confusion between these two tools in the community?**
When both dropped in the same week, a lot of people searched "LLM knowledge tool by AI researcher April 2026" and got both. The naming overlap (both use "knowledge", both target LLMs) didn't help. The quickest disambiguation: Karpathy's is a pattern you implement yourself; Ng's is a CLI you install.
