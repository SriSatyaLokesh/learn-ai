# Learn with Satya K — System Architecture

**Document:** Technical System Design & Data Flow  
**Last Updated:** March 2026  
**Status:** Foundation Phase (Planned features noted as [PLANNED])

---

## Architecture Overview

Learn with Satya K is a **static Jekyll blog with planned autonomous AI content generation**. The current system is a traditional static site generator; the multi-agent AI pipeline is in design phase.

### Current Architecture (MVP)

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  GitHub Pages (Static Hosting)                              │
│  ├── User Browser                                            │
│  │   ├── Serves premade HTML/CSS/JS (_site/)               │
│  │   ├── Lunr.js search (client-side)                      │
│  │   └── localStorage (progress tracking)                  │
│  │                                                           │
│  └── GitHub Actions (Build on Push)                        │
│      ├── Runs Gulp (CSS/JS processing)                    │
│      └── Runs Jekyll (Markdown → HTML)                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
     │
     │ Pull Request / Commit
     │
┌────▼───────────────────────────────────────────────────────┐
│ Author's Machine (Local Development)                        │
│ ├── Create/edit Markdown posts in _posts/                  │
│ ├── Run: npm run dev (Gulp + Jekyll + BrowserSync)        │
│ ├── Preview at localhost:4000                             │
│ ├── Commit & push                                         │
│ └── (Planned) Run agent pipeline                         │
│     └── Generate posts via Claude API                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Request Flow — User Accessing a Blog Post

```
1. User navigates to: https://username.github.io/learn-with-satya/ai/transformer-architecture/

2. GitHub Pages serves pre-built HTML from _site/ (< 100ms, cached by CDN)

3. Browser renders HTML with:
   - Post content (title, body, metadata)
   - Series navigation (if part of series)
   - Related posts
   - Difficulty badge
   - Table of contents
   - Image credits

4. JavaScript runs:
   - Lunr.js search index loads (if search used)
   - localStorage progress tracker fires
   - Smooth scroll listeners
   - Social share buttons

5. User reads post, scrolls to completion:
   - localStorage records: {postSlug: "transformer-architecture", completed: true}
   - Series progress sidebar updates (% complete)
   - "Mark Complete" button becomes visible at bottom

6. User navigates to next series post:
   - Browser checks localStorage
   - Renders checkmark on series sidebar
   - Fetches next post HTML
```

---

## Data Flow — Blog Post Creation (Current)

```
Author
  │
  ├─ Create Markdown file in _posts/ai/
  │  └─ Include YAML front-matter (title, tags, series, etc.)
  │
  ├─ Place hero image in assets/images/posts/{slug}/
  │
  └─ Commit & push to main
      │
      ▼
  Git Repository (GitHub)
      │
      ├─ Trigger GitHub Actions on push
      │
      ▼
  GitHub Actions Workflow
      │
      ├─ Checkout code
      ├─ Install Ruby gems (bundle install)
      ├─ Install npm deps (npm install)
      │
      ├─ Stage 1: Gulp Processing
      │  ├─ Compile src/yml/_config.yml → _config.yml
      │  ├─ Compile src/js/*.js → assets/js/main.js
      │  └─ Minify CSS
      │
      ├─ Stage 2: Jekyll Build
      │  ├─ Parse _data/*.yml
      │  ├─ Read all _posts/*.md files
      │  ├─ Apply front-matter defaults
      │  ├─ Render _layouts/post.html with Liquid
      │  ├─ Generate _site/ai/transformer-architecture/index.html
      │  ├─ Generate search.json (Lunr.js index)
      │  ├─ Generate feed.xml (RSS)
      │  ├─ Generate sitemap.xml (SEO)
      │
      ▼
  Static Site Generated (_site/)
      │
      ├─ Git push to GitHub Pages deployment folder
      │
      ▼
  GitHub Pages (Content Delivery)
      │
      └─ Serve static HTML to browser (1-3 minutes after push)
```

---

## Data Flow — Planned: AI Content Generation [PLANNED]

**Phase 4 of the project** introduces a multi-agent AI pipeline that generates blog posts automatically.

