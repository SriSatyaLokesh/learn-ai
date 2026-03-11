# Copilot Instructions for Learn with Satya K

## ⚠️ MANDATORY GIT WORKFLOW - NO EXCEPTIONS

**Every task, change, or feature MUST follow this workflow. No direct commits to main.**

**📖 Full Guide**: [Git Workflow with GitHub CLI Skill](./.github/skills/git-workflow-github-cli/SKILL.md)  
**Reference**: For detailed commands, troubleshooting, and GitHub CLI setup

### Git Workflow (Enforce for ALL Tasks)

```
1. Create GitHub Issue → 2. Create Branch → 3. Make Changes → 4. Create PR → 5. Link PR to Issue → 6. Merge to Main
```

#### Complete Workflow Steps

**For full details on each step, see [Git Workflow Skill](./skills/git-workflow-github-cli/SKILL.md)**

**1. Create GitHub Issue**
```bash
gh issue create --title "fix: Brief description" --body "Detailed description"
# Returns: https://github.com/SriSatyaLokesh/learn-with-satya/issues/42
```

**2. Create Feature Branch**
```bash
# Format: <type>/<issue-number>-<description>
git checkout -b fix/42-image-paths-baseurl
```

**3. Implement & Test Locally**
```bash
# Make your changes, then verify:
bundle exec jekyll build --future
# Exit code 0 = success, 1 = errors
```

**4. Commit with Issue Reference**
```bash
git add .
git commit -m "fix: Add baseurl to image paths

- Updated placeholder paths
- Fixed fallback images
Resolves #42"  # Keywords: Fixes, Resolves, Closes all work
```

**5. Push Branch to Remote**
```bash
git push origin fix/42-image-paths-baseurl
```

**6. Create Pull Request (⚠️ MUST INCLUDE "Fixes #X")**
```bash
# CRITICAL: PR body MUST start with "Fixes #42" to auto-close issue
gh pr create \
  --title "fix: Add baseurl to image paths" \
  --body "Fixes #42

## Changes
- Updated all image paths to include baseurl filter

## Testing
- [x] Local build passes
- [x] No console errors" \
  --base main
# Returns: https://github.com/SriSatyaLokesh/learn-with-satya/pull/3
```

**7. Assign Reviewer**
```bash
gh pr edit 3 --add-reviewer SriSatyaLokesh
```

**8. Approve PR**
```bash
gh pr review 3 --approve
# Note: You can't approve your own PR - this is normal
```

**9. Merge PR**
```bash
# Squash merge (recommended for smaller fixes)
gh pr merge 3 --squash --delete-branch

# Output shows: ✓ Merged + Issue auto-closes
```

**10. Verify on Main**
```bash
git checkout main
git log --oneline -3  # Verify merge commit is present
```

#### Workflow Rules

**✅ ALWAYS:**
- Create issue FIRST for any task (bug fix, feature, content, refactor)
- Create branch from main before making changes
- **Include "Fixes #X" in PR body to auto-close issue** (most critical!)
- Write descriptive commit messages with issue reference
- Test changes locally before pushing
- Delete branch after merge

**❌ NEVER:**
- Commit directly to main branch
- Push changes without an issue
- Create PR without "Fixes #X" (issues stay open)
- Merge without testing
- Leave unmerged branches hanging

**🔑 THE ONE THING THAT STOPPED ISSUES AUTO-CLOSING**:
- PR #1 merged but Issue #2 stayed open
- Root cause: PR body didn't include "Fixes #2" keyword
- Fix: Always start PR body with exactly `Fixes #<issue-number>`
- Result: Issue auto-closes when PR merges + GitHub links them

See [Skill: Git Workflow with GitHub CLI](./skills/git-workflow-github-cli/SKILL.md) for complete details, all commands, troubleshooting, and GitHub CLI setup.

#### Branch Naming Convention

| Type | Format | Example |
|------|--------|---------|
| Bug fix | `fix/<issue>-<description>` | `fix/42-css-loading-github-pages` |
| New feature | `feature/<issue>-<description>` | `feature/23-add-search-functionality` |
| Blog post | `content/<issue>-<post-slug>` | `content/15-transformer-architecture` |
| Documentation | `docs/<issue>-<doc-name>` | `docs/8-update-readme` |
| Styling | `style/<issue>-<component>` | `style/31-callout-boxes` |
| Refactor | `refactor/<issue>-<area>` | `refactor/19-series-navigation` |
| Tests | `test/<issue>-<feature>` | `test/12-series-progress` |
| Chores | `chore/<issue>-<task>` | `chore/5-update-dependencies` |

