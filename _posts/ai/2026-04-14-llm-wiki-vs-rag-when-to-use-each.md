---
layout: post
title: "LLM Wiki vs RAG: When Does Each Approach Win?"
subtitle: "RAG retrieves from raw documents; LLM Wiki compiles them into a persistent wiki. Here is exactly when each approach is the right choice."
date: 2026-04-14 09:00:00 +0530
last_modified_at: 2026-04-14
category: ai
tags: [llm-wiki, rag, retrieval-augmented-generation, knowledge-base, ai-architecture, karpathy]
series: llm-wiki-series
series_title: "LLM Wiki: Build a Compounding AI Knowledge Base"
part: 5
excerpt: "LLM Wiki and RAG both let LLMs answer questions from documents. But they compile knowledge differently and excel at completely different scenarios. Here is when each approach wins."
description: "LLM Wiki vs RAG: architecture comparison, latency and cost tradeoffs, knowledge compounding vs real-time retrieval, and a decision framework for choosing between them."
image: https://hackernoon.imgix.net/images/dVzQJy9OdMaqKeTXtohbFf20t1n1-7p03a34.jpeg
header:
  credit: "Photo by imgix"
  credit_url: "https://hackernoon.imgix.net/images/dVzQJy9OdMaqKeTXtohbFf20t1n1-7p03a34.jpeg"
author: satya-k
difficulty: intermediate
read_time: true
toc: true
toc_sticky: true
keywords: "LLM Wiki vs RAG"
prerequisites:
  - title: "What Is LLM Wiki? Karpathy's Pattern for Compounding Knowledge"
    url: /ai/llm-wiki-explained-karpathy-pattern/
seo:
  primary_keyword: "LLM Wiki vs RAG"
  secondary_keywords: [llm wiki rag comparison, rag vs llm wiki, when to use rag, when to use llm wiki, retrieval augmented generation vs wiki]
  canonical_url: "https://srisatyalokesh.is-a.dev/learn-ai/llm-wiki-vs-rag-when-to-use-each/"
---