```
Author Input
  │
  ├─ "Write Part 3 of the AI Fundamentals series on Transformer Architecture"
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│  Agent Pipeline (Local Machine, Node.js)                        │
│                                                                   │
│  1. Orchestrator Agent                                          │
│     Input: Raw topic/request                                    │
│     Output: Structured brief (JSON)                             │
│       ├─ category: "ai"                                         │
│       ├─ is_series: true                                        │
│       ├─ series_id: "ai-fundamentals"                           │
│       ├─ part: 3                                                │
│       ├─ difficulty: "intermediate"                             │
│       └─ word_count_target: 1200                                │
│                                                                   │
│  ↓ (AgentContext handoff)                                       │
│                                                                   │
│  2. Research Agent                                              │
│     Tools: Claude API web_search                                │
│     Input: Content brief                                        │
│     Output: Research insights + source URLs                     │
│       ├─ research_insights: ["...", "..."]                     │
│       ├─ notable_statistics: ["..."]                            │
│       └─ research_sources: [{title, url}, ...]                 │
│                                                                   │
│  ↓ (AgentContext handoff)                                       │
│                                                                   │
│  3. SEO & Strategy Agent                                        │
│     Input: Brief + Research                                     │
│     Output: SEO blueprint (title, outline, keywords)           │
│       ├─ title: "Transformer Architecture Explained: ..."       │
│       ├─ slug: "transformer-architecture-explained"             │
│       ├─ meta_description: "..."                                │
│       ├─ outline: [{h2: "...", h3s: ["..."]}]                 │
│       ├─ primary_keyword: "transformer architecture explained"  │
│       ├─ secondary_keywords: ["self-attention", "encoder-decoder"]
│       └─ image_queries: ["transformer diagram", "..."]          │
│                                                                   │
│  ↓ (AgentContext handoff)                                       │
│                                                                   │
│  4. Writer Agent                                                │
│     Input: Brief + Research + SEO blueprint                    │
│     Output: Full Markdown body text                             │
│       ├─ 1200+ words                                            │
│       ├─ Active voice, developer-friendly tone                  │
│       ├─ Follows SEO outline                                    │
│       ├─ Includes code blocks where relevant                    │
│       ├─ Image placeholders: {{ IMAGE: ... }}                   │
│       └─ "What's Next" section (series posts)                   │
│                                                                   │
│  ↓ (AgentContext handoff)                                       │
│                                                                   │
│  5. Formatter Agent                                             │
│     Input: All prior agent outputs                              │
│     Output: Jekyll-ready .md file                               │
│       ├─ Assembles complete YAML front-matter                   │
│       ├─ Validates front-matter completeness                    │
│       ├─ Replaces image placeholders with proper Markdown      │
│       ├─ Adds image attribution blocks                          │
│       ├─ Verifies word count & keyword presence                 │
│       ├─ Determines output path: _posts/ai/2026-03-10-slug.md  │
│       └─ Writes file to disk                                    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
  ↓
Output File
  │
  ├─ _posts/ai/2026-03-10-transformer-architecture-explained.md
  │  ├─ Complete front-matter
  │  ├─ Full body text
  │  └─ Image placeholders resolved
  │
  ├─ Author reviews Markdown
  ├─ Author sources hero image → assets/images/posts/transformer-architecture-explained/hero.jpg
  ├─ Author commits & pushes
  ▼
(Continues as: Data Flow — Blog Post Creation above)
```

**AgentContext** is a shared TypeScript interface threaded through all agents:

```typescript
interface AgentContext {
  // Orchestrator → All other agents
  topic: string;
  category: string;
  is_series: boolean;
  series_id?: string;
  part_number?: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  target_audience: string;
  word_count_target: number;

  // Research Agent appends
  research_insights: string[];
  notable_statistics: string[];
  research_sources: { title: string; url: string }[];

  // SEO Agent appends
  title: string;
  slug: string;
  meta_description: string;
  outline: { h2: string; h3s: string[] }[];
  primary_keyword: string;
  secondary_keywords: string[];

  // Writer Agent appends
  body_markdown: string;
  image_placeholders: { query: string; caption: string }[];

  // Formatter Agent appends
  final_frontmatter: string;
  final_filepath: string;
  validation_passed: boolean;
}
```

---

## Data Flows — Key Paths

### Path 1: Search Query (Client-Side)

```
User types in search box
  │
  ├─ JavaScript: Lunr.js search.js
  ├─ Searches pre-built index from search.json
  │
  ▼
Results displayed (title, excerpt, URL)
  │
  ├─ No server required
  └─ < 100ms response time
```

### Path 2: Series Navigation

```
User on Post #3 of Series
  │
  ├─ Liquid renders: _includes/series-navigation.html
  ├─ Reads _data/series.yml
  ├─ Finds current post in series.posts[]
  ├─ Renders prev/next buttons with part titles
  │
  ▼
"← Previous: Part 2: ..." | "Next: Part 4: ... →"
```

### Path 3: Category Page

