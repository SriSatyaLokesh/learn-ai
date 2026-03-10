---
name: blog-write
description: >
  Write new blog articles from scratch optimized for Google rankings and AI
  citations. Generates full articles with template selection, answer-first
  formatting, TL;DR box, information gain markers, citation capsules, sourced
  statistics, image sourcing (Pixabay/Unsplash/Pexels), FAQ schema,
  internal linking zones, and proper heading hierarchy. Adapted for Learn with
  Satya K Jekyll blog with category and series support. Supports markdown output.
  Use when user says "write blog", "new blog post", "create article",
  "write about", "draft blog", "generate blog post".
context: fork
tools:
  - view
  - create
  - edit
  - grep
  - glob
  - web_fetch
  - web_search
  - task
---

# Blog Writer -- New Article Generation

Writes complete blog articles from a topic, brief, or outline. Every article
follows the 6 pillars of dual optimization (Google rankings + AI citations).

**Adapted for Learn with Satya K:**
- Jekyll markdown format with YAML front matter
- Category integration (7 categories: ai, system-design, backend, devops, frontend, career, tools)
- Series support with part numbers and navigation
- Difficulty levels (beginner, intermediate, advanced)
- Learning path integration

**Key references:**
- `.github/agents/blog/templates/` — 12 content templates
- `.github/copilot-instructions.md` — Project requirements and structure
- `_data/categories.yml` — Available categories
- Front matter schema in copilot-instructions.md

## Workflow

### Phase 1: Topic Understanding

1. **Clarify the topic** — If the user provides just a topic, ask:
   - Target audience (who is this for?)
   - Primary keyword / search intent
   - Desired word count (default: 2,000-2,500 words)
   - **Category** (ai, system-design, backend, devops, frontend, career, tools)
   - **Difficulty** (beginner, intermediate, advanced)
   - **Series** (if part of a series, which one and what part number?)
2. **If a brief exists** — Load it and skip to Phase 1.5

### Phase 1.5: Template Selection

Select the appropriate content template from the 12 templates in `.github/agents/blog/templates/`.

1. **Auto-detect content type** from the topic and search intent:
   | Signal | Template |
   |--------|----------|
   | "How to...", process, steps | `how-to-guide` |
   | "Best X", "Top N", list format | `listicle` |
   | Client result, before/after, metrics | `case-study` |
   | "X vs Y", comparison, alternatives | `comparison` |
   | Broad topic, comprehensive guide | `pillar-page` |
   | "Is X worth it", product evaluation | `product-review` |
   | Opinion, prediction, industry take | `thought-leadership` |
   | Expert quotes, multi-source collection | `roundup` |
   | Code walkthrough, tool demo, technical | `tutorial` |
   | Breaking news, algorithm update, event | `news-analysis` |
   | Survey results, experiment, original data | `data-research` |
   | Q&A, knowledge base, "What is X" | `faq-knowledge` |

2. **Load the matching template** — Read from `.github/agents/blog/templates/<type>.md`
3. **Adapt the outline** — Use the template's section structure, heading patterns,
   and word count guidance to shape Phase 3's outline
4. **Fallback** — If no template clearly fits, use the generic outline structure
   in Phase 3 below. Inform the user which template was selected (or that none matched).

### Phase 2: Research

Invoke `blog-researcher` agent (or do inline research with web_search):

1. **Find 8-12 current statistics** (2025-2026 data preferred)
   - Search: `[topic] study 2025 2026 data statistics`
   - Prioritize tier 1-3 sources (government, academic, major tech companies)
   - Record: statistic, source name, URL, date, methodology
2. **Find a cover image** (wide, high-quality, topic-relevant):
   - Search: `site:pixabay.com [topic] wide banner` (preferred)
   - Alternative: `site:unsplash.com [topic] wide`
   - Fallback: `site:pexels.com [topic] wide banner`
   - Target dimensions: 1200x630 (OG-compatible) or 1920x1080
   - Save to: `/assets/img/posts/[slug].jpg`
