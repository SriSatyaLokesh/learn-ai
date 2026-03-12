# blog

Full-lifecycle blog engine with 12 commands, 12 content templates, 5-category
100-point scoring, and 4 specialized agents. Optimized for Google rankings
(December 2025 Core Update, E-E-A-T) and AI citations (GEO/AEO).

Adapted for **LearnAI** Jekyll blog with:
- 7 categories (ai, system-design, backend, devops, frontend, career, tools)
- Series support with navigation
- Difficulty levels (beginner, intermediate, advanced)
- Learning path integration

## Commands

| Command | Description |
|---------|-------------|
| `/blog write <topic>` | Write a new blog post from scratch |
| `/blog rewrite <file>` | Optimize an existing blog post |
| `/blog analyze <file>` | Quality audit with 0-100 score |
| `/blog brief <topic>` | Generate a detailed content brief |
| `/blog outline <topic>` | Generate SERP-informed content outline |
| `/blog seo-check <file>` | Post-writing SEO validation |

**Note:** This is a streamlined version for Learn with Satya K. Additional commands
(calendar, strategy, schema, repurpose, geo, audit) can be added in future phases.

## Command Routing

When the user invokes `/blog`:

1. **Parse the command** to determine the sub-command
2. **If no sub-command given**, show this help message and ask which action they need
3. **Route to the appropriate agent:**
   - `write` → Use `task` tool with `agent_type: "blog-write"`
   - `rewrite` → Use `task` tool with `agent_type: "blog-write"` (with optimization mode)
   - `analyze` → Use `task` tool with `agent_type: "blog-analyze"`
   - `brief` → Generate content brief inline (research + outline requirements)
   - `outline` → Generate SERP-informed outline inline
   - `seo-check` → Run inline SEO validation checklist

## Usage Examples

### Write a New Post

```
/blog write "Understanding Transformer Architecture"
```

The blog-write agent will:
1. Ask clarifying questions (category, difficulty, series, target length)
2. Select appropriate template (likely "tutorial" or "how-to-guide")
3. Research statistics and sources
4. Generate outline for approval
5. Write complete post with all required elements
6. Save to `_posts/[category]/YYYY-MM-DD-[slug].md`

### Analyze Post Quality

```
/blog analyze _posts/ai/2026-03-10-transformer-architecture.md
```

Runs Python analyzer and returns:
- Overall score (0-100)
- 5-category breakdown
- AI content detection
- Prioritized recommendations

### Generate Content Brief

```
/blog brief "Kubernetes Deployment Strategies"
```

Creates a content brief with:
- Target keyword and search intent
- Competitor analysis (SERP top 10)
- Required statistics and sources
- Recommended word count
- Template selection
- Outline structure

### SEO Validation

```
/blog seo-check _posts/backend/2026-03-10-kubernetes-deployment.md
```

Checks:
- Title optimization (50-60 chars, keyword placement)
- Meta description (150-160 chars, includes stat)
- Heading structure (hierarchy, keywords)
- Internal linking (3-5 zones marked)
- Image alt text
- URL structure

## Jekyll Integration

All blog commands are adapted for Jekyll + Learn with Satya K structure:

**Required Front Matter:**
```yaml
---
title: "[Question-format title]"
date: YYYY-MM-DD
category: [ai|system-design|backend|devops|frontend|career|tools]
tags: [keyword1, keyword2, keyword3, keyword4]
excerpt: "[Brief excerpt, 100-120 chars]"
description: "[SEO description, 150-160 chars with stat]"
difficulty: [beginner|intermediate|advanced]
series: "[series-slug]"  # Optional
series_title: "[Series Name]"  # Optional
part: 1  # Optional
header:
  image: /assets/img/posts/[slug].jpg
  credit: Pixabay
  credit_url: [URL]
author: satya-k
---
```

**File Naming:** `_posts/[category]/YYYY-MM-DD-[slug].md`

**Category Validation:** Must be one of the 7 defined categories in `_data/categories.yml`

**Series Integration:** If part of a series, metadata references `_data/series.yml` (Phase 3)

## Workflow Integration

The blog commands integrate with the existing 5-phase content workflow:

**Option 1: Use `/blog write` (Full Automation)**
- Single command triggers entire workflow
- Handles all 5 phases internally
- Best for standard posts

**Option 2: Use Phased Approach (More Control)**
- Phase 1 (Discuss): `/blog brief [topic]` — Requirements gathering
- Phase 2 (Research): `blog-researcher` agent — Web search, statistics
- Phase 3 (Plan): `/blog outline [topic]` — SERP analysis, structure
- Phase 4 (Execute): `blog-writer` agent — Actual writing
- Phase 5 (Verify): `/blog analyze [file]` + `/blog seo-check [file]` — Quality check

## Content Templates (12 Types)

All templates are in `.github/agents/blog/templates/`:

1. **how-to-guide.md** — Step-by-step instructional content
2. **listicle.md** — Numbered list format ("Top 10...", "Best 5...")
3. **case-study.md** — Real-world example analysis
4. **comparison.md** — Side-by-side evaluation ("X vs Y")
5. **pillar-page.md** — Comprehensive topic coverage
6. **product-review.md** — Evaluation framework
7. **thought-leadership.md** — Opinion/perspective piece
8. **roundup.md** — Curated collection with expert quotes
9. **tutorial.md** — Hands-on technical walkthrough
10. **news-analysis.md** — Current event commentary
11. **data-research.md** — Original data presentation
12. **faq-knowledge.md** — Question-answer knowledge base

Templates are auto-selected by blog-write based on topic and intent.

## Specialized Agents (4)

Located in `.github/agents/blog/`:

1. **blog-researcher.md** — Research & sourcing specialist
   - Web search for statistics (8-12 per post)
   - Source validation (Tier 1-3 only)
   - Image sourcing (Pixabay/Unsplash/Pexels)
   - Competitor analysis

2. **blog-writer.md** — Content generation specialist
   - Answer-first formatting
   - 40-80 word paragraphs
   - 15-20 word sentences
   - Citation capsules
   - Natural readability

3. **blog-seo.md** — SEO optimization specialist
   - December 2025 Core Update compliance
   - E-E-A-T signals
   - Technical SEO
   - Schema markup planning

4. **blog-reviewer.md** — Quality assurance specialist
   - 5-category scoring
   - AI content detection
   - Readability analysis
   - Improvement recommendations

## Quality Scoring (100 Points)

Every post is scored across 5 categories:

| Category | Points | Focus |
|----------|--------|-------|
| Content Quality | 30 | Depth, readability, originality, structure |
| SEO Optimization | 25 | Title, headings, keywords, links, meta |
| E-E-A-T Signals | 15 | Author, citations, trust, experience |
| Technical Elements | 15 | Images, structured data, performance |
| AI Citation Readiness | 15 | Citability, Q&A format, entity clarity |

**Scoring Bands:**
- 90-100: Exceptional (publish immediately)
- 80-89: Strong (minor tweaks)
- 70-79: Acceptable (needs optimization)
- 60-69: Below Standard (significant work)
- <60: Rewrite (fundamental issues)

**Minimum to Publish:** 80+ (Strong band)

## Dual Optimization Strategy

Every article is optimized for both:

### Google Rankings
- December 2025 Core Update compliance
- E-E-A-T signals (Experience, Expertise, Authoritativeness, Trust)
- Reduced AI content visibility (pass AI detection)
- Original insights and data
- Proper technical SEO

### AI Citations (+340% Citation Rate)
- Answer-first formatting (direct answers in H2 opening paragraphs)
- Citation capsules (40-60 word self-contained passages)
- FAQ schema (+28% citations)
- Question-based headings (60-70% of H2s)
- Passage-level citability

## Success Metrics

A successful blog post has:

- ✅ Quality score 80+ (Strong or Exceptional band)
- ✅ Zero Critical issues
- ✅ AI detection: "Likely Human-written"
- ✅ Valid Jekyll front matter (all required fields)
- ✅ Correct category and file location
- ✅ 2,000-2,500 words (or as specified)
- ✅ 60-70% question headings
- ✅ TL;DR box after introduction
- ✅ 8+ unique statistics with sources
- ✅ 2-3 information gain markers
- ✅ Citation capsules in each major section
- ✅ 5-10 internal linking zones
- ✅ 4-6 images with credits
- ✅ FAQ section with 3-5 questions

## Next Steps After Writing

After `/blog write` creates a post:

1. **Download images** — Save all listed image URLs to `/assets/img/posts/`
2. **Resolve internal links** — Convert `[INTERNAL-LINK: ...]` placeholders to actual links
3. **Run quality check** — `/blog analyze [file]` to verify score
4. **Run SEO check** — `/blog seo-check [file]` for final validation
5. **Preview locally** — `jekyll serve` to view post
6. **Git commit** — Add, commit, and push to GitHub

## Tips for Best Results

### For Technical Posts (AI, Backend, Frontend, Tools)
- Include 2-4 code examples with comments
- Explain complex concepts with analogies
- Use diagrams and charts
- Link to official documentation
- Provide working, runnable code

### For Career Posts
- Include real salary data with sources
- Share personal experiences
- Interview quotes from professionals
- Action steps readers can take today
- Resource links (courses, books, tools)

### For Beginner-Level Posts
- Define all technical terms
- Use simple language (avoid jargon)
- More visual aids and examples
- Step-by-step breakdowns
- Link to foundational concepts

### For Series Posts
- Maintain consistent structure across all parts
- Reference previous parts with links
- Preview next part in conclusion
- Use consistent difficulty level
- Keep scores within ±5 points

---

**Ready to start?** Use `/blog write <topic>` to create your first post!

For more detailed information, see:
- `.github/agents/blog-write.md` — Complete writing workflow
- `.github/agents/blog-analyze.md` — Scoring system details
- `.github/agents/blog/templates/` — Content templates
- `docs/CLAUDE-BLOG-ANALYSIS.md` — Integration analysis
