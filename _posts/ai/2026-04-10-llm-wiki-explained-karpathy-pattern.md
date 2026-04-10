---
layout: post
title: "What Is LLM Wiki? Karpathy's Compounding Knowledge Pattern"
subtitle: "How a single GitHub Gist quietly changed the way developers think about personal knowledge management"
date: 2026-04-10 09:00:00 +0530
last_modified_at: 2026-04-10
category: ai
tags: [llm-wiki, karpathy, knowledge-base, rag, obsidian, ai-agents]
series: llm-wiki-series
series_title: "LLM Wiki: Build a Compounding AI Knowledge Base"
part: 1
excerpt: "Andrej Karpathy's LLM Wiki is not a tool — it's a pattern. Instead of asking an LLM to search your files on every question, you let it build and maintain a persistent, interlinked wiki that compounds over time."
description: "Understand Karpathy's LLM Wiki pattern: what it is, the core idea behind it, its three-layer architecture, and why it outperforms RAG for long-term knowledge building."
image: https://cdn.analyticsvidhya.com/wp-content/uploads/2026/04/Karapathy-LLM-Wiki.webp
header:
  image_credit: "Photo by analyticsvidhya.com"
  image_credit_url: "https://analyticsvidhya.com"
author: satya-k
difficulty: intermediate
read_time: true
toc: true
toc_sticky: true
prerequisites:
  - title: "What is RAG? Retrieval-Augmented Generation Explained"
    url: /ai/what-is-rag/
seo:
  primary_keyword: "LLM Wiki Karpathy"
  secondary_keywords: [karpathy llm wiki, personal knowledge base llm, llm wiki pattern, compounding knowledge base]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/llm-wiki-explained-karpathy-pattern/"
---

On April 3, 2026, Andrej Karpathy — Tesla's former AI director and OpenAI cofounder — published [a short GitHub Gist titled "LLM Wiki"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Within days it earned 5,000+ stars and sparked 241+ community implementations. It didn't introduce a new model or framework. It described a pattern. **LLM Wiki** is a methodology where an LLM builds and maintains a persistent, interlinked knowledge base from your raw sources — compounding over time in a way that standard retrieval never can. Let's unpack why that distinction matters.

This post explains what LLM Wiki is, the problem it solves, the architecture behind it, and why it matters for anyone who accumulates knowledge with AI tools.

> **TL;DR** — LLM Wiki is a three-layer pattern where an LLM incrementally builds and maintains a persistent markdown wiki from your raw sources. Unlike RAG (which re-derives knowledge from scratch on every query), the wiki compounds over time. You read it; the LLM writes it.

I've been testing this pattern since the gist went live, and what surprised me most was the query quality difference. When I first ingested 10 sources into a wiki and then asked multi-hop questions, the answers were noticeably better than asking the same LLM to search those 10 files directly. The compiled wiki layer genuinely matters. In my experience, even a small wiki of 15–20 pages delivers synthesis that would take several minutes of back-and-forth to reconstruct with raw RAG.

## What Problem Does LLM Wiki Solve?