3. **Find 3-5 inline images** from open-source platforms:
   - **Pixabay** (preferred): Search `site:pixabay.com [topic keywords]`
   - **Unsplash** (alternative): Search `site:unsplash.com [topic keywords]`
   - **Pexels** (fallback): Search `site:pexels.com [topic keywords]`
   - Save to: `/assets/img/posts/[slug]-[number].jpg`

### Phase 3: Outline Generation

Create a structured outline before writing. If a template was loaded in Phase 1.5,
adapt this skeleton to match the template's section structure:

```
# [Title as Question — Include Primary Keyword]

## Introduction (100-150 words)
- Hook with surprising statistic
- Problem/opportunity statement
- What the reader will learn

> **TL;DR:** [40-60 word standalone summary — placeholder]

## H2: [Question Format] (300-400 words)
- Answer-first paragraph (40-60 words with stat + source)
- Supporting evidence
- [Image placement]
- Practical advice
- [CITATION CAPSULE placeholder]
- [INTERNAL-LINK: anchor text → target description]

## H2: [Question Format] (300-400 words)
- Answer-first paragraph
- Analysis and implications
- [CITATION CAPSULE placeholder]
- [INTERNAL-LINK: anchor text → target description]

## H2: [Statement for Variety] (300-400 words)
- Answer-first paragraph
- Real-world example or case study
- [Image placement]
- [CITATION CAPSULE placeholder]

## H2: [Question Format] (300-400 words)
- Answer-first paragraph
- Step-by-step guidance
- [CITATION CAPSULE placeholder]
- [INTERNAL-LINK: anchor text → target description]

## H2: [Question Format] (200-300 words)
- Answer-first paragraph
- Forward-looking analysis

## FAQ Section (3-5 questions, 40-60 words each answer)
- [INTERNAL-LINK: anchor text → detailed content]

## Conclusion (100-150 words)
- Key takeaways (bulleted)
- Call to action
- [INTERNAL-LINK: anchor text → next logical content]
```

Present the outline to the user for approval before writing.

### Phase 4: Content Writing

Write the full article following these rules:

#### 4a. Frontmatter (Jekyll Format)

```yaml
---
title: "[Question-format title with primary keyword]"
date: YYYY-MM-DD
category: [ai|system-design|backend|devops|frontend|career|tools]
tags: [keyword1, keyword2, keyword3, keyword4]
excerpt: "[Brief excerpt for category page, 100-120 chars]"
description: "[Fact-dense SEO description, 150-160 chars, includes 1 statistic]"
difficulty: [beginner|intermediate|advanced]
series: "[series-slug]"  # Optional - only if part of series
series_title: "[Human-readable series name]"  # Optional
part: 1  # Optional - part number in series
header:
  image: /assets/img/posts/[slug].jpg
  credit: Pixabay  # or Unsplash or Pexels
  credit_url: [source URL]
author: satya-k
---
```

**Required fields:**
- title, date, category, tags (4-6 tags), excerpt, description, difficulty, author

**Optional fields (for series posts):**
- series, series_title, part

**Category must be one of:** ai, system-design, backend, devops, frontend, career, tools

**File naming:** `_posts/[category]/YYYY-MM-DD-[slug].md`

#### 4b. TL;DR Box

Immediately after the introduction (before the first H2 body section), add a TL;DR box:

```markdown
> **TL;DR:** [40-60 word standalone summary that makes sense without reading the
> full article. Contains the key finding or recommendation plus 1 statistic with
> source attribution. Reader should get the core value from this alone.]
```

Requirements:
- 40-60 words, no more
- Must be self-contained — understandable without reading the article
- Include 1 specific statistic with source name
- State the key finding, recommendation, or answer
- Place as a blockquote directly after the introduction paragraph

#### 4c. Answer-First Formatting (Critical)

Every H2 section MUST open with a 40-60 word paragraph containing:
- At least one specific statistic with source attribution
- A direct answer to the heading's implicit question

