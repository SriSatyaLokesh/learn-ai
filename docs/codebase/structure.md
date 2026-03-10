# Learn with Satya K — Directory Structure

**Document:** Project Organization Reference  
**Last Updated:** March 2026  
**Status:** Foundation Phase

---

## High-Level Overview

```
learn-with-satya/
├── _posts/                 # Blog posts (organized by category)
├── _data/                  # YAML data files (series, categories)
├── _layouts/               # Jekyll post and page templates
├── _includes/              # Reusable template components
├── _sass/                  # SCSS stylesheets
├── _site/                  # Build output (generated, not committed)
├── assets/                 # CSS, JS, images
├── scripts/                # Utility scripts (blog analysis)
├── docs/                   # Project documentation
├── src/                    # Source files for Gulp processing
├── .github/                # GitHub workflows, instructions, skills
├── _authors/               # Author metadata
└── Root files              # _config.yml, Gemfile, package.json, etc.
```

---

## Detailed Directory Map

### `_posts/` — Blog Content
**Purpose:** All blog posts organized by category  
**Status:** Currently empty (awaiting Phase 4 content creation)

```
_posts/
├── ai/                     # AI & Machine Learning category
├── backend/                # Backend Engineering category
├── career/                 # Career Development category
├── devops/                 # DevOps & Cloud category
├── frontend/               # Frontend & Web category
├── system-design/          # System Design & Architecture category
└── tools/                  # Dev Tools & Ecosystem category
```

**File Naming:**
- Pattern: `YYYY-MM-DD-slug.md`
- Example: `2026-03-10-transformer-architecture-explained.md`
- Slug: kebab-case, max 60 chars, no stop words

**Front-Matter:**
Each post must include YAML front-matter with:
- `title`, `date`, `category`, `tags`
- `excerpt`, `description`
- `series`, `series_title`, `part` (if part of series)
- `difficulty`, `toc`, `read_time`
- `seo.primary_keyword`, `seo.canonical_url`

### `_data/` — Metadata Files
**Purpose:** Structured data for Jekyll templates

```
_data/
├── series.yml              # Learning series definitions
└── categories.yml          # Category metadata (icons, descriptions)
```

**series.yml Structure:**
```yaml
- id: transformer-series
  title: "Transformer Architecture Deep Dive"
  category: ai
  description: "..."
  difficulty: beginner
  total_parts: 5
  posts: []                 # Array of {slug, part, title}
```

**categories.yml Structure:**
```yaml
- slug: ai
  title: "Artificial Intelligence"
  display_name: "AI & Machine Learning"
  icon: "🤖"
  order: 1
```

### `_layouts/` — Page Templates
**Purpose:** Jekyll Liquid templates for rendering pages

```
_layouts/
├── post.html               # Individual blog post page
├── category.html           # Category index page
├── home.html               # Homepage
├── default.html            # Base layout wrapper
├── compress.html           # HTML compression (Jekyll)
└── [others]                # Minimal, contact, etc.
```

**Key Features Rendered:**
- Post metadata (date, reading time, author)
- Series navigation (prev/next)
- Table of contents
- Comments section
- Related posts

### `_includes/` — Reusable Components
**Purpose:** Partial templates injected into layouts

```
_includes/
├── header.html             # Top navigation bar
├── footer.html             # Footer with links
├── author.html             # Author info card
├── series-navigation.html  # Prev/Next series buttons [CUSTOM]
├── difficulty-badge.html   # Difficulty level badge [CUSTOM]
├── category-badge.html     # Category label with icon [CUSTOM]
├── image-credit.html       # Image attribution block [CUSTOM]
├── toc.html                # Table of contents
├── share.html              # Social share buttons
├── pagination-post.html    # Pagination controls
├── menu.html               # Mobile menu
└── [others]                # Comments, search, analytics, etc.
```

**[CUSTOM]**: Planned custom components for Learn with Satya K

### `_sass/` — Stylesheets
**Purpose:** SCSS files compiled to CSS