#### Issue Template

```markdown
**Title:** [Type] Brief description

**Description:**
What needs to be done and why?

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tested locally
- [ ] Documentation updated (if needed)

**Related:**
- Links to related issues or PRs
```

#### When User Requests a Task

**Copilot MUST follow all 10 steps** (see complete workflow above):

1. ✅ Create GitHub issue
2. ✅ Create feature branch with proper naming
3. ✅ Implement changes and test locally
4. ✅ Commit with issue reference ("Resolves #X")
5. ✅ Push branch to remote
6. ✅ Create PR **with "Fixes #X" in body** (auto-closes issue on merge)
7. ✅ Assign reviewer (you)
8. ✅ Approve PR (if not self-approval)
9. ✅ Merge with squash and delete branch
10. ✅ Verify on main branch

**Example Response to User Request:**
```
I'll fix the image paths issue. Following the 10-step Git workflow:

1. ✅ Created issue #42: "fix: Image paths missing baseurl"
2. ✅ Created branch: fix/42-image-paths-baseurl
3. ✅ Updated all image src paths to include {{ site.baseurl }}
4. ✅ Local build passes (1.25s, no errors)
5. ✅ Committed: "fix: Add baseurl to image paths (Resolves #42)"
6. ✅ Pushed to origin
7. ✅ Created PR #3 with "Fixes #42" in body
8. ✅ Assigned you as reviewer
9. ✅ Approved PR #3
10. ✅ Merged PR #3 with squash (branch deleted, issue auto-closed)

All done! Changes live on main and deployed to GitHub Pages. Issue #42 closed. 🚀
```

**For detailed commands and troubleshooting:**  
👉 **[Read: Git Workflow with GitHub CLI Skill](./skills/git-workflow-github-cli/SKILL.md)**

---

## 🚀 Quick Start - Content Creation Workflow

**Every blog post follows this 5-phase workflow:**

```
/start-issue → /discuss → /research → /plan → /execute → /verify
```

**📖 Full guide**: [`docs/WORKFLOW.md`](../docs/WORKFLOW.md)

**Common commands**:
- `/start-issue` - Begin new content (creates branch + brief)
- `/discuss` - Define requirements
- `/research` - Gather sources
- `/plan` - Create SEO & outline
- `/execute` - Write content
- `/verify` - Validate & deploy
- `/status` - Check progress

**⚠️ Phase gates**: Each phase validates prior phases complete. Never skip phases!

---

## 📝 Blog Creation Commands

**NEW: Professional blog creation system with quality scoring**

```
/blog write <topic>     - Write new post with template selection
/blog analyze <file>    - Quality audit (0-100 score, 5 categories)
/blog brief <topic>     - Generate content brief
/blog outline <topic>   - SERP-informed outline
/blog seo-check <file>  - Post-writing SEO validation
/blog rewrite <file>    - Optimize existing post
```

**Features:**
- **12 content templates** (auto-selected): how-to, listicle, case study, comparison, tutorial, etc.
- **5-category quality scoring** (100 points): Content, SEO, E-E-A-T, Technical, AI Citations
- **Dual optimization**: Google rankings (Dec 2025 Update) + AI citations (+340% rate)
- **AI detection**: Flags AI-generated patterns, ensures human-written quality
- **Jekyll integration**: Category/series support, difficulty levels, front matter validation

**Quality Standards:**
- Minimum publish score: **80+ (Strong band)**
- 8+ unique sources (Tier 1-3)
- Answer-first formatting (40-60 word opening paragraphs)
- Citation capsules for AI extraction
- 2-3 information gain markers (original data, experience, insights)
- FAQ section with 3-5 questions
- 5-10 internal linking zones

