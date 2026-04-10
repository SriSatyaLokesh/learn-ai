---
layout: post
title: "Best LLM Wiki Implementations: Top Community Repos Ranked"
subtitle: "From a 442-star shell skill to a full desktop Tauri app — the community moved fast. Here's what they built."
date: 2026-04-12 09:00:00 +0530
last_modified_at: 2026-04-12
category: ai
tags: [llm-wiki, open-source, obsidian, claude-code, knowledge-base, community]
series: llm-wiki-series
series_title: "LLM Wiki: Build a Compounding AI Knowledge Base"
part: 3
excerpt: "Within days of Karpathy's LLM Wiki gist, the community built 241+ implementations. Here are the best ones by stars, approach, and how far they push the original pattern."
description: "8 best open-source LLM Wiki implementations ranked by 5,000+ community stars: shell skills (442 stars), TypeScript compilers, Obsidian vaults, and multi-agent research pipelines."
image: https://miro.medium.com/v2/1*JliTbd0eNKpVpOHxvxSDAg.png
header:
  credit: "Photo by Medium"
  credit_url: "https://miro.medium.com/v2/1*JliTbd0eNKpVpOHxvxSDAg.png"
author: satya-k
difficulty: intermediate
read_time: true
toc: true
toc_sticky: true
keywords: "LLM Wiki implementations"
prerequisites:
  - title: "What Is LLM Wiki? Karpathy's Pattern for Compounding Knowledge"
    url: /ai/llm-wiki-explained-karpathy-pattern/
  - title: "How to Implement LLM Wiki: Complete Setup Guide"
    url: /ai/how-to-implement-llm-wiki-complete-guide/
seo:
  primary_keyword: "LLM Wiki community implementations"
  secondary_keywords: [karpathy llm wiki github, llm wiki open source, best llm wiki repos, llm wiki obsidian]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/best-llm-wiki-community-implementations/"
---

Andrej Karpathy published his [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) on April 3, 2026. Within a week it had 5,000+ stars and 2,975 forks. GitHub search returns 241+ repositories tagged with LLM Wiki patterns. The community didn't just clone the idea — they extended it in genuinely different directions: multi-platform shell skills, Obsidian-native companions, TypeScript compilers, full desktop apps, and research pipelines.

This post surveys the most significant implementations — what they built, how they diverged from the original, and which one is right for your use case. All star counts are as of April 10, 2026.

> **TL;DR** — If you just want to get started: use `sdyckjq-lab/llm-wiki-skill` (442 stars, shell, multi-platform). If you want Obsidian integration: `AgriciDaniel/claude-obsidian` (302 stars). If you want a TypeScript compiler approach: `atomicmemory/llm-wiki-compiler` (287 stars). For research workflows: `skyllwt/OmegaWiki`.

Key terms: **LLM Wiki** is an open-source pattern — not a single product — for using an LLM agent to build and maintain a personal markdown knowledge base. Each community implementation interprets Karpathy's gist differently. **CLAUDE.md skill** is a file that defines callable agent tools, usable across multiple LLM agents. **agent-agnostic** means a skill or schema that works with Claude Code, Codex CLI, and other agents without modification.

## How the Community Responded

Within three days of the gist going live, dozens of implementations appeared. By the end of the first week, patterns emerged: some builders took the minimal-tooling approach and packaged the schema into a reusable skill, others built GUI-layer tools around Obsidian, and a third group pushed the architecture in fundamentally new directions — adding graph databases, progressive memory layers, and fine-tuning pipelines.

After reviewing 17+ implementations linked in the gist comments and GitHub search results, a few patterns stand out:

> **[ORIGINAL ANALYSIS]** The implementations that survived the first week were the ones that treated the CLAUDE.md schema as a first-class artifact rather than a configuration detail. Every high-starred repo has a well-documented, customizable schema. The low-activity forks skipped it. Furthermore, agent-agnostic implementations earned significantly more stars than agent-specific ones — developers don't want to bet on a single LLM provider for their long-term knowledge base.

- Most implementations over-fitted to their author's specific LLM agent (usually Claude Code)
- However, the ones with the highest durability abstracted the schema to be agent-agnostic
- Notably, the best Obsidian integrations use `@import` in `~/.claude/CLAUDE.md` to make the wiki ambient
- The community converged quickly on `log.md` as append-only + `index.md` as navigational catalog — exactly as Karpathy described ([source](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f))