```
_sass/
├── jekflix.scss            # Main stylesheet imports
├── main.scss               # Base styles
├── _theme.scss             # Color variables, dark mode
├── _post.scss              # Post page specific styles
├── _header.scss            # Header/nav styles
├── _footer.scss            # Footer styles
├── _home.scss              # Homepage styles
├── _animations.scss        # Transitions, keyframes
├── _variables.scss         # Colors, spacing, fonts
├── _mixins.scss            # SCSS mixins
├── _normalize.scss         # CSS reset
└── [others]                # Typography, pagination, modals, etc.
```

**Build Process:**
- Gulp processes `src/yml/` → compiles to root `_config.yml`
- Jekyll compiles `_sass/` → generates `assets/css/main.css`

### `assets/` — Compiled Assets
**Purpose:** CSS, JavaScript, and images served to browser

```
assets/
├── css/
│   ├── main.css            # Compiled stylesheet (minified in prod)
│   └── highlight.css       # Code syntax highlighting
├── js/
│   ├── main.js             # Core site functionality (minified)
│   ├── search.js           # Lunr.js search implementation [CUSTOM]
│   ├── progress.js         # localStorage series progress tracking [CUSTOM]
│   └── series-progress.js  # Series completion calculator [CUSTOM]
├── images/
│   └── posts/              # Hero images by post slug
│       └── transformer-arch/
│           └── hero.jpg     # Example: post hero image
└── webfont/                # Custom fonts (if used)
```

**Image Organization:**
- Pattern: `assets/images/posts/{post-slug}/hero.jpg`
- Inline images: URLs to Unsplash/Wikimedia with attribution

### `src/` — Build Sources
**Purpose:** Pre-processed files for Gulp

```
src/
├── js/
│   ├── main/               # Main site JavaScript
│   │   ├── smoothscroll.js
│   │   ├── ouibounce.js
│   │   └── [others]
│   ├── preview/            # Preview widget libraries (color picker, etc.)
│   └── custom.js           # Site-specific scripts [CUSTOM]
└── yml/
    └── _config.yml         # Template for Jekyll configuration
```

**Gulp Pipeline:**
```
src/js/main/*.js → [concat] → [uglify] → assets/js/main.js
src/yml/_config.yml → [includes] → _config.yml
```

### `scripts/` — Utility Scripts
**Purpose:** Development and content analysis tools

```
scripts/
└── blog/
    └── analyze_blog.py     # Blog post quality analyzer
        │                   # 5-category 100-pt scoring system
        │                   # Content, SEO, E-E-A-T, Technical, AI Citation
        ├── Outputs JSON/Markdown/table reports
        ├── Detects AI-generated content patterns
        └── Optional: textstat, beautifulsoup4 dependencies
```

**Usage:**
```bash
python scripts/blog/analyze_blog.py <file>
python scripts/blog/analyze_blog.py <file> --format markdown --category seo
```

### `docs/` — Project Documentation
**Purpose:** PRD, TRD, workflow guides, and architecture docs

```
docs/
├── codebase/               # Codebase reference [THIS DIRECTORY]
│   ├── stack.md            # Tech stack summary
│   ├── structure.md        # Directory organization
│   ├── architecture.md     # System design & data flow
│   ├── conventions.md      # Coding standards
│   ├── integrations.md     # External services
│   ├── testing.md          # Testing strategy
│   └── concerns.md         # Known issues & technical debt
├── LearnHub_PRD.md         # Product Requirements Document
├── LearnHub_TRD.md         # Technical Requirements Document
├── WORKFLOW.md             # Copilot workflow integration guide
├── BLOG-SYSTEM-GUIDE.md    # Learning series & LMS features
├── BLOG-COMMANDS.md        # Blog creation commands (deprecated)
├── series/                 # Work-in-progress series briefs
│   └── CONTENT-***-*.md
├── posts/                  # Post planning & status
└── templates/              # Documentation templates
```

### `.github/` — GitHub Metadata & Configuration