**Quick Example:**
```bash
# Write a new post
/blog write "Understanding Transformer Architecture"
# (Answers questions: category, difficulty, series, length)
# (Auto-selects template, researches, generates outline, writes complete post)
# (Saves to: _posts/ai/2026-03-10-transformer-architecture.md)

# Check quality
/blog analyze _posts/ai/2026-03-10-transformer-architecture.md
# (Returns score: 87/100 [Strong], breakdown, recommendations)
```

**📖 Full guide**: [`.github/prompts/blog.prompt.md`](.github/prompts/blog.prompt.md)

### Blog Writing Style Guidelines

**CRITICAL: Avoid AI-Written Patterns**

❌ **DO NOT USE:**
- Emojis in blog content (🚀, ✅, 📊, etc.) — Use plain text only
- Excessive dashes and bullet points that signal AI writing
- Overly structured lists with "Here's what you need to know:" intros
- Phrases like "Let's dive in," "In this article," "At the end of the day"
- Section breaks with `---` horizontal rules — Use headings only

✅ **DO USE:**
- Natural, conversational language
- Direct statements without meta-commentary
- Code examples and practical demonstrations
- Real-world scenarios and concrete examples
- Data and statistics from credible sources

**Spacing & Typography:**
- Tight paragraph spacing (no excessive line breaks)
- Smaller heading sizes (H2: 27px, H3: 21px on desktop)
- Lists: 6px margin between items, 10-15px between list and next element
- Paragraphs: 10-15px margin between them
- No decorative dividers — Let content flow naturally

**Content Structure:**
- Start with value immediately (no fluff intros)
- Use headings to organize, not to create visual breaks
- Keep related content grouped together
- Use code blocks for technical examples
- Tables for comparisons, not bullet lists

**Markdown Formatting Rules:**
- **Line breaks**: Use blank line between paragraphs OR 2 spaces at end of line for line break
- **Bullet points**: Always use proper markdown lists (-, *, or +) with blank lines before/after
- **Never**: Single newline without 2 trailing spaces (renders as same line)
- **Example**:
  ```markdown
  Wrong:
  Item 1
  Item 2
  Item 3
  
  Right:
  - Item 1
  - Item 2
  - Item 3
  ```

**Liquid Syntax Escaping:**
- **CRITICAL**: Jekyll processes `{{ }}` and `{% %}` as Liquid template syntax
- **Docker/Jinja2/Helm templates**: Wrap in `{% raw %}...{% endraw %}` tags
- **Common patterns to escape**:
  - Docker format strings: `{{.Names}}`, `{{.Ports}}`, `{{.ID}}`
  - Jinja2 templates: `{{ variable }}`, `{% if condition %}`
  - Helm/K8s templates: `{{ .Values.image }}`
  - Go templates: `{{ range .Items }}`
- **Example fix**:
  ```markdown
  Wrong:
  docker ps --format "{{.Names}}"
  
  Right:
  {% raw %}
  docker ps --format "{{.Names}}"
  {% endraw %}
  ```
- **When to escape**: Any code block containing double curly braces or `{%`
- **Error indicators**: "Liquid syntax error", "[:dot, \".\"] is not a valid expression"

---

## 🎓 LMS Features

**Learning progress tracking** (localStorage-based):
- Auto-marks posts complete at 80% scroll
- Series completion percentage
- Progress dashboard at `/progress/`
- Completion badges and notifications

**Series navigation**:
- Previous/Next buttons with visual design
- Progress bar showing completion (e.g., "33% - 2/6 parts")
- Expandable parts list with ✅ indicators
- Series badge on posts ("Part X of Series")

**Difficulty-based optimization**:
- Beginner: 1,500-2,000 words, Grade 8-10, simple examples
- Intermediate: 2,000-3,000 words, Grade 10-12, production code
- Advanced: 3,000-4,500 words, College+, complex optimizations

**Components** (auto-integrated in post layout):
- `difficulty-badge.html` - Color-coded difficulty (🌱 beginner, 📚 intermediate, 🚀 advanced)
- `category-badge.html` - Category with emoji and color
- `series-navigation.html` - Complete series UI with progress
- `image-credit.html` - Attribution for Pixabay/Unsplash/Pexels
- `quality-score-badge.html` - Optional quality score display