Most developers and researchers working with LLMs hit the same wall eventually. You have documents — papers, articles, meeting notes, podcast transcripts. You upload them to [ChatGPT](https://chatgpt.com) or [NotebookLM](https://notebooklm.google.com/). You ask questions. The LLM searches, reads, and answers. Then a week later you ask a follow-up. It searches again. Reads again. Starts over.

Every query is a cold start. As a result, there is no accumulation.

Karpathy describes this as the core limitation of standard RAG: "the LLM is rediscovering knowledge from scratch on every question. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up."

The consequences become painful as your knowledge base grows:

- Multi-document synthesis requires the LLM to find and connect fragments manually on every query
- Contradictions between sources are never flagged — you discover them by accident
- The time cost of a good answer grows linearly with the number of documents
- Context windows limit how much can be analyzed in a single pass

LLM Wiki addresses this by making the compilation step happen once per source, not once per query.

## The Core Idea: Compile Knowledge, Don't Re-Derive It

The insight is straightforward once stated: treat knowledge like code. You don't re-run all your source files on every execution. You compile them once into an artifact — an executable, a bundle, a binary — and then run the artifact.

LLM Wiki applies the same logic to documents. When you add a new source, the LLM doesn't just index it for retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims.

As a result, the wiki becomes a persistent, already-synthesized artifact. Cross-references are already there. Contradictions have already been flagged. When you query, the LLM reads the wiki — a compact, structured artifact — rather than raw source files that are scattered, redundant, and unstructured.

This is the compounding effect: every source you add and every question you ask makes the wiki richer. A wiki you have maintained for three months is dramatically more useful than one created yesterday, because it has absorbed your evolving mental model, not just a pile of files.

## The Three-Layer Architecture

Karpathy defines three layers, each with a distinct role:

### Layer 1: Raw Sources

Your curated collection of source documents — articles, papers, images, data files, podcast transcripts, meeting notes. These are **immutable**. The LLM reads from them but never modifies them. This is your source of truth and your audit trail.

```
raw/
├── papers/
│   ├── attention-is-all-you-need.pdf
│   └── gpt4-technical-report.pdf
├── articles/
│   ├── 2026-03-karpathy-vibe-coding.md
│   └── anthropic-constitutional-ai.md
└── notes/
    └── team-meeting-2026-04-01.md
```

Notably, the immutability is important. If the LLM makes a synthesis error in the wiki, you always have the ground truth to compare against and correct from.

### Layer 2: The Wiki

A directory of LLM-generated markdown files — summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely: it creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent.

```
wiki/
├── index.md          ← navigational catalog of all pages
├── log.md            ← append-only operation history
├── concepts/
│   ├── attention-mechanism.md
│   └── reinforcement-learning.md
├── entities/
│   ├── openai.md
│   └── anthropic.md
└── synthesis/
    └── transformer-evolution.md
```

You read it; the LLM writes it. This division of labor is the key design choice. Humans are excellent curators, questioners, and thinkers. LLMs are excellent bookkeepers — they don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass.

### Layer 3: The Schema

A configuration document — `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex, `SYSTEM.md` for others — that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or running a lint pass.

Notably, this is the least obvious layer but arguably the most important. The schema is what transforms a generic LLM into a disciplined wiki maintainer. It defines:

- Directory structure conventions
- Page format templates for entities, concepts, summaries
- How to update `index.md` on every ingest
- How to handle contradictions between sources
- What constitutes a lint pass (orphan pages, stale claims, missing cross-references)

The schema evolves alongside the wiki. Early on it is minimal. As you discover what works for your domain, you add conventions collaboratively with the LLM.

## How Operations Work

### Ingest

You drop a new source into the raw collection and instruct the LLM to process it. A full ingest flow:

1. LLM reads the source
2. Discusses key takeaways with you (optional but recommended)
3. Writes a summary page in the wiki
4. Updates `index.md`
5. Updates relevant entity and concept pages across the wiki
6. Appends an entry to `log.md`

A single source might touch 10–15 wiki pages. The human stays involved — reviewing summaries, checking updates, directing emphasis. Or you batch-ingest many sources with minimal supervision. The schema defines whichever workflow you prefer.

### Query

You ask questions against the wiki. The LLM reads `index.md` to find relevant pages, drills into them, and synthesizes an answer with citations. Answers can take different forms: a markdown page, a comparison table, a Marp slide deck, a matplotlib chart.

Furthermore, the critical insight Karpathy adds: good answers should be filed back into the wiki as new pages. A comparison you asked for, an analysis you commissioned, a connection you discovered — these are valuable artifacts that shouldn't disappear into chat history. Your explorations compound the knowledge base just like ingested sources do.

### Lint

Periodically, ask the LLM to health-check the wiki. Look for contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references. The LLM is good at surfacing new questions to investigate and new sources to find.

## The Two Navigation Files

Additionally, two special files let the LLM navigate the wiki as it grows without needing embeddings infrastructure:

**`index.md`** is content-oriented. A catalog of every page with a one-line summary and optional metadata. When answering a query, the LLM reads the index first (low token cost) to identify relevant pages, then drills in. This works reliably at moderate scale — around 100 sources and hundreds of pages.

**`log.md`** is chronological. An append-only record of every ingest, query, and lint pass with timestamps. If each entry starts with a consistent prefix (e.g., `## [2026-04-02] ingest | Article Title`), the log becomes grep-able from the command line:

```bash
grep "^## \[" log.md | tail -5    # last 5 operations
grep "ingest" log.md | wc -l      # total sources ingested
```

The log gives the LLM temporal context — what has been done recently, which sources were ingested together, what questions led to which wiki pages.

## Why This Works (And Why Humans Abandoned Wikis Before)

Karpathy's diagnosis of why personal wikis always fail is sharp: "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value."

LLMs, however, remove that bottleneck. In practice, when you run your first ingest against 5–10 sources, the improvement is immediate — answers that previously required re-reading five documents now come from a pre-synthesized concept page the LLM built during ingestion. They don't get bored. They don't forget to update a cross-reference. They can touch 15 files in a single pass with no cognitive overhead. The wiki stays maintained because the cost of maintenance is near zero.

Additionally, the human's job becomes what humans are actually good at: curating sources, directing analysis, asking insightful questions, and thinking about what it all means.

Karpathy connects this to [Vannevar Bush's 1945 Memex vision](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/) — a personal, curated knowledge store with associative trails between documents. "Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that."

## Where LLM Wiki Fits

The pattern applies to a surprisingly wide range of contexts:

**Personal knowledge**: tracking health, goals, psychology, self-improvement — feeding journal entries, articles, podcast notes, building a structured picture of yourself over time.

**Deep research**: going deep on a topic over weeks or months — reading papers and incrementally building a comprehensive wiki with an evolving synthesis and thesis.

**Reading alongside a book**: filing each chapter as you go, building pages for characters, themes, plot threads, and how they connect. Think fan wikis like Tolkien Gateway — thousands of interlinked pages covering characters, places, events — built by one person with an LLM doing all the cross-referencing.

**Business and team wikis**: fed by Slack threads, meeting transcripts, project documents, customer calls. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.

**Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — any domain where you're accumulating knowledge over time and want it organized rather than scattered.

## What LLM Wiki Is Not

Importantly, it is not a specific tool, app, or library. The original gist is intentionally abstract. It describes the pattern; your LLM agent and your domain requirements determine the implementation.

Similarly, it is not a replacement for search engines or general-purpose RAG systems. If you need to search a corpus of thousands of documents you don't own, or answer one-off questions against a document library, RAG is still the right approach. LLM Wiki is for knowledge you're actively building and updating over time.

Additionally, it is not fully automated. The human remains the curator — deciding which sources are worth ingesting, guiding the emphasis during ingestion, asking the right questions, reviewing the outputs. The LLM does the grunt work, but the human provides the direction.

## The Toolchain

Karpathy's recommended setup is minimal on purpose:

- **[Obsidian](https://obsidian.md/)** as the wiki viewer/IDE — Obsidian's graph view visualizes which pages link to which, showing you what's connected, what's isolated, and which pages are hubs. The LLM makes edits; you browse the results in real time.
- **[qmd](https://github.com/tobi/qmd)** (optional) as a local search engine over the wiki — hybrid BM25/vector search, all on-device, with both a CLI and MCP server so the LLM can search directly.
- **[Obsidian Web Clipper](https://obsidian.md/clipper)** (optional) as a browser extension for converting web articles to markdown and dropping them directly into the raw sources folder.
- **Any LLM agent with file-system access** — [Claude Code](https://docs.anthropic.com/en/docs/claude-code), OpenAI Codex, or any agentic interface that can read and write markdown.

The wiki is just a git repository of markdown files. You get version history, branching, and collaboration for free, with no special database or infrastructure.

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "What Is LLM Wiki? Karpathy's Compounding Knowledge Pattern",
      "description": "Understand Karpathy's LLM Wiki pattern: what it is, the core idea behind it, its three-layer architecture, and why it outperforms RAG for long-term knowledge building.",
      "datePublished": "2026-04-10",
      "dateModified": "2026-04-10",
      "author": {
        "@type": "Person",
        "name": "Satya K",
        "url": "https://srisatyalokesh.is-a.dev/learn-ai/authors/satya-k/"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Learn with Satya K"
      },
      "image": "https://srisatyalokesh.is-a.dev/learn-ai/assets/images/posts/llm-wiki-explained/hero.jpg",
      "mainEntityOfPage": "https://srisatyalokesh.is-a.dev/learn-ai/llm-wiki-explained-karpathy-pattern/"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Does LLM Wiki replace RAG?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. RAG is better for large, mostly-static corpora you don't own. LLM Wiki is better when you're actively building and curating knowledge over time, because the wiki compounds with every source ingested."
          }
        },
        {
          "@type": "Question",
          "name": "Do I need a specific LLM to implement the LLM Wiki pattern?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. The pattern works with any LLM agent that has file-system access including Claude Code, Codex, and open-source models. The schema document you write is what makes the LLM behave as a disciplined wiki maintainer."
          }
        },
        {
          "@type": "Question",
          "name": "What is the risk of hallucinations in an LLM Wiki?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hallucination is a real risk. Raw sources are kept immutable as ground truth. Periodic lint passes let the LLM compare wiki claims against source documents. For mission-critical domains, human review of LLM edits is recommended."
          }
        }
      ]
    }
  ]
}
</script>