```
User navigates to /ai/ category
  │
  ├─ Jekyll renders _layouts/category.html
  ├─ Reads _data/categories.yml for icon/color
  ├─ Filters _posts/ to only category: ai
  ├─ Groups series posts separately from standalone
  │
  ▼
Category landing page with:
  ├─ Icon, description
  ├─ Series list with progress bars
  └─ Standalone posts grid
```

### Path 4: Series Index Page

```
User visits /series/ai-fundamentals/
  │
  ├─ Jekyll renders _layouts/series.html
  ├─ Reads series metadata from _data/series.yml
  ├─ Lists all parts in order
  │
  ▼
Series index showing:
  ├─ Series title & description
  ├─ All parts listed (Part 1, Part 2, ...)
  ├─ Completion checkmarks (from localStorage)
  ├─ Estimated reading time (total)
  └─ Difficulty level
```

---

## Key Architectural Constraints

| Constraint | Implication | Workaround |
|-----------|------------|-----------|
| **Static Site Only** | No real-time features | Use localStorage + JavaScript for client-side state |
| **No Server Backend** | No user accounts, no persistent data | Series progress stored in browser; no sync across devices |
| **GitHub Pages Jekyll Only** | No custom Ruby plugins | Use GitHub Pages whitelist plugins only |
| **No Database** | All content is Markdown files | Use YAML data files for structured metadata |
| **No Server-Side Auth** | No private posts or member areas | GitHub Discussions (Giscus) for comments; GitHub auth optional |
| **Build Time File Size** | Site build slows if 500+ posts | Use Jekyll incremental builds; monitor at ~200+ posts |

---

## Performance Characteristics

| Operation | Typical Time | Notes |
|-----------|----------|-------|
| Blog post load | < 200ms | Static HTML from GitHub CDN |
| Search query | < 100ms | Lunr.js client-side |
| Series navigation click | Instant | Pre-rendered HTML, no API call |
| Full site build | 10–30 seconds | Depends on post count |
| GitHub Pages deploy | 1–3 minutes | After git push |
| localStorage progress save | < 5ms | Synchronous browser API |

---

## Relationship Diagram: Components

```
┌─────────────────────────────────────────────────────────────────┐
│                      Markdown Posts (_posts/)                    │
│                                                                   │
│  ├─ Metadata: title, date, category, tags, series, difficulty  │
│  └─ Content: Body text, inline images, code blocks             │
│                                                                   │
└────────────────────────┬──────────────────────────────────────────┘
                         │
         ┌───────────────┴────────────────┬──────────────────┐
         │                                │                  │
         ▼                                ▼                  ▼
    Jekyll Parser            _data/series.yml      _data/categories.yml
         │                        │                        │
         │ (matches series/part)   │ (series metadata)     │ (category metadata)
         │                        │                        │
         └────────────┬───────────┴────────────┬───────────┘
                      │                        │
                      ▼                        ▼
            _layouts/post.html      _includes/series-nav.html
            _includes/toc.html      _includes/category-badge.html
            _includes/author.html   _includes/difficulty-badge.html
                      │                        │
                      └────────────┬───────────┘
                                   │
                                   ▼
                    assets/css/main.css (styled)
                    assets/js/main.js (search, progress)
                                   │
                                   ▼
                        _site/ai/post-slug.html
                        (.deployed to GitHub Pages)
                                   │
                                   ▼
                            User Browser
                    (renders HTML + localStorage + JS)
```

---

## Error Handling & Validation

### Post Creation (Current)

1. **Jekyll Build Errors:**
   - YAML parsing failure → GitHub Actions workflow fails
   - HTML syntax error → Jekyll stops build
   - Missing front-matter field → Error message in build log

2. **Manual Checks by Author:**
   - Read post in browser
   - Verify links work
   - Check image placement
   - Proofread content

### Post Creation (Planned - AI Agents)

1. **Orchestrator Validation:**
   - Confirms category exists in `_data/categories.yml`
   - Confirms series exists or creates new one
   - Validates difficulty level is one of: beginner, intermediate, advanced

2. **Formatter Agent Validation:**
   - Checks all front-matter fields present and valid
   - Verifies word count ≥ minimum
   - Confirms primary keyword in title, description, first paragraph, H2
   - Validates image credit format for all external images
   - Tests YAML syntax
   - Ensures part number is unique within series

3. **Author Review:**
   - Final human approval before commit

---

## References

- **Tech Stack:** [stack.md](stack.md)
- **Directory Structure:** [structure.md](structure.md)
- **Conventions:** [conventions.md](conventions.md)
- **PRD (Detailed Features):** `.github/docs/LearnHub_PRD.md`
- **TRD (Agent System):** `.github/docs/LearnHub_TRD.md`