**Progress tracking** (`assets/js/learning-progress-tracker.js`):
- Tracks scroll completion (80% = complete, 100% = badge)
- Stores in `localStorage` key: `learn-with-satya-progress`
- Shows completion button at end of posts
- Dashboard shows total stats and series breakdowns

**📖 Full guide**: [`docs/BLOG-SYSTEM-GUIDE.md`](../docs/BLOG-SYSTEM-GUIDE.md)

---

## Project Overview

**Learn with Satya K** is a Jekyll-based AI-powered learning blog system hosted on GitHub Pages. It's a developer-owned static site that functions as a lightweight Learning Management System (LMS) with structured learning series across AI, System Design, Backend Engineering, and more.

**Key Characteristics:**
- Content is generated through a multi-agent AI pipeline (Orchestrator → Research → SEO → Writer → Formatter)
- Organized into 7 categories with sequential learning series
- Static HTML output with client-side features (search, progress tracking)
- SEO-optimized with structured data and image attribution

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Static Site Generator | Jekyll 4.x | Markdown → HTML conversion with Liquid templates |
| Theme | Chirpy | Responsive design, dark mode, TOC, categories |
| Hosting | GitHub Pages | Free static hosting with auto-deploy on push |
| Search | Lunr.js | Client-side full-text search |
| AI Pipeline | Node.js + Claude API (sonnet-4-6) | Content generation via 5-agent system |
| Progress Tracking | localStorage | Client-side series completion tracking |
| Analytics | Plausible/Fathom | Privacy-first visitor analytics |

## Directory Structure

```
learn-with-satya/
├── _posts/
│   ├── ai/                    # AI category posts
│   ├── system-design/         # System Design posts
│   ├── backend/               # Backend Engineering posts
│   ├── devops/                # DevOps posts
│   ├── frontend/              # Frontend posts
│   ├── career/                # Career posts
│   └── tools/                 # Dev Tools posts
│
├── _data/
│   ├── series.yml             # Learning series metadata
│   └── categories.yml         # Category definitions
│
├── _layouts/
│   ├── post.html              # Post layout with series nav
│   ├── series.html            # Series index page
│   └── category.html          # Category landing page
│
├── _includes/
│   ├── image-credit.html      # Image attribution partial
│   ├── series-nav.html        # Prev/next navigation
│   ├── series-sidebar.html    # Learning path sidebar
│   ├── toc.html               # Table of contents
│   └── jsonld-article.html    # Schema.org structured data
│
├── assets/
│   ├── images/posts/          # Hero images by post slug
│   └── js/
│       ├── search.js          # Lunr.js search
│       ├── progress.js        # Post completion tracking
│       └── series-progress.js # Series completion calculator
│
├── agents/                    # AI agent system (excluded from build)
│   ├── orchestrator.js
│   ├── research.js
│   ├── seo.js
│   ├── writer.js
│   ├── formatter.js
│   └── config.js
│
├── _config.yml                # Jekyll configuration
├── Gemfile                    # Ruby dependencies
└── .github/
    ├── workflows/deploy.yml   # GitHub Actions deployment
    └── docs/                  # PRD and TRD documents
```

## Build, Test, and Deployment Commands

### Local Development

```bash
# Install dependencies
bundle install

# Serve site locally with auto-rebuild
bundle exec jekyll serve

# Serve with drafts and future posts
bundle exec jekyll serve --drafts --future

# Build for production
JEKYLL_ENV=production bundle exec jekyll build
```

### Agent System

```bash
# Run full content generation pipeline
node agents/run.js "Write Part 3 of AI Fundamentals on Transformer Architecture"

# With explicit overrides
node agents/run.js "Standalone post on Docker basics" --category devops --difficulty beginner

# Dry run (don't write file)
node agents/run.js "..." --dry-run
```

### Deployment

```bash
# Commit and push triggers automatic GitHub Pages deployment
git add .
git commit -m "feat(ai): add transformer-architecture post"
git push origin main
# Site live at https://yourusername.github.io/learn-with-satya/ in 1-3 minutes
```

## Front-Matter Specification

### Complete Front-Matter Template

**ALL posts MUST include this YAML structure:**

