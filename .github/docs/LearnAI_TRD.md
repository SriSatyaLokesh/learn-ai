# LearnAI — Technical Requirements Document (TRD)
**Version:** 1.0 | **Date:** March 2026 | **Status:** Draft

---

## Document Info

| Field | Detail |
|---|---|
| Project Name | LearnAI — Jekyll-Based AI-Powered Learning Blog System |
| Document Type | Technical Requirements Document |
| Author | Satya K |
| Stack | Jekyll 4.x · GitHub Pages · Chirpy Theme · Claude API · Node.js |
| Companion Doc | LearnAI PRD v1.0 |

---

## Table of Contents

10. [Technical Architecture Overview](#10-technical-architecture-overview)
11. [Jekyll Site Structure](#11-jekyll-site-structure)
12. [Jekyll Configuration](#12-jekyll-configuration)
13. [Front-Matter Specification](#13-front-matter-specification)
14. [\_data Files Specification](#14-_data-files-specification)
15. [Agent System — Technical Specification](#15-agent-system--technical-specification)
16. [Theme Selection & Customisation](#16-theme-selection--customisation)
17. [GitHub Pages Deployment](#17-github-pages-deployment)
18. [SEO Technical Implementation](#18-seo-technical-implementation)
19. [Search Implementation](#19-search-implementation)
20. [Implementation Roadmap](#20-implementation-roadmap)
21. [Security & Privacy](#21-security--privacy)
22. [Glossary](#22-glossary)

---

## 10. Technical Architecture Overview

### 10.1 System Components

| Component | Technology | Purpose |
|---|---|---|
| Blog Engine | Jekyll 4.x | Static site generation from Markdown + Liquid templates |
| Hosting | GitHub Pages | Free static hosting with auto-build on git push |
| CDN (optional) | Cloudflare (free tier) | Edge caching, HTTPS, performance boost |
| Theme | Chirpy | Base layout, responsive design, built-in dark mode |
| Search | Lunr.js | Client-side full-text search index built at Jekyll build time |
| Agent Runner | Node.js / TypeScript | Local runner that invokes AI agent chain |
| AI Backbone | Claude API (`claude-sonnet-4-6`) | Powers all five agents |
| Web Search (Agent) | Claude web_search tool | Research Agent's ability to browse the web |
| Image CDN | Unsplash API / Wikimedia Commons | Freely licensed images with metadata for attribution |
| Analytics | Plausible or Fathom | Privacy-first visitor analytics (no cookies, GDPR-friendly) |
| Comments (optional) | Giscus (GitHub Discussions) | Comment threads via GitHub without a backend |

---

## 11. Jekyll Site Structure

### 11.1 Directory Layout

```
learn-ai/
├── _posts/
│   ├── ai/                        # AI category posts
│   ├── system-design/             # System Design posts
│   ├── backend/                   # Backend Engineering posts
│   ├── devops/                    # DevOps posts
│   ├── frontend/                  # Frontend posts
│   ├── career/                    # Career posts
│   └── tools/                    # Dev Tools posts
│
├── _data/
│   ├── series.yml                 # All learning series metadata
│   └── categories.yml            # Category slugs, names, colours, icons
│
├── _layouts/
│   ├── post.html                  # Post layout: series nav, TOC, read time
│   ├── series.html                # Series index page layout
│   └── category.html             # Category landing page layout
│
├── _includes/
│   ├── image-credit.html          # Reusable image credit partial
│   ├── series-nav.html            # Prev/next series navigation partial
│   ├── series-sidebar.html        # Sticky learning path sidebar partial
│   ├── toc.html                   # Auto table of contents partial
│   └── jsonld-article.html        # Schema.org JSON-LD injection
│
├── assets/
│   ├── images/posts/              # Local hero images by post slug
│   └── js/
│       ├── search.js              # Lunr.js search implementation
│       ├── progress.js            # localStorage series progress tracker
│       └── series-progress.js     # Series completion % calculator
│
├── agents/                        # Agent runner scripts (not part of Jekyll build)
│   ├── orchestrator.js
│   ├── research.js
│   ├── seo.js
│   ├── writer.js
│   ├── formatter.js
│   └── config.js                  # API keys via .env, model settings
│
├── _config.yml                    # Jekyll main configuration
├── Gemfile                        # Ruby gem dependencies
└── .github/
    └── workflows/
        └── deploy.yml             # GitHub Actions build & deploy workflow
```

> **Note:** The `agents/` directory is excluded from the Jekyll build via `exclude` in `_config.yml`. It is a local tooling folder only.

---

## 12. Jekyll Configuration

### 12.1 `_config.yml` — Essential Settings

```yaml
# Site identity
theme: jekyll-theme-chirpy
title: LearnAI
tagline: Structured learning paths for modern developers
description: A developer learning blog covering AI, System Design, Backend, and more.
url: "https://yourusername.github.io"
baseurl: "/learn-ai"

# Author
author:
  name: Your Name
  url: https://yourportfolio.com

# Permalink structure
permalink: /:categories/:title/

# Pagination
paginate: 12
paginate_path: "/page:num/"

# Build settings
markdown: kramdown
highlighter: rouge
kramdown:
  syntax_highlighter: rouge

# Plugins (all GitHub Pages whitelisted)
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-paginate
  - jekyll-toc
  - jekyll-relative-links

# Exclude from build
exclude:
  - agents/
  - node_modules/
  - .env
  - "*.js"        # root-level scripts only
  - Gemfile.lock
  - README.md

# Front-matter defaults
defaults:
  - scope:
      path: "_posts"
      type: "posts"
    values:
      layout: post
      read_time: true
      toc: true
      toc_sticky: true
      comments: true

# Collections (for series index pages)
collections:
  series:
    output: true
    permalink: /series/:name/
```

### 12.2 `Gemfile`

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-theme-chirpy"

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
  gem "jekyll-paginate"
  gem "jekyll-toc"
  gem "jekyll-relative-links"
end
```

---

## 13. Front-Matter Specification

### 13.1 Complete Front-Matter Template

All posts must include the following YAML front-matter. The **Formatter Agent** is responsible for generating and validating this block on every post it creates.

```yaml
---
title: "Understanding Transformer Architecture"
subtitle: "How attention mechanisms changed everything in AI"
date: 2026-03-10 09:00:00 +0530
last_modified_at: 2026-03-10

# Taxonomy
category: ai
tags: [transformers, attention, deep-learning, nlp]

# Series (omit both fields for standalone posts)
series: ai-fundamentals
series_title: "AI Fundamentals"
part: 3

# Content metadata
excerpt: "A deep dive into how transformer models use self-attention to process sequences in parallel — and why this changed AI forever."
description: "Learn transformer architecture from scratch: self-attention, encoder-decoder structure, positional encoding, and how BERT and GPT use it."  # SEO meta (140-160 chars)

# Hero image (author-provided)
header:
  image: /assets/images/posts/transformer-arch/hero.jpg
  image_credit: "Photo by John Doe on Unsplash"
  image_credit_url: "https://unsplash.com/photos/xyz"

# Learning metadata
difficulty: intermediate   # beginner | intermediate | advanced
read_time: true
toc: true
toc_sticky: true

# Prerequisites (optional)
prerequisites:
  - title: "AI Fundamentals Part 2: Backpropagation"
    url: /ai/ai-fundamentals-part-2/

# SEO
seo:
  primary_keyword: "transformer architecture explained"
  secondary_keywords: [self-attention, encoder decoder, BERT, GPT]
  "canonical_url": "https://yourusername.github.io/learn-ai/ai/transformer-architecture/"
---
```

### 13.2 Front-Matter Field Reference

| Field | Type | Required | Rules |
|---|---|---|---|
| `title` | String | ✅ Yes | Should naturally include primary keyword. Max 70 chars. |
| `subtitle` | String | Optional | Sub-heading shown below title. Max 120 chars. |
| `date` | DateTime | ✅ Yes | ISO format with timezone offset (e.g., `2026-03-10 09:00:00 +0530`) |
| `last_modified_at` | Date | Optional | Updated by Formatter Agent on re-generation |
| `category` | String | ✅ Yes | Must exactly match a slug from `_data/categories.yml` |
| `tags` | Array | ✅ Yes | 3–7 lowercase hyphenated tags |
| `series` | String | Conditional | Series slug from `_data/series.yml`. Omit for standalone posts. |
| `series_title` | String | Conditional | Required if `series` is set. Human-readable series name. |
| `part` | Integer | Conditional | Required if `series` is set. Must be unique within the series. |
| `excerpt` | String | ✅ Yes | 2–3 sentence post summary shown in cards. Max 250 chars. |
| `description` | String | ✅ Yes | SEO meta description. **140–160 chars.** Must include primary keyword. |
| `header.image` | Path | Optional | Relative path to hero image in `assets/`. Author-provided. |
| `header.image_credit` | String | Conditional | Required if `header.image` is set. Full attribution string. |
| `header.image_credit_url` | URL | Conditional | Required if `header.image_credit` is set. Original image URL. |
| `difficulty` | Enum | ✅ Yes | One of: `beginner`, `intermediate`, `advanced` |
| `toc` | Boolean | Optional | Enable auto-generated Table of Contents (recommended for posts > 800 words) |
| `prerequisites` | Array | Optional | Array of `{title, url}` objects linking to prior posts |
| `seo.primary_keyword` | String | ✅ Yes | Main target keyword. Used for validation checks by Formatter Agent. |
| `seo.canonical_url` | URL | ✅ Yes | Absolute canonical URL for this post. |

---

## 14. `_data` Files Specification

### 14.1 `_data/series.yml`

```yaml
- id: ai-fundamentals
  title: "AI Fundamentals"
  description: "From zero to understanding modern AI systems — no PhD required."
  category: ai
  difficulty: beginner
  total_parts: 8             # Update as posts are added
  cover_image: /assets/images/series/ai-fundamentals-cover.jpg
  posts:
    - part: 1
      slug: what-is-machine-learning
      title: "What is Machine Learning?"
    - part: 2
      slug: neural-networks-explained
      title: "Neural Networks Explained"
    - part: 3
      slug: transformer-architecture
      title: "Understanding Transformer Architecture"

- id: system-design-primer
  title: "System Design Primer"
  description: "Learn to design scalable systems from first principles."
  category: system-design
  difficulty: intermediate
  total_parts: 10
  cover_image: /assets/images/series/system-design-primer-cover.jpg
  posts:
    - part: 1
      slug: what-is-system-design
      title: "What is System Design?"
```

### 14.2 `_data/categories.yml`

```yaml
- slug: ai
  name: "Artificial Intelligence"
  icon: "🤖"
  color: "#6366F1"
  description: "LLMs, ML fundamentals, RAG, embeddings, and AI agents"

- slug: system-design
  name: "System Design"
  icon: "🏗️"
  color: "#0EA5E9"
  description: "Scalability, distributed systems, and architecture patterns"

- slug: backend
  name: "Backend Engineering"
  icon: "⚙️"
  color: "#10B981"
  description: "APIs, databases, authentication, and microservices"

- slug: devops
  name: "DevOps & Infrastructure"
  icon: "🚀"
  color: "#F59E0B"
  description: "CI/CD, Docker, Kubernetes, and cloud deployment"

- slug: frontend
  name: "Frontend & Web"
  icon: "🎨"
  color: "#EC4899"
  description: "Modern JS, React, performance, and web standards"

- slug: career
  name: "Career & Mindset"
  icon: "🧠"
  color: "#8B5CF6"
  description: "Developer growth, productivity, and job hunting"

- slug: tools
  name: "Dev Tools & Ecosystem"
  icon: "🛠️"
  color: "#64748B"
  description: "IDEs, CLI tools, frameworks, and boilerplate"
```

---

## 15. Agent System — Technical Specification

### 15.1 Technology Stack

| Component | Choice & Rationale |
|---|---|
| Language | Node.js (TypeScript recommended) — Anthropic SDK has excellent JS/TS support |
| AI Model | `claude-sonnet-4-6` — Best balance of speed, cost, and quality for content tasks |
| Agent Pattern | Sequential chain with structured JSON handoffs. No parallelism — preserves context quality. |
| Web Search | Claude's built-in `web_search` tool (`type: web_search_20250305`) for Research Agent |
| Image Search | Unsplash API (free tier) for image suggestions; Wikimedia API for attribution lookups |
| File I/O | Node.js `fs` module — Formatter Agent writes directly to `_posts/category/` directory |
| Environment | `dotenv` for API key management (`.env` file never committed to git) |
| Runner Interface | CLI: `node agents/run.js "your content idea here"` |

### 15.2 Orchestrator Agent

Receives the author's raw idea and produces a structured content brief passed to all subsequent agents.

**Input:** Free-text prompt from author via CLI

**Output schema:**
```json
{
  "topic": "Transformer Architecture in AI",
  "category": "ai",
  "is_series": true,
  "series_id": "ai-fundamentals",
  "part_number": 3,
  "difficulty": "intermediate",
  "target_audience": "developers with basic ML knowledge",
  "scope_notes": "Focus on self-attention and why it replaced RNNs",
  "word_count_target": 1200
}
```

**Behaviour:**
- Classifies category from the 7 defined options
- Detects if this is a series post or standalone
- Detects if a new series needs to be created or an existing one extended
- If classification confidence is low, outputs clarification questions before proceeding
- Max tokens: `500`

### 15.3 Research Agent

**Input:** Content brief JSON from Orchestrator

**Tools used:** `web_search` (performs 4–6 targeted searches)

**Search strategy:**
1. Recent tutorials/articles on the topic
2. Statistics and data points
3. Common misconceptions or pitfalls
4. Expert perspectives or case studies

**Output:**
```json
{
  "research_insights": [
    "Transformers process all tokens in parallel, unlike RNNs which are sequential",
    "The original 'Attention is All You Need' paper was published in 2017 by Google Brain",
    "Self-attention complexity is O(n²) in sequence length — a known limitation"
  ],
  "notable_statistics": [
    "GPT-4 is estimated to have ~1.8 trillion parameters",
    "BERT uses only the encoder; GPT uses only the decoder"
  ],
  "research_sources": [
    { "title": "Attention is All You Need", "url": "https://arxiv.org/abs/1706.03762" },
    { "title": "The Illustrated Transformer", "url": "https://jalammar.github.io/illustrated-transformer/" }
  ],
  "content_gaps": "Most articles skip positional encoding intuition — good angle for this post"
}
```

**Max tokens:** `2000`

### 15.4 SEO & Strategy Agent

**Input:** Content brief + Research summary

**Responsibilities:**
- Title generation with primary keyword in first 60 characters
- Slug generation (kebab-case, max 60 characters)
- Meta description (140–160 characters, includes primary keyword)
- H2/H3 outline (5–8 sections)
- Primary keyword + 4–6 secondary keywords
- Suggested internal links to existing posts in same category
- 2–3 image search query suggestions for Unsplash

**SEO rules enforced:**
- Primary keyword in: title, first paragraph, at least one H2, and meta description
- No keyword stuffing (max density ~2%)
- Internal links to 2–3 related posts
- Slug must not contain stop words (the, a, and, etc.)

**Output schema:**
```json
{
  "title": "Transformer Architecture Explained: Self-Attention from Scratch",
  "slug": "transformer-architecture-explained",
  "meta_description": "Learn how transformer architecture works — self-attention, positional encoding, encoder-decoder structure, and why it replaced RNNs in modern AI.",
  "outline": [
    {
      "h2": "What Problem Did Transformers Solve?",
      "h3s": ["The RNN Bottleneck", "Why Sequential Processing Doesn't Scale"],
      "notes": "Hook readers with the problem before introducing the solution"
    },
    {
      "h2": "The Self-Attention Mechanism",
      "h3s": ["Queries, Keys, and Values", "Attention Score Calculation", "Multi-Head Attention"],
      "notes": "Include a visual diagram placeholder here"
    }
  ],
  "primary_keyword": "transformer architecture explained",
  "secondary_keywords": ["self-attention mechanism", "encoder decoder transformer", "BERT vs GPT", "positional encoding"],
  "internal_link_suggestions": [
    { "anchor": "neural network basics", "url": "/ai/neural-networks-explained/" }
  ],
  "image_queries": [
    "transformer neural network diagram",
    "self-attention mechanism visualization",
    "encoder decoder architecture"
  ]
}
```

**Max tokens:** `1500`

### 15.5 Writing Agent

**Input:** Content brief + Research summary + SEO blueprint

**Writing constraints:**
- Minimum 800 words for series posts; 600 words for standalone posts
- Active voice throughout
- Developer-friendly tone: conversational but technically precise
- No plagiarism — all content rewritten from research in original voice
- Include a "What's Next" section at the end of all series posts

**Image placeholder format used in body:**
```
{{ IMAGE: transformer diagram self-attention | caption: Diagram showing how queries, keys and values interact in self-attention | credit: unsplash }}
```

**Required sections for series posts:**
1. Introduction / hook
2. Body sections (following the H2/H3 outline from SEO Agent)
3. Key Takeaways (bulleted summary)
4. What's Next (link to next part in the series)

**Output:** Full Markdown body text (no front-matter — handled by Formatter Agent)

**Max tokens:** `4000`

### 15.6 Formatter Agent

**Input:** All prior agent outputs (brief, research, SEO blueprint, written body)

**Responsibilities:**
1. Assemble complete Jekyll front-matter from all collected data
2. Replace `{{ IMAGE: ... }}` placeholders with proper Markdown + attribution
3. Validate front-matter completeness against the field reference in Section 13.2
4. Verify series/part number consistency with `_data/series.yml`
5. Check word count meets minimum
6. Confirm primary keyword is present in title and `meta_description`
7. Confirm attribution is present for all non-local images
8. Determine output file path: `_posts/{category}/{YYYY-MM-DD}-{slug}.md`
9. Write file to disk
10. Print console summary to author

**Image attribution format output:**
```markdown
![Diagram showing how queries, keys and values interact in self-attention](https://images.unsplash.com/photo-xyz)
*Photo by Jane Smith on [Unsplash](https://unsplash.com/photos/xyz) — Unsplash License*
```

**Max tokens:** `2000`

### 15.7 Agent Handoff — `AgentContext` Data Contract

All inter-agent handoffs use a single cumulative `AgentContext` object passed through the chain. Each agent reads from and appends to this object. It is also saved as a JSON sidecar file (`agents/output/{slug}.context.json`) for debugging.

```typescript
interface AgentContext {
  // Set by Orchestrator
  topic: string;
  category: string;
  is_series: boolean;
  series_id?: string;
  part_number?: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  target_audience: string;
  scope_notes: string;
  word_count_target: number;

  // Set by Research Agent
  research_insights: string[];
  notable_statistics: string[];
  research_sources: { title: string; url: string }[];
  content_gaps: string;

  // Set by SEO Agent
  title: string;
  slug: string;
  meta_description: string;
  outline: { h2: string; h3s: string[]; notes: string }[];
  primary_keyword: string;
  secondary_keywords: string[];
  internal_link_suggestions: { anchor: string; url: string }[];
  image_queries: string[];

  // Set by Writing Agent
  body_markdown: string;
  image_placeholders: { query: string; caption: string; credit: string }[];

  // Set by Formatter Agent
  final_frontmatter: string;
  final_filepath: string;
  validation_passed: boolean;
  validation_errors?: string[];
}
```

### 15.8 Agent Runner — CLI Interface

```bash
# Run the full pipeline
node agents/run.js "Write Part 3 of the AI Fundamentals series on Transformer Architecture"

# Run with explicit overrides
node agents/run.js "Standalone post on why developers should learn Docker" --category devops --difficulty beginner

# Dry run (skip file write, just print the output)
node agents/run.js "..." --dry-run
```

**`.env` file (never committed):**
```env
ANTHROPIC_API_KEY=sk-ant-...
UNSPLASH_ACCESS_KEY=...
```

---

## 16. Theme Selection & Customisation

### 16.1 Theme Comparison

| Theme | Pros | Cons |
|---|---|---|
| **Chirpy** ⭐ Recommended | Dark mode built-in, excellent TOC, reading time, categories, ideal for dev blogs | Less flexible for fully custom layouts |
| Minimal Mistakes | Highly configurable, large community, built-in category/tag pages | Heavier; more config upfront |
| Just the Docs | Great for documentation-style series | Less blog-like; better for pure docs |
| TeXt Theme | Clean, feature-rich, good for tech blogs | Smaller community |

> **Recommendation:** Use **Chirpy** for its out-of-the-box dark mode, built-in TOC, reading time display, and excellent category support. It requires minimal customisation to match Learn with Satya K requirements.

### 16.2 Custom Additions to Theme

The following custom components must be built on top of the chosen theme:

| Component | File | Description |
|---|---|---|
| Series Navigation | `_includes/series-nav.html` | Prev/Next buttons with part titles, injected below post content |
| Learning Path Sidebar | `_includes/series-sidebar.html` | Sticky list of all series parts with completion checkmarks |
| Difficulty Badge | `_includes/difficulty-badge.html` | Colour-coded badge (green/yellow/red) shown next to read time |
| Image Credit Block | `_includes/image-credit.html` | Renders the structured attribution block below each image |
| Progress Tracker | `assets/js/progress.js` | Marks posts as read in `localStorage` on scroll-to-bottom |
| Series Completion Bar | `assets/js/series-progress.js` | Calculates and renders series completion % on series index pages |
| JSON-LD Injection | `_includes/jsonld-article.html` | Schema.org Article structured data for SEO rich results |

---

## 17. GitHub Pages Deployment

### 17.1 Step-by-Step Deployment Flow

1. Developer runs the agent pipeline locally:
   ```bash
   node agents/run.js "Write Part 3 of AI Fundamentals on Transformers"
   ```
2. Formatter Agent writes the `.md` file to `_posts/ai/` and notifies the developer
3. Developer reviews the generated Markdown, makes any manual edits, places the hero image in `assets/images/posts/{slug}/hero.jpg`
4. Developer commits and pushes:
   ```bash
   git add .
   git commit -m "feat(ai): add ai-fundamentals-part-3 transformer architecture"
   git push origin main
   ```
5. GitHub Actions workflow triggers Jekyll build
6. Site is live at `https://yourusername.github.io/Learn with Satya K/` within 1–3 minutes

### 17.2 GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy Jekyll to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: "3.2"
          bundler-cache: true

      - name: Build Jekyll
        run: bundle exec jekyll build --destination ./_site
        env:
          JEKYLL_ENV: production

      - name: Validate HTML (optional)
        run: bundle exec htmlproofer ./_site --disable-external --checks Links,Images

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 18. SEO Technical Implementation

### 18.1 Plugin Configuration

| Plugin | Configuration |
|---|---|
| `jekyll-seo-tag` | Reads `title`, `description`, `canonical_url`, and `header.image` from front-matter to auto-generate `<meta>` and OpenGraph tags |
| `jekyll-sitemap` | Auto-generates `/sitemap.xml` on build. Exclude pages via `sitemap: false` in front-matter. |
| `jekyll-feed` | Generates `/feed.xml` for all posts. Configure per-category feeds in `_config.yml`. |
| `jekyll-toc` | Scans H2/H3 elements in post body to generate sticky table of contents. Enabled via `toc: true` in front-matter. |

### 18.2 Schema.org JSON-LD

Each post page injects an `Article` schema JSON-LD block via `_includes/jsonld-article.html`:

```html
<!-- _includes/jsonld-article.html -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{{ page.title }}",
  "description": "{{ page.description }}",
  "author": {
    "@type": "Person",
    "name": "{{ site.author.name }}",
    "url": "{{ site.author.url }}"
  },
  "datePublished": "{{ page.date | date_to_xmlschema }}",
  "dateModified": "{{ page.last_modified_at | date_to_xmlschema | default: page.date | date_to_xmlschema }}",
  "image": "{{ page.header.image | absolute_url }}",
  "url": "{{ page.url | absolute_url }}",
  "publisher": {
    "@type": "Organization",
    "name": "{{ site.title }}",
    "url": "{{ site.url }}"
  }
}
</script>
```

### 18.3 OpenGraph & Twitter Cards

These are auto-handled by `jekyll-seo-tag`. Ensure the following in `_config.yml`:

```yaml
twitter:
  username: your_twitter_handle

social:
  name: Your Name
  links:
    - https://twitter.com/your_twitter_handle
    - https://github.com/yourusername
```

---

## 19. Search Implementation

### 19.1 Lunr.js Client-Side Search

| Component | Detail |
|---|---|
| Index Generation | A Jekyll plugin generates `search.json` at build time containing: post title, excerpt, URL, category, tags, and part number for all posts |
| Index Loading | `search.js` fetches `/search.json` on page load and builds the Lunr index client-side |
| Search UI | Modal or slide-in panel triggered by `Cmd+K` / `Ctrl+K` and search icon in nav |
| Results Display | Show post title, category badge, excerpt snippet, and series info (if applicable) |
| Performance | Search index is compressed; typically < 200KB for 500 posts |

### 19.2 `search.json` Generation (Jekyll Plugin)

```liquid
---
layout: null
---
[
  {% for post in site.posts %}
  {
    "title": {{ post.title | jsonify }},
    "excerpt": {{ post.excerpt | strip_html | truncatewords: 30 | jsonify }},
    "url": {{ post.url | jsonify }},
    "category": {{ post.category | jsonify }},
    "tags": {{ post.tags | jsonify }},
    "series": {{ post.series | jsonify }},
    "part": {{ post.part | jsonify }},
    "difficulty": {{ post.difficulty | jsonify }},
    "date": {{ post.date | date: "%b %-d, %Y" | jsonify }}
  }{% unless forloop.last %},{% endunless %}
  {% endfor %}
]
```

---

## 20. Implementation Roadmap

### 20.1 Phased Delivery Plan

| Phase | Deliverables | Duration |
|---|---|---|
| **Phase 1: Foundation** | Jekyll project init, Chirpy theme setup, `_config.yml`, basic layouts (post, category, series), GitHub Pages deployment pipeline, Gemfile & dev environment | Week 1–2 |
| **Phase 2: Content Architecture** | `_data/series.yml` + `categories.yml`, custom includes (series-nav, sidebar, difficulty badge, image-credit), front-matter spec finalised, `search.json` generation | Week 2–3 |
| **Phase 3: Agent Pipeline** | Orchestrator + Research + SEO + Writing + Formatter agents coded & tested locally. dotenv config. Test run producing 2–3 sample posts end-to-end. | Week 3–5 |
| **Phase 4: First Content Wave** | Publish ≥ 2 complete series (8+ posts each) and 5 standalone posts across 3 categories using the agent pipeline | Week 5–7 |
| **Phase 5: Polish & SEO** | Schema JSON-LD injection, sitemap submission to Google Search Console, Plausible analytics setup, Giscus comments, Lighthouse audit & fixes | Week 7–8 |
| **Phase 6: Portfolio Integration** | Add blog section to developer portfolio with latest posts widget, series spotlight, and link to Learn with Satya K | Week 8–9 |

### 20.2 Post-Launch Backlog

- [ ] Per-category RSS feeds
- [ ] Newsletter signup (via free Buttondown or similar)
- [ ] "Suggest a Topic" GitHub Issues link in footer
- [ ] Reading time distribution analytics in Plausible
- [ ] Automated broken link checker in GitHub Actions
- [ ] WebP image optimisation pipeline in GitHub Actions

---

## 21. Security & Privacy

| Area | Policy |
|---|---|
| **API Keys** | Claude API key stored in `.env` file, never committed. Use GitHub Secrets for any CI/CD usage. |
| **No User Data** | No login system, no personal data stored server-side. Series progress is `localStorage` only. |
| **Analytics** | Use Plausible or Fathom — privacy-first, no cookies, no GDPR consent banner required. |
| **Comments** | Giscus uses GitHub OAuth. Users authenticate with their own GitHub account; no custom user database. |
| **Content Review** | Author reviews all AI-generated content before pushing. No unreviewed content ever reaches production. |
| **Image Licenses** | Only CC0, CC-BY, or Unsplash License images. No copyrighted images. Attribution always included. |
| **Dependencies** | Run `npm audit` and `bundle audit` periodically. Pin gem/package versions in lockfiles. |

---

## 22. Glossary

| Term | Definition |
|---|---|
| **Jekyll** | Ruby-based static site generator that converts Markdown + Liquid templates to HTML |
| **GitHub Pages** | Free static hosting service by GitHub that natively runs Jekyll builds |
| **Front-matter** | YAML metadata block at the top of each Markdown file (between `---` delimiters) |
| **Learning Series** | An ordered collection of blog posts forming a complete curriculum on a topic |
| **Orchestrator Agent** | First agent in the pipeline that parses the author's idea and produces a structured brief |
| **Research Agent** | Agent that uses web search to gather reference material and statistics |
| **SEO Agent** | Agent responsible for keyword strategy, post outline, and meta information |
| **Writing Agent** | Agent that composes the full blog post body following the SEO outline |
| **Formatter Agent** | Final agent that assembles the Jekyll-ready `.md` file with complete front-matter |
| **AgentContext** | Shared TypeScript interface passed between all agents carrying cumulative data |
| **Lunr.js** | A lightweight full-text search library that runs entirely in the browser |
| **Chirpy** | A feature-rich Jekyll theme designed for technical/developer blogs |
| **Giscus** | Comment system powered by GitHub Discussions, embeds via script tag |
| **JSON-LD** | A structured data format for Schema.org markup, used for SEO rich results |
| **WebP** | Modern image format with superior compression over JPEG/PNG for web delivery |
| **Liquid** | Jekyll's templating language used in layouts and includes |
| **Front-matter defaults** | `_config.yml` section that applies front-matter values to all posts matching a scope |
| **Whitelist plugins** | Jekyll plugins officially supported by GitHub Pages (no custom plugins allowed) |

---

*LearnAI TRD v1.0 — March 2026 — This is a living document. Update version and date on any revision.*