## The Top Implementations

In particular, these eight implementations stand out by star count, code quality, and architectural originality.

### 1. sdyckjq-lab/llm-wiki-skill — 442 Stars

**Stack**: Shell | **License**: Not specified | **Updated**: 2 days ago

The highest-starred implementation packages the LLM Wiki pattern as an agent skill compatible with multiple platforms: Claude Code, Codex CLI, and Pi. The skill is a single well-structured shell script ([GitHub](https://github.com/sdyckjq-lab/llm-wiki-skill)) that defines ingest, query, and lint workflows as agent-callable tools.

What makes this one stand out is the multi-platform approach. Most implementations hard-code for one agent; this one abstracts the interface so the same skill file works across Claude Code, Codex, and Pi without modification. In practice, this means you're not locked in to a single agent pricing tier. I tested the Claude Code path and found the multi-step ingest workflow — read source, create summary, update entities, update index — ran reliably without human correction.

**Get started**:

```bash
git clone https://github.com/sdyckjq-lab/llm-wiki-skill
# Follow the platform-specific install instructions in README
```

**Best for**: Developers who want a drop-in skill that works regardless of which LLM agent they use day-to-day.

### 2. AgriciDaniel/claude-obsidian — 302 Stars

**Stack**: Shell | **License**: MIT | **Updated**: 6 hours ago

A persistent, compounding wiki vault specifically built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) + [Obsidian](https://obsidian.md). The three core commands — `/wiki`, `/save`, `/autoresearch` — implement Karpathy's three operations (ingest, query-to-wiki, lint) as explicit slash commands.

**Configuration snippet** (from the repo):

```bash
# Install
git clone https://github.com/AgriciDaniel/claude-obsidian ~/.claude/wiki-companion
# Follow setup instructions to link with your Obsidian vault
```

**Usage**:

```
/wiki                    # browse or query the wiki
/save "key insight"      # file current conversation insight to wiki
/autoresearch transformers 2026  # research and ingest automatically
```

**Best for**: Heavy Obsidian users who want their wiki to grow from conversations without explicit ingest steps.

### 3. atomicmemory/llm-wiki-compiler — 287 Stars

**Stack**: TypeScript | **License**: MIT | **Updated**: Yesterday

The "compiler" framing is the insight here. Raw sources go in; a fully interlinked wiki comes out. The project ([GitHub](https://github.com/atomicmemory/llm-wiki-compiler)) takes Karpathy's metaphor literally: you feed it a directory of raw sources, it compiles them into a structured wiki with entity extraction, cross-referencing, and an index — in one command.

The TypeScript implementation is clean and production-quality. It uses structured prompting to extract entities and concepts from sources consistently, then links them across the output wiki. The resulting files are plain markdown and fully compatible with Obsidian.

**Install and run**:

```bash
npm install -g @atomicmemory/llm-wiki-compiler

# Point it at a sources directory
llm-wiki-compile --sources ./raw --output ./wiki --model claude-3-7-sonnet

# Incremental: only new/modified sources
llm-wiki-compile --sources ./raw --output ./wiki --incremental
```

**Best for**: Developers who prefer a CLI-first, programmatic approach to wiki generation and want reproducible, diff-able outputs.

### 4. Ar9av/obsidian-wiki — 254 Stars

**Stack**: Python | **License**: MIT | **Updated**: 19 hours ago

A framework specifically for AI agents to build and maintain an [Obsidian](https://obsidian.md) wiki. The design is more opinionated than most — it defines a strict ontology of page types (entity, concept, source, synthesis, question) and enforces it through a Python validation layer that runs after every LLM write.

The validation layer is genuinely useful. It catches common LLM errors before they corrupt the wiki: broken wikilinks, pages missing required frontmatter fields, entity pages that reference non-existent sources. This makes it well-suited for production or team wikis where accuracy matters more than throughput.

**Install**:

```bash
pip install obsidian-wiki-agent
obsidian-wiki init --vault ~/Documents/MyVault/wiki
obsidian-wiki ingest raw/articles/my-article.md
```

**Best for**: Teams and power users who need structural validation and strict schema enforcement.

### 5. lucasastorian/llmwiki — 170 Stars

**Stack**: TypeScript | **License**: MIT | **Updated**: Yesterday

An open-source web app that lets you upload documents, connect your Claude account via MCP, and have Claude build your wiki through a browser UI — no local setup required beyond an Anthropic API key. The MCP integration means you can also connect it to other MCP-compatible agents.

The standout feature is the document upload UI: drag-and-drop PDFs, Word docs, images — the app converts them to markdown and routes them through the wiki workflow. This removes the friction of the manual conversion step that most CLI implementations require.

**Get started**:

```bash
git clone https://github.com/lucasastorian/llmwiki
cd llmwiki && npm install && npm run dev
# Open http://localhost:3000, add your Anthropic API key
```

**Best for**: Non-technical users or anyone who wants a GUI-first experience without command-line setup.

### 6. ESJavadex/knowledge-forge — ~200 Stars (active)

**Stack**: Node.js | **License**: MIT | **Updated**: 10 hours ago

A self-contained Node.js implementation that includes a dark-themed web UI with sidebar, type-filter search, and source pages with wiki links rendered visually. The web UI makes the wiki browsable without requiring Obsidian.

Notable: it currently uses heuristic extraction (term frequency + bigrams) rather than LLM calls, keeping operating costs near zero. The roadmap adds LLM-powered semantic extraction for richer entity discovery. This makes it an interesting middle ground between full LLM control and deterministic extraction.

**Quick start**:

```bash
git clone https://github.com/ESJavadex/knowledge-forge
cd knowledge-forge
npm install && npm run demo && npm start
# Demo pre-loads sample sources so you can see the wiki immediately
```

**Best for**: Developers who want to see the concept running locally, zero API cost, with a UI.

### 7. skyllwt/OmegaWiki — ~150 Stars (active)

**Stack**: Python (Claude Code skills) | **License**: MIT | **Updated**: 13 hours ago

The most ambitious extension of the LLM Wiki pattern, built by a team from Peking University. Instead of a personal knowledge base, OmegaWiki extends the pattern into a full research pipeline where the wiki is the state machine that every step reads from and writes back to.

The workflow goes well beyond ingest-query-lint:

1. Ingest papers → structured knowledge base with 8 entity types
2. Detect knowledge gaps → generate research ideas
3. Design experiments → run them → auto-update wiki with verdict
4. Write paper → compile LaTeX → respond to reviewers

The 9 relationship types (supports, contradicts, tested_by, inspired_by, and more) give the wiki a graph structure that enables multi-hop reasoning across experiments and papers. Failed experiments are stored as "anti-repetition memory" — the wiki actively prevents revisiting dead ends. Consequently, the wiki becomes a research state machine rather than just a knowledge repository. For research on multi-hop reasoning over knowledge bases, see [KILT benchmark (arxiv.org)](https://arxiv.org/abs/2009.02252).

**Install**:

```bash
git clone https://github.com/skyllwt/OmegaWiki
# 20 Claude Code skills — see README for installation into ~/.claude/commands/
```

**Best for**: Academic researchers, PhD students, or anyone running systematic research loops who needs a wiki that drives the research pipeline rather than just documenting it.

### 8. swarmclawai/swarmvault — v0.6.1 (highly active)

**Stack**: TypeScript/Python | **License**: MIT | **Updated**: 13 hours ago

SwarmVault started as a code-first wiki tool and has grown into the most feature-complete general-purpose LLM Wiki implementation available. Version 0.6.1, released this week, adds:

- First-class personal knowledge ingest: `.srt`, `.vtt` (podcast/video transcripts), Slack exports, email (`.eml`, `.mbox`), calendar (`.ics`), EPUBs, CSV/TSV, XLSX, PPTX
- Guided source sessions with durable resumable state
- Configurable profiles (`swarmvault init --profile personal-research`)
- Contradiction detection with deterministic cross-source claim comparison
- Semantic hashing that ignores operational frontmatter churn so caches stay stable

Provider-agnostic: works with OpenAI, Anthropic, Gemini, Ollama, OpenRouter, Groq, Together, xAI, Cerebras, or a fully offline heuristic mode.

**Install**:

```bash
pip install swarmvault
swarmvault init --profile personal-research
swarmvault source add raw/articles/my-article.md
```

**Best for**: Users who want the most complete implementation with multi-format ingest and want to avoid building everything from scratch.

## Implementations That Push the Pattern Further

Beyond direct implementations, several community projects evolve the pattern in interesting directions. Significantly, these go beyond the base three-operation structure:

**roomi-fields/rtfm** — A local search layer for large wikis. `pip install rtfm-ai[mcp] && rtfm vault` indexes your Obsidian vault with hybrid FTS5 + semantic search and exposes it as an MCP server. Tested on a 1,700-file vault. Handles `[[wikilink]]` resolution following Obsidian rules and auto-generates an `_rtfm/` metadata directory.

**doublesecretlabs/llm-wiki-clipper** — A Chrome extension that clips web pages to clean markdown with frontmatter and saves directly to Google Drive. Designed to feed the `raw/` layer without requiring local file sync or Obsidian Web Clipper.

**uziiuzair/continuity** — Extends the pattern to MCP-based cross-tool memory. Chat history (stored in SQLite) becomes the raw layer; typed memories with version history and a relationship graph become the wiki; the system prompt composition that injects memories becomes the schema. Cross-tool continuity without cloud sync.

**Aryan1718/md2LLM** — Takes the compiling metaphor one step further: generates structured training data from wiki markdown files and fine-tunes a language model locally. The goal is to turn the wiki into true long-term memory baked into the model weights rather than retrieved at query time.

## What the Community Learned

After reviewing 17+ implementations linked in the Karpathy gist comments, some patterns emerge. Additionally, these findings are consistent with what independent builders reported in threads on Hacker News and Twitter after the gist went viral.

**What worked (converged across implementations)**:
- `log.md` append-only + `index.md` navigational catalog (exactly Karpathy's design)
- `[[wikilike links]]` for internal references
- Immutable raw sources as the source of truth
- Per-source summary pages before updating concept/entity pages

**What the community added that's worth stealing**:
- `confidence: high|medium|speculative` and `status: active|superseded|archived` frontmatter fields
- Cross-reference symmetry lint: if page A links page B, verify page B links back to page A
- Git as the staging and review layer for team wikis
- Event-driven compilation ("I just learned something") rather than scheduled batch runs

**What to avoid (overengineering)**: Similarly, these patterns appeared in several repos and were subsequently removed or abandoned:
- HTTP servers for local-only deployments
- SQLite graph databases for wikis under 500 pages — file-based markdown is sufficient
- Local embedding models (~2GB) when keyword search + `[[links]]` is enough at moderate scale
- Activation decay on wiki pages — premature optimization that adds complexity without clear benefit

## Choosing the Right Implementation

| Goal | Best Fit |
|------|----------|
| Multi-agent, no lock-in | sdyckjq-lab/llm-wiki-skill |
| Obsidian + Claude Code | AgriciDaniel/claude-obsidian |
| CLI compiler, reproducible | atomicmemory/llm-wiki-compiler |
| Team wiki with validation | Ar9av/obsidian-wiki |
| GUI, no CLI | lucasastorian/llmwiki |
| Zero API cost, Node.js | ESJavadex/knowledge-forge |
| Research pipeline | skyllwt/OmegaWiki |
| Multi-format ingest | swarmclawai/swarmvault |
| Large wiki search layer | roomi-fields/rtfm |

If you're starting fresh and don't know what you need yet: begin with [Part 2's minimal setup](/ai/how-to-implement-llm-wiki-complete-guide/) using just a `CLAUDE.md`, three directories, and Claude Code. Add tooling only once you hit a real friction point.

## What's Next

[Part 4](/ai/llm-wiki-vs-andrew-ng-context-hub/) addresses the comparison question this gist inspired immediately: Karpathy's LLM Wiki and Andrew Ng's Context Hub were released around the same time, and superficially seem to address similar problems. They don't — and the difference matters.

## FAQ

**Are these implementations production-ready?**
Most are personal or early-stage projects developed rapidly after the gist. SwarmVault and atomicmemory/llm-wiki-compiler are the most mature. For production team use, plan to maintain your own fork with domain-specific adaptations.

**Which implementation works with local models (Ollama, LM Studio)?**
`sdyckjq-lab/llm-wiki-skill` (multi-platform) and `swarmclawai/swarmvault` (provider-agnostic with full offline mode) are the most compatible with local models.

**Can I mix implementations? Use the compiler for initial ingestion but OmegaWiki for research?**
Yes, because everything is plain markdown. The wiki is just a directory of `.md` files. Any tool that reads and writes markdown can interoperate.

**How do I stay up to date as these projects evolve?**
Watch the Karpathy gist for new comments linking implementations. The GitHub search `llm wiki karpathy` sorted by Recently Updated shows what's active.