```yaml
---
title: "Understanding Transformer Architecture"
subtitle: "How attention mechanisms changed everything in AI"  # Optional
date: 2026-03-10 09:00:00 +0530
last_modified_at: 2026-03-10  # Optional

# Taxonomy
category: ai  # REQUIRED: Must match slug from _data/categories.yml
tags: [transformers, attention, deep-learning, nlp]  # REQUIRED: 3-7 lowercase hyphenated tags

# Series (OMIT both fields for standalone posts)
series: ai-fundamentals           # Series slug from _data/series.yml
series_title: "AI Fundamentals"   # Human-readable series name
part: 3                            # Unique part number within series

# Content metadata
excerpt: "A deep dive into how transformer models use self-attention to process sequences in parallel."  # REQUIRED: Max 250 chars
description: "Learn transformer architecture: self-attention, encoder-decoder structure, positional encoding, BERT and GPT."  # REQUIRED: 140-160 chars, includes primary keyword

# Hero image (author-provided)
header:
  image: /assets/images/posts/transformer-arch/hero.jpg
  image_credit: "Photo by John Doe on Unsplash"
  image_credit_url: "https://unsplash.com/photos/xyz"

# Learning metadata
difficulty: intermediate   # REQUIRED: beginner | intermediate | advanced
read_time: true
toc: true
toc_sticky: true

# Prerequisites (optional)
prerequisites:
  - title: "AI Fundamentals Part 2: Backpropagation"
    url: /ai/ai-fundamentals-part-2/

# SEO
seo:
  primary_keyword: "transformer architecture explained"  # REQUIRED
  secondary_keywords: [self-attention, encoder decoder, BERT, GPT]
  canonical_url: "https://yourusername.github.io/learn-with-satya/ai/transformer-architecture/"  # REQUIRED
---
```

### Front-Matter Field Rules

| Field | Type | Required | Rules |
|---|---|---|---|
| `title` | String | ✅ Yes | Include primary keyword. Max 70 chars. |
| `date` | DateTime | ✅ Yes | ISO format with timezone: `YYYY-MM-DD HH:MM:SS +HHMM` |
| `category` | String | ✅ Yes | Must match: `ai`, `system-design`, `backend`, `devops`, `frontend`, `career`, or `tools` |
| `tags` | Array | ✅ Yes | 3-7 lowercase hyphenated tags |
| `series` | String | If series post | Series slug from `_data/series.yml` |
| `series_title` | String | If `series` set | Human-readable series name |
| `part` | Integer | If `series` set | Unique part number (1, 2, 3...) |
| `excerpt` | String | ✅ Yes | 2-3 sentence summary. Max 250 chars. |
| `description` | String | ✅ Yes | SEO meta description. **140-160 chars.** Must include primary keyword. |
| `header.image_credit` | String | If image used | Full attribution with photographer and source |
| `difficulty` | Enum | ✅ Yes | One of: `beginner`, `intermediate`, `advanced` |
| `seo.primary_keyword` | String | ✅ Yes | Main target keyword for SEO |
| `seo.canonical_url` | URL | ✅ Yes | Absolute canonical URL |

## File Naming and Organization

### Post File Naming Convention

```
_posts/{category}/{YYYY-MM-DD}-{slug}.md
```

**Examples:**
- `_posts/ai/2026-03-10-transformer-architecture-explained.md`
- `_posts/system-design/2026-03-15-load-balancing-strategies.md`
- `_posts/backend/2026-03-20-rest-api-design-best-practices.md`

**Rules:**
- Date must match front-matter `date` field
- Slug must be kebab-case, max 60 characters
- Slug must NOT contain stop words (the, a, and, of, etc.)
- Category folder must match front-matter `category` field

### Permalink Structure

Jekyll generates URLs as: `/:categories/:title/`

**Example:** `https://yourusername.github.io/learn-with-satya/ai/transformer-architecture-explained/`

## Categories and Series

### 7 Defined Categories

| Slug | Display Name | Icon | Description |
|---|---|---|---|
| `ai` | Artificial Intelligence | 🤖 | LLMs, ML fundamentals, RAG, embeddings, AI agents |
| `system-design` | System Design | 🏗️ | Scalability, distributed systems, architecture patterns |
| `backend` | Backend Engineering | ⚙️ | APIs, databases, authentication, microservices |
| `devops` | DevOps & Infrastructure | 🚀 | CI/CD, Docker, Kubernetes, cloud deployment |
| `frontend` | Frontend & Web | 🎨 | Modern JS, React, performance, web standards |
| `career` | Career & Mindset | 🧠 | Developer growth, productivity, job hunting |
| `tools` | Dev Tools & Ecosystem | 🛠️ | IDEs, CLI tools, frameworks, boilerplate |

