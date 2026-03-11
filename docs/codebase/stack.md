# Learn with Satya K — Technology Stack

**Document:** Codebase Architecture Reference  
**Last Updated:** March 2026  
**Status:** Currently Foundation Phase (see Phase 1 in Roadmap)

---

## Quick Reference

| Layer | Technology | Version | Purpose |
|-------|----------|---------|---------|
| **Static Site Generator** | Jekyll | 4.x | Markdown → HTML + Liquid templating |
| **Package Manager** | npm | 8+ | Node.js dependencies |
| **Ruby Manager** | bundler | Latest | Ruby gem dependencies |
| **Build Automation** | Gulp | 4.0.2 | CSS/JS processing, image optimization |
| **Theme** | Chirpy (custom) | Latest | Base Jekyll theme for blogs |
| **Hosting** | GitHub Pages | Native | Static site deployment (free) |
| **Search** | Lunr.js | - | Client-side full-text search (built at build time) |
| **Blog Quality Analyzer** | Python 3 | 3.6+ | Content analysis, SEO scoring (100-pt system) |
| **AI Agent Runner** | Node.js | 18+ | (Planned: Claude API integration) |
| **AI Backbone** | Claude API | sonnet-4-6 | (Planned: Content generation agents) |

---

## Layer Breakdown

### 1. **Frontend & Static Generation**

- **Jekyll 4.x** (`Gemfile`)
  - Converts Markdown files in `_posts/` to HTML
  - Uses Liquid templates in `_layouts/` and `_includes/`
  - Generates static output to `_site/` directory
  - Runs on GitHub Actions CI/CD on each push

- **Chirpy Theme**
  - Base responsive theme designed for developer blogs
  - Built-in dark mode, TOC, reading time display
  - Category and tag support
  - Customizations in progress (series navigation, difficulty badges, etc.)

- **Lunr.js**
  - Client-side JavaScript library for full-text search
  - Search index built at Jekyll build time from `search.json`
  - No backend required; runs entirely in browser

### 2. **Build & Development**

- **Gulp 4.0.2** (`gulpfile.js`)
  - **Responsibilities:**
    - Compile `src/yml/_config.yml` → `_config.yml` (YAML includes support)
    - Process CSS from `src/scss/` → `assets/css/`
    - Combine/minify JavaScript from `src/js/` → `assets/js/`
    - Optimize images via ImageMIN
    - Trigger Jekyll build on file changes
    - Serve site locally with BrowserSync for live reload

  - **Key Dependencies:**
    - `gulp-concat` — Combine CSS/JS files
    - `gulp-imagemin` — Image optimization
    - `gulp-uglify` — JavaScript minification
    - `gulp-rename` — File renaming
    - `browser-sync` — Dev server with live reload
    - `child_process` — Execute Jekyll commands

- **npm** 
  - Manages Node.js dev dependencies (Gulp, Babel, etc.)
  - Scripts in `package.json`:
    - `npm run build` → `gulp build`
    - `npm run serve` → `bundle exec jekyll serve --baseurl /learn-with-satya`
    - `npm run dev` → `gulp build && bundle exec jekyll serve --baseurl /learn-with-satya`

### 3. **Ruby & Gems**

- **Bundler** (`Gemfile`)
  - Manages Jekyll and plugin dependencies
  - Core gems:
    - `jekyll` — Site generator
    - `kramdown` — Markdown processor
    - `rouge` — Syntax highlighting
    - `jekyll-paginate` — Post pagination
    - `json`, `logger`, `csv` — Ruby 3.4+ compatibility

### 4. **Content Structure**

- **Markdown Posts** (`_posts/` directory)
  - Organized by category: `ai/`, `backend/`, `system-design/`, `devops/`, `frontend/`, `career/`, `tools/`
  - YAML front-matter header containing metadata
  - (Currently: Empty; awaiting first content posts)