```
.github/
├── workflows/              # GitHub Actions CI/CD
│   └── acquire-codebase-knowledge.md
├── instructions/           # Developer rules & patterns
│   ├── developer-guide.instructions.md
│   ├── backend.instructions.md
│   ├── frontend.instructions.md
│   ├── playwright-typescript.instructions.md
│   ├── testing.instructions.md
│   └── [others]            # 10+ instruction files
├── skills/                 # AI agent skill definitions
│   ├── acquire-codebase-knowledge/
│   ├── documentation-writer/
│   ├── playwright-automation-fill-in-form/
│   ├── subagent-driven-development/
│   └── [others]            # 8+ skill definitions
├── docs/                   # Strategic planning docs
│   ├── LearnHub_PRD.md
│   ├── LearnHub_TRD.md
│   └── RESEARCH-DECISIONS.md
├── prompts/                # Copilot prompt templates
├── copilot-instructions.md # Main entry point for Copilot
└── tool-sets.json          # Available Copilot tools
```

### `_authors/` — Author Metadata
**Purpose:** Author profiles linked to posts

```
_authors/
└── satya-k.md              # Satya K's author profile
```

**Content:**
- Bio, social links, avatar
- Used for author attribution on posts

### `_site/` — Build Output
**Status:** Generated on each build, not committed to git

```
_site/
├── index.html              # Homepage
├── feed.xml                # RSS feed
├── sitemap.xml             # SEO sitemap
├── search.json             # Lunr.js search index
├── assets/                 # Compiled CSS, JS, images
├── ai/                     # Category page
├── backend/                # Category page
├── [categories]/
└── [post-urls]/            # Rendered individual posts
```

---

## File Type Summary

| Extension | Location | Purpose | Compiled By |
|-----------|----------|---------|------------|
| `.md` | `_posts/`, `docs/` | Markdown content | Jekyll |
| `.html` | `_layouts/`, `_includes/`, root | Liquid templates | Jekyll |
| `.yml` / `.yaml` | `_data/`, `src/yml/`, root | Configuration & data | Gulp (src) → Jekyll |
| `.scss` | `_sass/` | Stylesheets | Jekyll |
| `.js` | `src/js/`, `assets/js/` | JavaScript | Gulp → minified in prod |
| `.py` | `scripts/` | Python utilities | Manual execution |
| `.json` | Root, `package.json`, root | Config & lock files | npm / Manual |
| `.lock` | Root | Locked versions | Bundler / npm |

---

## Build Flow & Dependencies

```
Source Files                    Build Step                      Output
─────────────────────────────────────────────────────────────────────
src/yml/_config.yml  ─────→  [Gulp include]  ─────→  _config.yml
src/js/*.js          ─────→  [Gulp concat/uglify]  ─→ assets/js/main.js
_sass/*.scss         ─────→  [Jekyll compile]  ────→ assets/css/main.css
_posts/*.md          ─────→  [Jekyll + Liquid]  ──→ _site/*/*.html
_data/*.yml          ─────→  [Jekyll parse]  ──────→ Site variables
_layouts/*.html      ─────→  [Jekyll render]  ────→ _site/*.html
_includes/*.html     ─────→  [Jekyll inject]  ────→ Inside layouts
assets/images/*      ─────→  [Copy]  ───────────→ _site/assets/images/
```

---

## Key Observations

1. **Static Output:** All final content is HTML/CSS/JS in `_site/` — served directly by GitHub Pages
2. **No Database:** All content stored as Markdown + YAML files in git
3. **Two-Stage Build:**
   - **Stage 1 (Gulp):** Config compilation, CSS/JS processing, image optimization
   - **Stage 2 (Jekyll):** Markdown → HTML, template rendering, site generation
4. **Excluded from Build:** `docs/`, `node_modules/`, `src/`, `.env`, `.git/` are in `.gitignore` or excluded from Jekyll
5. **Ready for Customization:** `_includes/` directory prepared for series navigation, difficulty badges, and custom components

---

## References

- **Stack Reference:** [stack.md](stack.md)
- **Architecture Overview:** [architecture.md](architecture.md)
- **Conventions & Standards:** [conventions.md](conventions.md)