### Series Structure

Series metadata is defined in `_data/series.yml`:

```yaml
- id: ai-fundamentals              # Unique series slug
  title: "AI Fundamentals"         # Display name
  description: "From zero to understanding modern AI systems"
  category: ai                     # Parent category
  difficulty: beginner
  total_parts: 8                   # Update as posts are added
  cover_image: /assets/images/series/ai-fundamentals-cover.jpg
  posts:
    - part: 1
      slug: what-is-machine-learning
      title: "What is Machine Learning?"
    - part: 2
      slug: neural-networks-explained
      title: "Neural Networks Explained"
```

**When adding a series post:**
1. Ensure series exists in `_data/series.yml`
2. Add post entry to series `posts` array
3. Increment `total_parts` count
4. Use consistent `series` slug in front-matter

## AI Agent Content Pipeline

### 5-Agent Sequential Chain

The content generation pipeline transforms a topic idea into a complete Jekyll post:

```
Author Input → Orchestrator → Research → SEO → Writer → Formatter → Final .md File
```

| Agent | Role | Output |
|---|---|---|
| **Orchestrator** | Classifies category, series, difficulty, scope | Content brief (JSON) |
| **Research** | Web search for insights, statistics, sources | Research summary + URLs |
| **SEO & Strategy** | Title, slug, meta, outline, keywords, image queries | SEO blueprint (JSON) |
| **Writer** | Writes full post body following outline | Markdown draft |
| **Formatter** | Assembles front-matter, validates, writes file | Final `.md` in `_posts/{category}/` |

### AgentContext Data Contract

All agents read from and append to a cumulative `AgentContext` object:

```typescript
interface AgentContext {
  // Orchestrator
  topic: string;
  category: string;
  is_series: boolean;
  series_id?: string;
  part_number?: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  
  // Research Agent
  research_insights: string[];
  research_sources: { title: string; url: string }[];
  
  // SEO Agent
  title: string;
  slug: string;
  meta_description: string;
  outline: { h2: string; h3s: string[] }[];
  primary_keyword: string;
  secondary_keywords: string[];
  
  // Writer
  body_markdown: string;
  
  // Formatter
  final_frontmatter: string;
  final_filepath: string;
  validation_passed: boolean;
}
```

## Key Conventions

### Image Attribution

**All external images MUST include attribution:**

```markdown
![Alt text](https://images.unsplash.com/photo-xyz)
*Photo by [Photographer Name] on [Unsplash](https://unsplash.com/photos/xyz) — Unsplash License*
```

**Image sources allowed:**
- Unsplash (free tier with attribution)
- Wikimedia Commons (with attribution)

**Prohibited:** Getty Images, Shutterstock, or other restricted sources

### SEO Requirements

**Primary keyword must appear in:**
- Title (first 60 characters preferred)
- Meta description
- First paragraph of post
- At least one H2 heading

**Rules:**
- Keyword density ≤ 2% (no stuffing)
- Include 2-3 internal links to related posts
- Meta description: 140-160 characters exactly
- Slug: kebab-case, max 60 chars, no stop words

### Content Quality Standards

**Series posts:**
- Minimum 800 words
- Include "What's Next" section linking to next part
- Follow SEO-agent-generated outline structure

**Standalone posts:**
- Minimum 600 words
- Include "Key Takeaways" bulleted summary

**All posts:**
- Active voice throughout
- Developer-friendly tone: conversational but technically precise
- Include code blocks where relevant
- Table of contents for posts > 800 words

### Series Navigation

**Series posts automatically include:**
- Breadcrumb showing: Series Title > Part N
- Prev/Next buttons at bottom with part titles
- Series sidebar showing all parts with completion checkmarks
- Progress bar indicating current position

**Implemented via:**
- `_includes/series-nav.html` (prev/next)
- `_includes/series-sidebar.html` (full series list)
- `assets/js/series-progress.js` (completion tracking)