- **YAML Data Files** (`_data/`)
  - `series.yml` — Learning series definitions
  - `categories.yml` — Category metadata (icons, descriptions, order)

### 5. **Content Analysis & Quality**

- **Python Script** (`scripts/blog/analyze_blog.py`)
  - 5-category, 100-point quality scoring system:
    - **Content Quality** (30 pts) — Depth, readability, grammar
    - **SEO Optimization** (25 pts) — Keywords, structure, metadata
    - **E-E-A-T Signals** (15 pts) — Author, citations, trust
    - **Technical Elements** (15 pts) — Schema, images, mobile
    - **AI Citation Readiness** (15 pts) — Structured data, extraction
  - Detects AI-generated content patterns
  - Multiple output formats: JSON, Markdown, table
  - Optional dependencies: `textstat` (readability), `beautifulsoup4` (HTML parsing)

### 6. **Planned: AI Agent System**

- **Language:** Node.js (TypeScript recommended)
- **AI Model:** Claude API (`claude-sonnet-4-6`)
- **Architecture:** Sequential agent chain (no parallelism)
- **Agent Stack:**
  1. **Orchestrator** — Classify content, determine series/category
  2. **Research** — Web search via Claude's `web_search` tool
  3. **SEO Strategy** — Generate outline, keywords, meta
  4. **Writer** — Compose full post body
  5. **Formatter** — Assemble Jekyll-ready `.md` file
- **Environment:** `.env` file for API keys (not committed to git)
- **Status:** ⏳ In design phase (see TRD Section 15)

---

## Runtime Stack

### Local Development
```bash
# Install Ruby dependencies
bundle install

# Install Node dependencies
npm install

# Start dev server (Gulp + Jekyll + BrowserSync)
npm run dev
```

### Build Pipeline
```bash
# Manual build
gulp build

# Jekyll only (for testing)
bundle exec jekyll serve --baseurl /learn-with-satya

# Production build
JEKYLL_ENV=production bundle exec jekyll build
```

### Deployment
- **Platform:** GitHub Pages (native Jekyll support)
- **Trigger:** Push to `main` branch
- **Build:** Automatic via GitHub Actions
- **Deployment:** ~1–3 minutes from push to live

---

## Dependencies Summary

### Critical Dependencies (5+)
1. **Jekyll** — Core static site generator
2. **Chirpy Theme** — Base blog theme (customization in progress)
3. **Ruby (via Bundler)** — Gem management
4. **Node.js (via npm)** — Build tool ecosystem
5. **Gulp** — Task automation for CSS/JS/images

### Missing (Not Yet Integrated)
- Anthropic SDK for Claude API calls
- Web search integration (Claude native tool, non-blocking)
- Image sourcing (Unsplash API, not yet integrated)

---

## Version Constraints

| Tool | Required | Current | Notes |
|------|----------|---------|-------|
| Node.js | 18+ | Check via `node -v` | Specified in `package.json` `engines` |
| Ruby | 3.0+ | Check via `ruby -v` | Required by Jekyll 4.x |
| bundler | Latest | Auto-installed | Manages gems |
| npm | 8+ | Auto-installed | Manages node packages |

---

## Known Architecture Decisions

1. **Static Site Only** — No server-side processing. All logic at build time or in browser.
2. **GitHub Pages Hosting** — Constrains to Jekyll-native plugins only (no custom plugins).
3. **Client-Side Search** — Lunr.js to avoid backend dependency.
4. **Sequential Agent Chain** — Planned AI agents run sequentially (not parallel) to preserve context quality.
5. **Gulp-Driven Build** — Custom YAML config compilation and asset processing.

---

## References

- **PRD:** `.github/docs/LearnHub_PRD.md`
- **TRD:** `.github/docs/LearnHub_TRD.md`
- **Jekyll Docs:** https://jekyllrb.com/docs/
- **Chirpy Theme:** https://github.com/cotes2020/jekyll-theme-chirpy