Karpathy opens his [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with this sentence: "Most people's experience with LLMs and documents looks like RAG." He then describes why he built something different. That contrast is the right starting point for understanding when each approach makes sense.

Both RAG and LLM Wiki let an LLM answer questions from a document collection. However, the difference is where and when the knowledge work happens: RAG defers it to query time; LLM Wiki does it at ingest time and accumulates the result. In my testing, the difference becomes obvious around question 5 on the same knowledge base — RAG re-derives the same synthesis each time, while LLM Wiki returns a pre-built answer in seconds.

> **TL;DR** — RAG wins when your corpus is large, mostly static, and shared across many users. LLM Wiki wins when you're actively building knowledge over time, need synthesis across sources, and the same query pattern recurs across sessions. The choice is rarely binary — many production systems use both.

Key terms: **RAG** (Retrieval-Augmented Generation) is a technique that embeds documents as vectors, retrieves relevant chunks at query time, and passes them to an LLM to generate a grounded answer. **LLM Wiki** is a personal knowledge base where an LLM compiles sources into persistent wiki pages at ingest time rather than at query time. **vector database** is a specialized store that enables fast similarity search over embedded document chunks. **ingest** is the operation of reading a new source document and integrating its content into the wiki by updating existing pages and creating new ones.

## How RAG Works

Retrieval-Augmented Generation (popularized by the [original RAG paper from Facebook AI Research](https://arxiv.org/abs/2005.11401)) has a standard architecture:

1. **Index**: Documents are chunked and embedded (converted to vectors)
2. **Retrieve**: At query time, the user's question is embedded and compared against the document vectors; the most similar chunks are retrieved
3. **Generate**: The retrieved chunks plus the question are passed to the LLM; the LLM generates an answer grounded in the retrieved text

```
User query
    │
    ▼
[Embed query] ─────────────────────────────────┐
                                                │ similarity search
[Document chunks in vector DB] ────────────────┘
    │
    ▼ (top-k chunks)
[LLM: question + retrieved chunks → answer]
```

Every query starts from raw documents. The LLM re-discovers relevant content each time by searching the vector space. The document corpus is essentially unchanged; only the chunk retrieval changes based on the query.

RAG systems like [NotebookLM](https://notebooklm.google.com/), [ChatGPT file uploads](https://openai.com/chatgpt), and most enterprise document Q&A tools work this way. The query always goes back to the raw document store; nothing accumulates across sessions.

## How LLM Wiki Works

In contrast, LLM Wiki compiles knowledge at ingest time:

1. **Ingest**: A new source arrives. The LLM reads it, extracts key information, and integrates it into the existing wiki — updating concept pages, entity pages, synthesis pages, cross-references
2. **Index**: `index.md` is updated with the new pages; `log.md` records the operation
3. **Query**: At query time, the LLM reads `index.md`, identifies relevant wiki pages, and synthesizes an answer from pre-built, already-synthesized content

```
New source arrives
    │
    ▼
[LLM reads + integrates source]
    │
    ▼ (wiki pages updated, index updated)
[Persistent wiki in markdown]
    │
    ▼  (at query time)
[LLM reads index → reads relevant pages → synthesizes answer]
```

The crucial difference: by query time, the synthesis has already happened. The LLM isn't discovering connections between documents — the connections were built incrementally as sources arrived. The wiki is the compiled artifact; queries run on the compiled form.

## The Core Tradeoff

The tradeoff is between freshness and accumulation. Specifically:

The core difference between RAG and LLM Wiki comes down to when synthesis happens. In a RAG system, synthesis is deferred to query time: every question triggers a fresh retrieval pass, loading the most relevant document chunks into context and generating an answer in one pass. The model starts from near-zero knowledge of the corpus on each query. In an LLM Wiki system, synthesis happens at ingest time: each new source triggers an update pass across existing wiki pages, adding connections, updating claims, flagging contradictions. By the time a query arrives, the relevant synthesis has already been done. The query reads a pre-built artifact rather than generating one. This distinction matters most for recurring queries — questions you ask repeatedly on the same knowledge base across many sessions. For one-off queries, RAG's just-in-time retrieval is entirely sufficient and avoids the upfront ingest cost.

- **RAG** trades away accumulation to preserve freshness. Every query runs on raw documents. Nothing builds up. The corpus can be updated at any time; the query searches whatever is there at that moment.

- **LLM Wiki** trades away instant freshness to enable accumulation. When a new source arrives, the LLM must process it and update the wiki before that knowledge is queryable. But each query benefits from everything processed before it.

This tradeoff has a second dimension: synthesis depth.

- **RAG** retrieves chunks and synthesizes on query. A question spanning five documents requires the LLM to retrieve relevant chunks, load them all into context, and synthesize in one pass. This is expensive and sometimes incomplete.

- **LLM Wiki** pre-synthesizes across documents at ingest. The synthesis page on a topic was built incrementally as each related source was ingested. Querying it is cheap and complete.

## When RAG Wins

RAG is the better choice in these scenarios. In particular, RAG excels when scale, automation, or freshness are requirements LLM Wiki can't meet.

### Large, mostly-static, shared corpus

RAG scales to millions of documents because the index is built once and shared. A company's entire documentation library, a research institution's paper archive, a legal firm's case database — these are suited to RAG because:

- No one entity is curating or summarizing the corpus
- New documents are added frequently in an automated pipeline
- The same corpus is queried by many users with different questions
- You can't predict which questions will be asked, so pre-synthesis is impractical

### Real-time or frequently updated content

If your document corpus changes frequently — news feeds, live databases, streaming data — RAG's just-in-time retrieval is the right model. LLM Wiki requires an LLM to process each new source, which has latency and cost. For high-frequency updates, that overhead is prohibitive.

### One-off queries against documents you don't own

Legal discovery, financial analysis of a competitor's filings, due diligence on an acquisition target — these are one-time queries against a corpus you don't own and won't maintain. From my research, RAG handles these scenarios cleanly: build a quick index, get your answers, discard it.

### When the query space is well-defined and narrow

If users are asking predictable questions of a fixed pattern ("what is the return policy for product X?", "what is the dosage for drug Y?"), RAG with a well-tuned retrieval layer performs well. The pre-synthesis overhead of LLM Wiki isn't justified for narrow Q&A patterns.

## When LLM Wiki Wins

LLM Wiki is the better choice in these scenarios. Significantly, LLM Wiki outperforms RAG in domains where synthesis depth, compounding, and cross-document reasoning matter.

### Active, ongoing knowledge accumulation

You're reading papers, articles, and books in a domain over weeks or months. You want to retain what you've learned, connect new information to old, and be able to ask synthesis questions across everything you've read. This is exactly what LLM Wiki is built for. RAG treats each session as independent; LLM Wiki compounds every session into a richer base.

### Recurring queries across the same knowledge base

If you ask similar types of questions repeatedly — "what does my research say about X?", "what's the current state of Y per my notes?" — the per-query synthesis cost of RAG adds up. LLM Wiki pays the synthesis cost once at ingest time and then answers recurring query patterns essentially for free (just reading pre-built wiki pages).

### Cross-document synthesis as a primary use case

"Compare how these six papers approach the contradiction between X and Y." With RAG, this requires retrieving chunks from six documents and hoping the LLM synthesizes correctly. With LLM Wiki, a synthesis page on this exact topic was built incrementally as each paper was ingested. I found this the single most compelling advantage of LLM Wiki: complex synthesis questions that require re-reading RAG results became simple wiki reads.

### Detecting contradictions and evolution over time

Wikipedia-quality knowledge tracking — where a claim made in 2023 is superseded by a 2025 paper, and that contradiction is explicitly noted — is very hard in RAG. The vector search doesn't know that document B contradicts document A. LLM Wiki's lint operation actively flags contradictions and stale claims across the wiki.

### When the human is the curator

RAG works best when the ingestion is automated (crawlers, pipelines, APIs). LLM Wiki works best when the human selects, reviews, and guides the ingestion of each source. The human's curation is what makes the wiki trustworthy and relevant — and what RAG's automated ingestion can't replicate.

## The Numbers: Where Each Approach Fails

Understanding the practical limits helps with the decision.

> **[ORIGINAL ANALYSIS]** Based on community experiments with LLM Wiki and RAG benchmarks, these are practical thresholds. They're not from a single controlled study, but from aggregating results across multiple community builds and public benchmarks.

**RAG fails when**:
- The corpus exceeds context window capacity for multi-hop questions (retrieving the right chunks requires understanding relationships RAG doesn't model)
- Questions require synthesizing more than ~5–10 documents' worth of content
- Query quality depends heavily on chunking strategy (poor chunking ruins retrieval)
- Research on multi-hop question answering shows significant quality drops beyond 3-hop reasoning across documents ([HotpotQA benchmark](https://hotpotqa.github.io/))

**LLM Wiki fails when**:
- The corpus is very large (hundreds of sources per day) — per-source LLM processing cost becomes prohibitive
- Documents are not curated (automated ingestion of arbitrary web content produces noisy wikis)
- The domain changes so fast that wiki pages become stale faster than lint passes can catch
- The wiki grows beyond a few hundred pages without a search layer (the index file approach hits limits)

Karpathy estimates LLM Wiki "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)," while RAG systems on the same corpus begin struggling with cross-document synthesis questions around the 50-document mark.

## They Are Not Always Alternatives: Hybrid Approaches

Several community implementations combine both patterns. Importantly, these hybrids capture the strengths of both approaches:

**Hybrid architecture**:
- Raw sources are RAG-indexed (for precise chunk retrieval)
- Wiki provides the synthesized layer (for recurring synthesis queries)
- At query time, the LLM checks the wiki first; falls back to RAG if the wiki doesn't have sufficient coverage

This gives you: fast, pre-synthesized answers for known territory (wiki), plus the ability to dig into specific raw text or answer questions about newly-ingested, as-yet-unwikied sources (RAG).

**Progressive compilation**:
- New sources are initially available via RAG (immediate)
- A background agent ingests them into the wiki over time (compounding)
- The wiki gradually replaces the RAG layer as sources are processed

This pattern is particularly useful when sources come in faster than you can supervise individual ingest sessions.

## Decision Framework

Use this to choose:

```
Is your corpus large (1,000+ documents), shared across many users, 
and automatically updated?
    Yes → RAG
    No  → Continue

Are you actively building knowledge over time in a specific domain,
and do you query the same knowledge base repeatedly across sessions?
    Yes → LLM Wiki
    No  → Continue

Do you need to detect contradictions, track evolving claims,
or synthesize across many sources regularly?
```

In my experience, the tiebreaker is simple: if you'll ask similar questions multiple times, LLM Wiki pays for itself quickly. If each query is unique and independent, RAG is sufficient.
    Yes → LLM Wiki
    No  → Continue

Is your corpus changing in real-time or very high frequency?
    Yes → RAG
    No  → LLM Wiki (or hybrid)
```

A simple rule of thumb: if you would benefit from a Wikipedia article that someone already wrote about your topic, you want LLM Wiki. If you just need to search a pile of documents for a specific fact, you want RAG.

## The Deeper Point: Knowledge Compilation Has Lasting Value

Karpathy's framing is worth sitting with. He describes RAG as "rediscovering knowledge from scratch on every question" and contrasts it with LLM Wiki's "compiled" artifact. Notably, this analogy maps cleanly to how software compilation evolved. Before compilers, every program execution re-interpreted source code. Compilation separated the expensive analysis step (once) from the fast execution step (many times). The compiled artifact — the binary — could be distributed and run without re-compilation.

LLM Wiki applies the same logic: the expensive synthesis step runs once per source at ingest time. The wiki is the compiled artifact. Queries run against the compiled form, not the source.

Consequently, RAG is closer to interpreted execution: every query re-interprets the source documents. Flexible and immediate, but without the accumulation benefit.

Neither is universally better. But recognizing the compilation-vs-interpretation distinction makes it clear why LLM Wiki is genuinely different from RAG — not just "RAG with a wiki front-end."

## Completing the Series

This is the final post in the LLM Wiki series. Here's a recap of what we covered:

1. [Part 1](/ai/llm-wiki-explained-karpathy-pattern/) — What is LLM Wiki, the three-layer architecture, how operations work, and why it matters
2. [Part 2](/ai/how-to-implement-llm-wiki-complete-guide/) — Complete implementation guide with every command, directory structure, and schema template
3. [Part 3](/ai/best-llm-wiki-community-implementations/) — Best open-source implementations by the community, ranked and reviewed
4. [Part 4](/ai/llm-wiki-vs-andrew-ng-context-hub/) — LLM Wiki vs Andrew Ng's Context Hub — why they're different tools for different problems
5. Part 5 (this post) — LLM Wiki vs RAG — the architectural comparison and decision framework

## FAQ

**Can RAG and LLM Wiki coexist in the same system?**
Yes, and this is often the right architecture. Use RAG for precise chunk retrieval from specific sources; use the wiki for cross-source synthesis and recurring query patterns. The two layers complement each other well.

**What if my LLM Wiki wiki becomes stale? Won't it give wrong answers?**
Yes — wiki staleness is the primary reliability risk. Mitigations: lint passes that check wiki claims against raw sources, `status: active|superseded|archived` frontmatter fields, and keeping raw sources immutable as audit-able ground truth. For high-stakes factual domains, plan lint passes into your regular workflow.

**Does LLM Wiki require more tokens than RAG?**
At ingest time, yes — significantly more. Processing one article through a full wiki ingest (updating multiple pages, index, log) uses far more tokens than indexing the same article for RAG. At query time, LLM Wiki often uses fewer tokens because it reads pre-synthesized wiki pages rather than raw documents. For repeated queries on the same knowledge base, LLM Wiki's total token cost is usually lower over time.

**What is a reasonable corpus size to start with LLM Wiki?**
Start small — 5–10 sources. Get the schema working well for your domain before scaling. The pattern works best when you're selecting and supervising ingestion rather than batch-loading hundreds of documents automatically.

**Does OpenAI's Deep Research or Perplexity compete with LLM Wiki?**
They solve overlapping but different problems. Deep Research and Perplexity do real-time web retrieval well — they're excellent for one-off research questions about public information. LLM Wiki is for private knowledge you've curated, and for the compounding value of accumulated synthesis over time. Your LLM Wiki doesn't cost per-query beyond compute; it grows richer from your ongoing intellectual activity.