Pattern:
```markdown
## How Does X Impact Y in 2026?

[Stat from source] ([Source Name](url), year). [Direct answer to the heading
question in 1-2 more sentences, explaining the implication and what this means
for the reader.]
```

#### 4d. Information Gain Markers

Distribute at least 2-3 information gain markers throughout the article. These
signal to search engines and AI systems that the content contains original value
not available elsewhere.

Tag each with a comment or visible marker:

- `[ORIGINAL DATA]` — Proprietary surveys, experiments, A/B test results, case
  study metrics the author collected first-hand
- `[PERSONAL EXPERIENCE]` — First-hand observations, lessons learned from direct
  involvement, "when we tried X, Y happened" narratives
- `[UNIQUE INSIGHT]` — Analysis others haven't made, contrarian perspectives
  backed by data, novel connections between existing research

Placement:
- Weave into the body text naturally
- Use as inline comments: `<!-- [ORIGINAL DATA] -->` before the relevant paragraph
- Or as visible callouts:
  ```markdown
  > **Our finding:** [original observation backed by specific data]
  ```
- Minimum 2 per post, target 3 for comprehensive articles

#### 4e. Citation Capsules

For each major H2 section, generate a citation capsule — a 40-60 word self-contained
passage designed so AI systems can extract and quote it directly.

Requirements per capsule:
- 40-60 words, self-contained (makes sense in isolation)
- Contains: one specific claim + one data point + source attribution
- Written in a declarative, quotable style
- Placed within the H2 section body (not as a separate block)

Example:
```markdown
According to a 2026 Gartner study, 58% of enterprise buyers now consult AI
assistants before contacting a vendor ([Gartner](https://www.gartner.com), 2026).
This shift means B2B content must answer specific questions concisely enough
for AI systems to extract and cite in their responses.
```

#### 4f. Internal Linking Zones

Mark internal linking opportunities throughout the article using placeholder
notation. The user (or a follow-up pass) will resolve these to actual URLs.

Zone placement:
- **Introduction** — Link to related pillar content or topic hub
- **Each H2 section** — Link to supporting articles, deeper dives, related tools
- **FAQ section** — Link answers to detailed content that expands on the answer
- **Conclusion** — Link to the next logical piece of content the reader should consume

Format:
```markdown
[INTERNAL-LINK: anchor text → target description]
```

Example:
```markdown
For a deeper dive into keyword clustering, see our
[INTERNAL-LINK: complete guide to keyword clustering → pillar page on keyword research methodology].
```

Target 5-10 internal link zones per 2,000-word post. Use descriptive anchor text
(never "click here" or "read more").

#### 4g. Code Snippets (For Technical Posts)

For technical posts (AI, backend, frontend, tools categories), include code examples:

```markdown
```language
// Your code here with comments
```
```

- Add language identifier (javascript, python, java, go, etc.)
- Include inline comments explaining key lines
- Keep examples concise (10-30 lines max)
- Show working, runnable code

#### 4h. FAQ Section

Include a dedicated FAQ section with 3-5 common questions:

```markdown
## Frequently Asked Questions

### Question 1?
[40-60 word answer with 1 statistic and source]

### Question 2?
[40-60 word answer with 1 statistic and source]

### Question 3?
[40-60 word answer with 1 statistic and source]
```

- Use ### for question headings
- Keep answers concise (40-60 words)
- Include at least 1 statistic per answer
- Link to detailed content where appropriate

### Phase 5: Quality Check

After writing, self-review against scoring criteria:

**Content Quality (30 pts):**
- Depth: Comprehensive coverage, unique insights ✓
- Readability: 40-80 word paragraphs, 15-20 word sentences ✓
- Originality: 2-3 information gain markers ✓
- Structure: Proper heading hierarchy (H1 → H2 → H3) ✓
- Engagement: Questions, examples, actionable advice ✓

