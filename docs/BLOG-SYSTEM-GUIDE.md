# Blog System Complete Guide

## Overview

Learn with Satya K now has a complete professional blog system integrated with AI-powered content creation, quality scoring, LMS features, and progress tracking. This guide covers everything you need to know.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Blog Commands](#blog-commands)
3. [Content Creation Workflow](#content-creation-workflow)
4. [LMS Features](#lms-features)
5. [Quality Standards](#quality-standards)
6. [Jekyll Integration](#jekyll-integration)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Create Your First Blog Post

```bash
# Option 1: Automated (fastest)
/blog write "Understanding Transformer Architecture"

# Option 2: Phased (more control)
/blog brief "Understanding Transformer Architecture"
# Review the brief, then:
/blog outline [paste-brief-content]
# Review the outline, then:
/blog write [paste-outline-content]
```

### Check Quality Score

```bash
/blog analyze _posts/ai/2026-03-15-understanding-transformer-architecture.md
```

### Expected Output

- ✅ New post in `_posts/[category]/YYYY-MM-DD-[slug].md`
- ✅ Quality score 80+ (Strong or Exceptional)
- ✅ 8+ unique sources cited
- ✅ Answer-first formatting
- ✅ FAQ section included
- ✅ AI detection: "Likely Human-written"
- ✅ Series support (if applicable)

---

## Blog Commands

### 1. `/blog write` - Create New Post

**Purpose:** Complete end-to-end post creation with AI assistance

**Usage:**
```bash
# Automated workflow
/blog write "[topic]" --difficulty [beginner|intermediate|advanced] --category [category]

# With series
/blog write "[topic]" --series [series-id] --part [number]

# Examples
/blog write "Building a REST API with Express" --difficulty beginner --category backend
/blog write "Understanding Kubernetes Pods" --series k8s-fundamentals --part 3
```

**What it does:**
1. **Phase 1: Topic Understanding** - Analyzes topic, selects template, determines difficulty
2. **Phase 2: Research** - Finds 8+ Tier 1-3 sources, extracts key insights
3. **Phase 3: Outline** - Creates structured outline with citation zones
4. **Phase 4: Writing** - Generates complete post with answer-first formatting
5. **Phase 5: Quality Check** - Scores post, ensures 80+ threshold, checks AI detection

**Output:**
- New post file in `_posts/[category]/YYYY-MM-DD-[slug].md`
- Quality report (score breakdown, AI detection result)
- Recommendations for improvement (if < 80 score)

**Options:**
- `--difficulty` - beginner, intermediate, advanced (auto-detected if omitted)
- `--category` - ai, system-design, backend, devops, frontend, career, tools
- `--series` - Series ID from `_data/series.yml`
- `--part` - Part number in series
- `--skip-quality-check` - Skip Phase 5 (not recommended)

---

### 2. `/blog rewrite` - Improve Existing Post

**Purpose:** Enhance low-scoring posts to meet 80+ threshold

**Usage:**
```bash
/blog rewrite _posts/ai/2026-03-10-my-post.md

# With specific focus
/blog rewrite _posts/backend/api-design.md --focus seo
/blog rewrite _posts/devops/docker-basics.md --focus readability
```

**What it does:**
1. Analyzes existing post
2. Identifies weak areas (Content, SEO, E-E-A-T, Technical, AI Citation)
3. Rewrites sections to improve score
4. Preserves good sections
5. Re-scores to verify improvement

**Focus Options:**
- `content` - Improve depth, structure, engagement
- `seo` - Optimize title, headings, keywords, meta
- `eeat` - Add citations, author signals, experience
- `technical` - Add schema, optimize images, performance
- `ai-citation` - Improve citability, Q&A formatting
- `readability` - Simplify language, improve flow
- `all` (default) - Holistic rewrite

---

### 3. `/blog analyze` - Quality Scoring

**Purpose:** Score posts using 100-point system across 5 categories

**Usage:**
```bash
# Single post
/blog analyze _posts/ai/transformer-architecture.md

# All posts in category
/blog analyze --category ai

# Batch analysis
/blog analyze _posts/backend/*.md

# JSON output (for automation)
/blog analyze _posts/ai/my-post.md --format json
```

**Output:**
```
🎯 Quality Score: 87/100 (Strong)

📊 Category Breakdown:
├─ Content Quality: 27/30 (Exceptional)
├─ SEO Optimization: 22/25 (Strong)
├─ E-E-A-T Signals: 13/15 (Strong)
├─ Technical Elements: 12/15 (Strong)
└─ AI Citation Readiness: 13/15 (Strong)

🤖 AI Content Detection: Likely Human-written
   - Type-Token Ratio: 0.52 (Good vocabulary diversity)
   - AI Trigger Phrases: 2/17 (Acceptable)
   - Burstiness: 0.68 (Natural sentence variation)

✅ READY TO PUBLISH
```

**Score Bands:**
- **90-100:** Exceptional - Best-in-class content
- **80-89:** Strong - Publish-ready, competitive
- **70-79:** Acceptable - Minor improvements needed
- **60-69:** Below Standard - Significant revision required
- **< 60:** Rewrite - Does not meet quality bar

**Minimum Publish Threshold:** 80+

---

### 4. `/blog brief` - Create Content Brief

**Purpose:** Phase 1 only - generate topic brief for review

**Usage:**
```bash
/blog brief "Topic name"
/blog brief "Understanding Kubernetes Networking" --difficulty intermediate
```

**Output:**
```markdown
# Content Brief: Understanding Kubernetes Networking

## Topic Analysis
- **Primary Intent:** Educational tutorial
- **Target Difficulty:** Intermediate
- **Estimated Length:** 2,500-3,500 words
- **Template:** Tutorial

## Target Audience
Developers with basic Kubernetes knowledge who want to understand networking...

## Key Concepts to Cover
1. Pod networking fundamentals
2. Services and load balancing
...

## Success Criteria
- Explain CNI plugins with examples
- Provide working YAML manifests
...
```

**Next Steps:**
- Review and edit brief
- Run `/blog outline` with brief content to continue

---

### 5. `/blog outline` - Create Structured Outline

**Purpose:** Phase 3 only - generate detailed outline from brief

**Usage:**
```bash
/blog outline [paste-brief-content-here]
```

**Output:**
```markdown
# Outline: Understanding Kubernetes Networking

## 1. Introduction (200 words)
**Answer-first paragraph:**
Kubernetes networking enables pod-to-pod communication across nodes...

**Citation zone:** [Source 1: Official K8s docs on networking model]

## 2. Pod Networking Fundamentals (400 words)
### 2.1 Network Namespaces
...
```

**Next Steps:**
- Review outline structure
- Run `/blog write` with outline content to generate full post

---

### 6. `/blog seo-check` - SEO Validation

**Purpose:** Quick SEO audit without full quality scoring

**Usage:**
```bash
/blog seo-check _posts/ai/my-post.md
```

**Output:**
```
🔍 SEO Analysis

✅ Title: 58 characters (optimal 50-60)
✅ Meta Description: 155 characters (optimal 150-160)
✅ URL: /ai/understanding-transformer-architecture/ (clean, readable)
✅ H1: Matches title
✅ Headings: Proper hierarchy (H2 → H3)
⚠️  Primary Keyword: "transformer architecture" - density 1.8% (target 1-2%)
✅ Internal Links: 7 found
⚠️  External Links: 4 found (target 8+ unique sources)
✅ Image Alt Text: All images have descriptive alt text
✅ Schema Markup: BlogPosting schema detected

📊 SEO Score: 22/25 (Strong)

🎯 Recommendations:
1. Add 4 more unique external sources (Tier 1-3)
2. Consider adding FAQ schema (boosts AI citations +28%)
```

---

## Content Creation Workflow

### Approach 1: Automated (Recommended for Most Posts)

**Best for:**
- Standard tutorials, guides, listicles
- Posts where you trust AI to handle research
- When speed is priority

**Steps:**
1. Run `/blog write "[topic]"` with optional flags
2. Wait 15-20 minutes for complete post
3. Review generated content
4. Make manual edits if needed
5. Publish (if 80+ score) or rewrite (if < 80)

**Total Time:** ~20-30 minutes (including review)

---

### Approach 2: Phased (Recommended for Complex Topics)

**Best for:**
- Series content with dependencies
- Complex technical topics requiring expert review
- High-stakes publishing (company blog, thought leadership)
- When you want control at each phase

**Steps:**

#### Phase 1: Brief (5 min)
```bash
/blog brief "Topic name"
```
- Review topic analysis
- Confirm target audience
- Adjust key concepts if needed
- Verify success criteria

#### Phase 2: Research (External - 10 min)
- Blog system automatically finds sources
- You can supplement with domain-specific research
- Ensure 8+ Tier 1-3 sources

#### Phase 3: Outline (5 min)
```bash
/blog outline [paste-brief]
```
- Review structure and flow
- Adjust heading hierarchy
- Mark citation zones
- Plan internal links

#### Phase 4: Writing (15 min)
```bash
/blog write [paste-outline]
```
- AI generates full content
- Review answer-first paragraphs
- Verify citation quality
- Check code examples (if technical post)

#### Phase 5: Quality Check (5 min)
```bash
/blog analyze [post-file]
```
- Review score breakdown
- Check AI detection result
- Address any weak categories
- Rewrite if < 80 score

**Total Time:** ~40-50 minutes (more control, higher quality)

---

### Series Workflow

For multi-part learning series:

1. **Define series** in `_data/series.yml`:
```yaml
- id: kubernetes-fundamentals
  title: Kubernetes Fundamentals Series
  category: devops
  description: Master Kubernetes from basics to production
  difficulty: intermediate
  total_parts: 6
  posts:
    - slug: k8s-architecture-overview
      part: 1
      title: "Part 1: Architecture Overview"
    - slug: pods-and-containers
      part: 2
      title: "Part 2: Pods and Containers"
```

2. **Create each part** with series context:
```bash
/blog write "Kubernetes Architecture Overview" --series kubernetes-fundamentals --part 1
/blog write "Pods and Containers" --series kubernetes-fundamentals --part 2
```

3. **Navigation auto-generated** - Previous/Next buttons, progress bar, parts list

4. **Prerequisites** - Each post can reference previous parts:
```yaml
prerequisites:
  - kubernetes-fundamentals-1
  - docker-basics
```

---

## LMS Features

### Learning Progress Tracking

**User Experience:**
1. User reads a post
2. When they scroll to 80%, post is auto-marked complete
3. Progress saved in browser localStorage
4. View all progress at `/progress/`

**Developer Integration:**
```html
<!-- Already integrated in _layouts/post.html -->
<!-- Automatically tracks completion when user reaches 80% scroll -->
```

**Progress Dashboard** (`/progress/`):
- Total posts completed
- Series completion percentage
- Estimated learning time
- Reset progress button

### Series Navigation

**Components:**
- **Progress bar** - Visual completion percentage
- **Previous/Next buttons** - Navigate series sequentially
- **Parts list** - Expandable list of all parts (shows ✅ for completed)
- **Series badge** - Shows "Part X of Series" on post

**Example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━ 33% Complete (2/6 parts)

[← Previous: Architecture Overview]  [Next: Services & Networking →]

Series Parts
├─ ✅ Part 1: Architecture Overview
├─ ✅ Part 2: Pods and Containers  
├─ 📍 Part 3: Deployments (You are here)
├─ Part 4: Services & Networking
├─ Part 5: Storage & ConfigMaps
└─ Part 6: Production Best Practices
```

### Difficulty-Based Optimization

**Automatic Adjustments:**

| Difficulty | Word Count | Reading Level | Code Examples | Depth |
|-----------|-----------|---------------|---------------|-------|
| Beginner | 1,500-2,000 | Grade 8-10 | Simple, commented | Fundamental |
| Intermediate | 2,000-3,000 | Grade 10-12 | Production-ready | Practical |
| Advanced | 3,000-4,500 | College+ | Complex, optimized | Deep dive |

**Reading Level Enforcement:**
- Flesch Reading Ease: 60-70 (beginner), 50-60 (intermediate), 40-50 (advanced)
- Gunning Fog Index: 8-10 (beginner), 10-12 (intermediate), 12-14 (advanced)

### Interactive Elements

**Code Blocks with Copy Button:**
```html
<!-- Automatically added by syntax highlighter -->
```

**Collapsible Sections:**
```markdown
<details>
<summary>Advanced: Performance Optimization</summary>

Deep dive content for advanced readers...
</details>
```

**Embedded Demos:**
```markdown
<!-- CodeSandbox, JSFiddle, Repl.it embeds -->
<iframe src="..."></iframe>
```

---

## Quality Standards

### Minimum Requirements (80+ Score)

#### Content Quality (30 points)
- ✅ **Depth:** Comprehensive coverage, 1,500+ words
- ✅ **Readability:** Flesch score 50-70, clear structure
- ✅ **Originality:** Personal insights, real examples
- ✅ **Structure:** Logical flow, proper headings
- ✅ **Engagement:** Actionable takeaways, code examples
- ✅ **Grammar:** Error-free, professional tone

#### SEO Optimization (25 points)
- ✅ **Title:** 50-60 characters, keyword-optimized
- ✅ **Headings:** H2-H6 hierarchy, keyword-rich
- ✅ **Keywords:** Natural density (1-2%), semantic variations
- ✅ **Links:** 5-10 internal, 8+ external (Tier 1-3)
- ✅ **Meta:** Description 150-160 chars, category tags
- ✅ **URL:** Clean, readable, category-based

#### E-E-A-T Signals (15 points)
- ✅ **Author:** Profile with expertise indicators
- ✅ **Citations:** 8+ unique Tier 1-3 sources
- ✅ **Trust:** Official docs, academic papers, reputable blogs
- ✅ **Experience:** Personal examples, "I've found", "In my work"

#### Technical Elements (15 points)
- ✅ **Schema:** BlogPosting JSON-LD
- ✅ **Images:** 4-6 with descriptive alt text
- ✅ **Structured Data:** FAQ schema (if applicable)
- ✅ **Performance:** Optimized images, lazy loading

#### AI Citation Readiness (15 points)
- ✅ **Citability:** Self-contained passages (40-60 words)
- ✅ **Q&A Format:** Question-based headings, direct answers
- ✅ **Entity Clarity:** Proper nouns, definitions, context
- ✅ **Stats:** Data points in opening paragraphs

### Source Tiers

| Tier | Examples | Citation Value |
|------|----------|---------------|
| Tier 1 | Official docs, government, academic papers | High authority |
| Tier 2 | Major tech companies (Google, Microsoft, AWS), IEEE | Strong authority |
| Tier 3 | Reputable blogs (Martin Fowler, CSS-Tricks), MDN | Moderate authority |
| Tier 4 | General blogs, forums, Reddit | Low authority (avoid) |

**Minimum:** 8 unique Tier 1-3 sources per post

### AI Content Detection

**Pass Criteria:**
- Type-Token Ratio (TTR): 0.40-0.65 (vocabulary diversity)
- AI Trigger Phrases: < 5 out of 17 phrases
- Burstiness: > 0.50 (varied sentence lengths)

**Result:** "Likely Human-written"

**Red Flag Phrases (avoid):**
- "Delve into"
- "In today's digital landscape"
- "Leverage"
- "Seamlessly"
- "It's important to note that"
- [See full list in analyzer script]

---

## Jekyll Integration

### Front Matter Schema

```yaml
---
layout: post
title: "Understanding Transformer Architecture"  # 50-60 chars
date: 2026-03-15 10:00:00
category: ai  # One of 7 categories
tags: [deep-learning, nlp, transformers, attention-mechanism]  # 4-6 tags
excerpt: "Learn how transformer models revolutionized NLP through attention mechanisms"
description: "Complete guide to transformer architecture: attention, encoders, decoders, and modern implementations"  # SEO description
difficulty: intermediate  # beginner, intermediate, advanced
image: /assets/img/posts/transformer-architecture.jpg
header:
  credit: "Pixabay"
  credit_url: "https://pixabay.com/..."
author: satya-k
reading_time: 12
series: deep-learning-fundamentals  # Optional
series_title: "Deep Learning Fundamentals"  # Optional
part: 3  # Optional
total_parts: 5  # Optional
prerequisites:  # Optional
  - neural-networks-basics
  - attention-mechanism
---

[Content here]
```

### Directory Structure

```
_posts/
├── ai/
│   ├── 2026-03-15-understanding-transformer-architecture.md
│   └── 2026-03-16-building-gpt-from-scratch.md
├── system-design/
│   ├── 2026-03-14-distributed-caching-strategies.md
│   └── 2026-03-17-event-driven-architecture.md
├── backend/
├── devops/
├── frontend/
├── career/
└── tools/
```

### Series Data (`_data/series.yml`)

```yaml
- id: deep-learning-fundamentals
  title: Deep Learning Fundamentals
  category: ai
  description: Master neural networks from perceptrons to transformers
  difficulty: intermediate
  total_parts: 5
  posts:
    - slug: neural-networks-basics
      part: 1
      title: "Part 1: Neural Networks Basics"
    - slug: backpropagation-explained
      part: 2
      title: "Part 2: Backpropagation Explained"
    - slug: understanding-transformer-architecture
      part: 3
      title: "Part 3: Understanding Transformer Architecture"
```

### Category Data (`_data/categories.yml`)

```yaml
- slug: ai
  title: Artificial Intelligence
  display_name: AI & Machine Learning
  description: Master LLMs, ML fundamentals, RAG systems...
  icon: 🤖
  color: "#8B5CF6"
  order: 1
```

### Components

**Difficulty Badge:**
```liquid
{% include difficulty-badge.html difficulty=page.difficulty %}
```

**Category Badge:**
```liquid
{% include category-badge.html category=page.category %}
```

**Series Navigation:**
```liquid
{% if page.series %}
  {% include series-navigation.html %}
{% endif %}
```

**Image Credit:**
```liquid
{% include image-credit.html credit=page.header.credit url=page.header.credit_url %}
```

**Quality Score Badge (optional):**
```liquid
{% include quality-score-badge.html score=85 %}
```

---

## Troubleshooting

### Low Quality Score

**Problem:** Post scores < 80

**Solutions:**

1. **Content Quality Low (< 24/30)**
   - Increase depth: Add more sections, examples, explanations
   - Improve structure: Use clear headings, logical flow
   - Add engagement: Code examples, visuals, takeaways
   - Check grammar: Run through Grammarly or similar

2. **SEO Optimization Low (< 20/25)**
   - Optimize title: 50-60 chars, keyword at start
   - Fix headings: Use H2-H6 hierarchy, keyword variations
   - Add links: 5-10 internal, 8+ external (Tier 1-3)
   - Write meta description: 150-160 chars, compelling

3. **E-E-A-T Signals Low (< 12/15)**
   - Add more sources: Target 10+ unique Tier 1-3
   - Include author experience: "In my work...", "I've found..."
   - Cite official docs: Link to authoritative sources

4. **Technical Elements Low (< 12/15)**
   - Add images: 4-6 with descriptive alt text
   - Add FAQ schema: 3-5 Q&A pairs
   - Check BlogPosting schema: Verify JSON-LD

5. **AI Citation Low (< 12/15)**
   - Answer-first paragraphs: 40-60 words with stats
   - Question headings: "How does X work?" format
   - Citation capsules: Self-contained 40-60 word passages

**Rewrite Command:**
```bash
/blog rewrite _posts/ai/my-post.md --focus [weak-category]
```

---

### AI Detection Fails

**Problem:** "Likely AI-generated" result

**Solutions:**

1. **Reduce AI Trigger Phrases**
   - Replace "delve into" → "explore", "examine"
   - Replace "leverage" → "use", "utilize"
   - Replace "seamlessly" → remove or rephrase
   - Avoid "It's important to note", "In today's digital landscape"

2. **Increase Vocabulary Diversity (TTR)**
   - Use synonym variations
   - Avoid repetitive phrasing
   - Mix sentence structures
   - Add domain-specific terminology

3. **Increase Burstiness**
   - Vary sentence lengths (short, medium, long)
   - Mix simple and complex sentences
   - Use fragments occasionally for emphasis
   - Break up long paragraphs

**Manual Edit:**
- Read post aloud - does it sound natural?
- Add personal anecdotes
- Use contractions ("it's", "you'll")
- Include questions and direct address ("you", "your")

---

### Series Navigation Not Showing

**Problem:** Series navigation missing on post page

**Checklist:**

1. **Front Matter:**
   ```yaml
   series: my-series-id
   part: 1
   ```

2. **Series Data (`_data/series.yml`):**
   ```yaml
   - id: my-series-id  # Must match front matter
     title: My Series Title
     total_parts: 5
     posts:
       - slug: my-post-slug  # Must match post filename
         part: 1
   ```

3. **Post Layout:** Includes series-navigation.html component (already integrated)

4. **Jekyll Rebuild:** Run `bundle exec jekyll serve` to regenerate

---

### Progress Not Tracking

**Problem:** Posts not marked complete when scrolling

**Checklist:**

1. **Script Loaded:**
   - Check `assets/js/learning-progress-tracker.js` exists
   - Verify post layout includes script tag (already integrated)

2. **Browser Console:**
   - Open DevTools → Console
   - Look for "✅ Post marked as complete: [slug]" message
   - Check for JavaScript errors

3. **localStorage:**
   - Open DevTools → Application → Local Storage
   - Check for `learn-with-satya-progress` key
   - Data format: `{"posts": {...}, "series": {...}}`

4. **Clear Cache:**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Clear localStorage: `localStorage.clear()` in console

---

### Build Errors

**Problem:** Jekyll build fails

**Common Issues:**

1. **Invalid Front Matter:**
   - Check YAML syntax: proper indentation, quotes, colons
   - Validate with [YAML Lint](http://www.yamllint.com/)
   - Common errors: unescaped quotes, missing colons

2. **Missing Category:**
   - Category must be one of 7 defined in `_data/categories.yml`
   - Check spelling: `ai`, not `AI` or `artificial-intelligence`

3. **Invalid Series Reference:**
   - Series ID in front matter must exist in `_data/series.yml`
   - Post slug must be in series.posts array
   - Part number must match series.posts[].part

4. **Image Path:**
   - Use absolute paths: `/assets/img/posts/image.jpg`
   - Or relative to site root: `{{ site.baseurl }}/assets/img/...`
   - Check file exists

**Debug:**
```bash
bundle exec jekyll build --trace  # Shows full error stack
bundle exec jekyll serve --verbose  # Shows build warnings
```

---

### Python Analyzer Errors

**Problem:** `/blog analyze` fails

**Solutions:**

1. **Dependencies Missing:**
   ```bash
   pip install textstat beautifulsoup4 nltk pyphen
   ```

2. **NLTK Data:**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

3. **File Not Found:**
   - Check file path: must be relative to repo root
   - Use forward slashes: `_posts/ai/my-post.md` (not backslashes)

4. **Encoding Issues:**
   - Ensure files are UTF-8 encoded
   - Remove special characters from filenames

**Manual Run:**
```bash
python scripts/blog/analyze_blog.py _posts/ai/my-post.md --format markdown
```

---

## Next Steps

### Phase 4 Remaining: Advanced LMS Features

- [ ] **Learning Path Graph** - Visual prerequisite tree
- [ ] **Quiz Questions** - Auto-generated from content
- [ ] **Certificate Generation** - On series completion
- [ ] **Discussion Integration** - Comments, Q&A

### Phase 5: Testing & Polish

- [ ] **Test Build** - `bundle exec jekyll serve`
- [ ] **Create Example Posts** - 1 per category (7 total)
- [ ] **Test Series Navigation** - Create 3-part sample series
- [ ] **Test Progress Tracking** - Verify localStorage, dashboard
- [ ] **Mobile Responsiveness** - Test on phone/tablet
- [ ] **Performance Audit** - Lighthouse score

### Content Roadmap

1. **AI Category:**
   - [ ] Transformer Architecture (Part 1)
   - [ ] Attention Mechanisms (Part 2)
   - [ ] BERT vs GPT (Part 3)

2. **System Design Category:**
   - [ ] Distributed Caching
   - [ ] Event-Driven Architecture
   - [ ] Rate Limiting Strategies

3. **Backend Category:**
   - [ ] Building REST APIs
   - [ ] Authentication & JWT
   - [ ] Database Optimization

---

## Resources

- **Full Command Reference:** `docs/BLOG-COMMANDS.md`
- **Workflow Integration:** `docs/BLOG-WORKFLOW-INTEGRATION.md`
- **Original Analysis:** `docs/CLAUDE-BLOG-ANALYSIS.md`
- **PRD:** `.github/docs/PRD.md`
- **TRD:** `.github/docs/TRD.md`

---

## Support

For issues or questions:
1. Check this guide first
2. Review troubleshooting section
3. Check GitHub Issues
4. Consult original claude-blog docs (in `temp-claude-blog/`)

---

**Last Updated:** March 2026  
**Version:** 1.0.0  
**Status:** Phase 1-3 Complete, Phase 4-5 In Progress