## FAQ

**Does LLM Wiki replace RAG?**
No. They solve different problems. RAG is better when you have a large, mostly-static corpus you don't own and need to answer ad-hoc queries against. LLM Wiki is better when you're actively building and curating knowledge over time. Part 5 of this series covers the comparison in depth.

**Do I need a specific LLM to use this pattern?**
No. The pattern works with any LLM agent that has file-system access — Claude Code, Codex, open-source models via local inference tools. The schema document (CLAUDE.md or AGENTS.md) is what makes the LLM behave correctly, and you write that document yourself.

**How large can the wiki get before the index file approach breaks down?**
Karpathy notes it works "surprisingly well at moderate scale (~100 sources, ~hundreds of pages)." Beyond that, community builders have added hybrid search tools (qmd, rtfm) that give the LLM proper search without requiring embeddings infrastructure.

**Is this the same as Obsidian + smart plugins?**
Obsidian is the viewer in Karpathy's setup — not the engine. The LLM writes the wiki; Obsidian displays it. Plugins like Dataview can query page frontmatter, and Marp can generate slide decks from wiki content, but the intelligence comes from the LLM agent, not the Obsidian plugin ecosystem.

**What's the risk of LLM hallucinations corrupting the wiki?**
It's a real risk, especially for high-stakes factual claims (API parameters, version numbers, legal details). The mitigation is the three-layer architecture: raw sources are immutable and serve as ground truth. The lint operation can compare wiki claims against source documents. For critical domains, human review of LLM edits is recommended.

## What's Next

This post explained the pattern. [Part 2](/ai/how-to-implement-llm-wiki-complete-guide/) gets concrete: directory structure, the schema document, ingest and query workflows, and every command you need to set up a working LLM Wiki from scratch using Claude Code.

[Part 3](/ai/best-llm-wiki-community-implementations/) explores the best open-source implementations the community has built in the weeks since the gist — ranked by stars, functionality, and production-readiness.

[Part 4](/ai/llm-wiki-vs-andrew-ng-context-hub/) compares LLM Wiki with Andrew Ng's Context Hub — two projects released around the same time that look similar but solve fundamentally different problems.

[Part 5](/ai/llm-wiki-vs-rag-when-to-use-each/) is the definitive comparison: LLM Wiki vs RAG — how they differ architecturally, where each wins, and how to choose.