## Jekyll Configuration Essentials

### Key Settings in `_config.yml`

```yaml
# Permalink structure (DO NOT CHANGE)
permalink: /:categories/:title/

# Pagination
paginate: 12
paginate_path: "/page:num/"

# Markdown processor
markdown: kramdown
highlighter: rouge

# GitHub Pages whitelisted plugins
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-paginate
  - jekyll-toc
  - jekyll-relative-links

# Exclude agent system from build
exclude:
  - agents/
  - node_modules/
  - .env
  - "*.js"  # Root-level only
```

### Front-Matter Defaults

```yaml
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
```

## Common Workflows

### Creating a New Series Post

1. Verify series exists in `_data/series.yml` or add it
2. Run agent pipeline: `node agents/run.js "Write Part N of {series} on {topic}"`
3. Review generated file in `_posts/{category}/{date}-{slug}.md`
4. Source and place hero image in `assets/images/posts/{slug}/hero.jpg`
5. Update front-matter `header.image` path
6. Commit and push to deploy

### Creating a Standalone Post

1. Run agent: `node agents/run.js "Standalone post on {topic}" --category {category}`
2. Verify no `series`, `series_title`, or `part` fields in front-matter
3. Review and edit content
4. Add hero image if desired
5. Commit and push

### Adding a New Series

1. Edit `_data/series.yml` and add new series entry:
   ```yaml
   - id: new-series-slug
     title: "New Series Title"
     description: "Brief description"
     category: category-slug
     difficulty: beginner
     total_parts: 0  # Will increment
     posts: []
   ```
2. Create series posts using agent pipeline
3. Update `total_parts` as posts are added

---

## Content Creation Workflow

### 5-Phase Content Pipeline

Every blog post follows this structured workflow (adapted from Copilot Team Workflow):

```
/start-issue → /discuss → /research → /plan → /execute → /verify
```

| Phase | Command | Purpose | Agents Used |
|-------|---------|---------|-------------|
| **Setup** | `/start-issue` | Create branch and content brief | - |
| **1. Discuss** | `/discuss` | Define requirements (WHAT to write) | @discuss |
| **2. Research** | `/research` | Gather sources and insights | @research |
| **3. Plan** | `/plan` | Create SEO strategy and outline | @plan, @seo-planner |
| **4. Execute** | `/execute` | Write content and create final file | @writer, @formatter |
| **5. Verify** | `/verify` | Validate and prepare deployment | @verify |

### Starting New Content

**Always begin with:**
```
/start-issue
```

This will:
- Create feature branch (e.g., `content/CONTENT-042-transformer-architecture`)
- Create content brief at `docs/series/CONTENT-{id}-{slug}.md`
- Guide you through the 5 phases

**Never skip phases** — each phase validates the previous one is complete.

### Content Brief Tracking

All work-in-progress content is tracked in `docs/series/` with this structure:

```markdown
# Content Brief: {Title}

**Status**: 📝 In Progress

## Phase 1: Discuss ✅
[x] Complete

## Phase 2: Research 🔍
[x] Complete

## Phase 3: Plan 📋
[ ] In Progress

## Phase 4: Execute ⚡
[ ] Not Started

## Phase 5: Verify ✅
[ ] Not Started
```

### Quick Reference Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/start-issue` | Begin new content | Always first |
| `/discuss` | Define requirements | After start |
| `/research` | Gather sources | After discuss |
| `/plan` | Create outline + SEO | After research |
| `/execute` | Write content | After plan |
| `/verify` | Validate + deploy prep | After execute |
| `/status` | Check progress | Anytime |
| `/debug` | Troubleshoot issues | When stuck |

### Phase Gates (Critical!)

Each agent validates prior phases complete before proceeding. If you see:

> "Phase X must be complete first"

Go back and complete that phase. This prevents incomplete or low-quality content.

### Full Documentation

For complete workflow guide including troubleshooting, examples, and best practices:

**📖 Read: [`docs/WORKFLOW.md`](../docs/WORKFLOW.md)**

---

**Document Version:** 1.2 | **Last Updated:** January 2025 | **Source:** LearnHub PRD v1.0 & TRD v1.0 + Copilot Team Workflow (copilot-team-workflow)