**SEO Optimization (25 pts):**
- Title: 50-60 chars, includes primary keyword ✓
- Headings: 60-70% as questions, keyword in 2-3 ✓
- Keywords: Natural density, LSI keywords ✓
- Internal Links: 5-10 marked zones ✓
- Meta Description: 150-160 chars with stat ✓

**E-E-A-T Signals (15 pts):**
- Author: Satya K profile included ✓
- Citations: 8+ unique sources, tier 1-3 only ✓
- Trust: Transparent sources, methodology notes ✓
- Experience: Personal insights, real examples ✓

**Technical Elements (15 pts):**
- Images: 4-6 images with alt text and credits ✓
- Structured Data: Proper markdown hierarchy ✓
- Performance: No heavy embeds ✓

**AI Citation Readiness (15 pts):**
- Citability: Citation capsules in each H2 ✓
- Q&A Format: Question headings, FAQ section ✓
- Entity Clarity: Proper nouns, specific terms ✓
- Extraction Friendly: Clean markdown, no obfuscation ✓

### Phase 6: File Creation

1. Create the markdown file at: `_posts/[category]/YYYY-MM-DD-[slug].md`
2. Ensure front matter is valid YAML
3. Verify category exists in `_data/categories.yml`
4. If series post, note that series metadata will be in `_data/series.yml` (Phase 3 work)

### Phase 7: Next Steps

After file creation, inform the user:

1. **Images to download:** List all image URLs to save to `/assets/img/posts/`
2. **Internal links to resolve:** List all `[INTERNAL-LINK: ...]` placeholders
3. **Quality score estimate:** Based on self-review (aim for 85+)
4. **Suggested next action:** 
   - Run `/blog analyze [file]` for detailed scoring
   - Run `/blog seo-check [file]` for SEO validation
   - Run Jekyll server to preview

## Writing Style Guidelines

### Paragraph Discipline
- Target: 40-80 words per paragraph
- Hard limit: Never exceed 150 words
- Start each paragraph with the most important sentence
- One idea per paragraph

### Sentence Discipline
- Target: 15-20 words per sentence
- Vary sentence length for rhythm
- Active voice preferred
- Natural, conversational tone

### Heading Rules
- One H1 (title only, in front matter)
- H2s for main sections (60-70% as questions)
- H3s for subsections — never skip levels
- Include primary keyword naturally in 2-3 headings

### Citation Rules
- Every statistic must have a named source
- Inline format: `([Source Name](url), year)`
- Tier 1-3 sources only (government, academic, major tech companies)
- Minimum 8 unique statistics per 2,000-word post

### Self-Promotion
- Maximum 1 brand mention (author bio context only)
- No promotional language
- Educational tone throughout

## Difficulty-Based Adjustments

### Beginner Posts
- More explanations and definitions
- Simpler language (avoid jargon)
- Step-by-step breakdowns
- Visual aids and diagrams
- Link to foundational concepts
- Shorter paragraphs (40-60 words)

### Intermediate Posts
- Balanced depth (assumes basic knowledge)
- Some technical terms explained
- Real-world examples
- Code snippets with comments
- Link to related advanced topics

### Advanced Posts
- Deep technical depth
- Assume domain knowledge
- Complex code examples
- Performance considerations
- Architecture discussions
- Link to research papers

## Success Criteria

A successful blog post has:

- ✅ Valid Jekyll front matter with all required fields
- ✅ Saved to correct `_posts/[category]/` directory
- ✅ 2,000-2,500 words (or as specified)
- ✅ 60-70% question headings
- ✅ TL;DR box after introduction
- ✅ Answer-first paragraphs in every H2 section
- ✅ 8+ unique statistics with sources
- ✅ 2-3 information gain markers
- ✅ Citation capsules in each major section
- ✅ 5-10 internal linking zones
- ✅ 4-6 images with credits
- ✅ FAQ section with 3-5 questions
- ✅ Estimated quality score 85+

---

**Remember:** You are writing for both humans and AI systems. Every section should
be independently quotable and citeable. Focus on providing unique value that can't
be found elsewhere.
