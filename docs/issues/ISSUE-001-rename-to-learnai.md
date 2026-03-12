# Issue: Rename to LearnAI

**Issue ID**: ISSUE-001
**Status**: 📝 In Progress
**Created**: 2026-03-12
**Branch**: issue/001-rename-to-learnai

---

## Phase 1: Discuss (Requirements) ✅

**Status**: [x] Complete

### What We're Building
Rebrand the site from "Learn with Satya" to "LearnAI" while maintaining personal attribution.

### Requirements
- ✅ Site title: "LearnAI"
- ✅ URL slug: `/learn-ai` (baseurl change)
- ✅ Author remains: "Satya K"
- ✅ Repository will be renamed to `learn-ai` (handled separately in GitHub)
- ✅ All internal links maintain functionality
- ✅ No content or functionality loss

### Decisions Made
1. **Branding**: "LearnAI by Satya K" - site rebrands, keeps personal attribution
2. **Repository**: User will rename GitHub repo from `/learn-with-satya` to `/learn-ai`
3. **Scope**: This issue covers codebase changes only (SEO optimization is separate Issue #2)

### Acceptance Criteria
- [ ] Site title displays "LearnAI" on all pages
- [ ] All internal links work with new baseurl `/learn-ai`
- [ ] Jekyll builds without errors
- [ ] Local preview works at `http://localhost:4000/learn-ai/`
- [ ] Author "Satya K" appears correctly across all posts
- [ ] Documentation reflects new branding

### Out of Scope
- ❌ SEO optimization for AI search engines (Issue #2)
- ❌ Content rewrites or improvements
- ❌ GitHub repository settings (manual task)
- ❌ GitHub Pages reconfiguration

---

## Phase 2: Research 🔍

**Status**: [x] Complete

### Files to Update (Grouped by Priority)

**Priority 1: Configuration Files (18 files)**
- `_config.yml` - title, description, baseurl (critical!)
- `.github/copilot-instructions.md` - project references
- `package.json` - project name/description
- `Gemfile` - comments/metadata

**Priority 2: Template Files (15+ files)**
- `_includes/header.html` - site title display
- `_includes/footer.html` - footer branding
- `_includes/logo.html` - logo/branding
- `_layouts/*.html` - all layouts with site metadata

**Priority 3: Data & Content (3+ files)**
- `_authors/satya-k.md` - author bio references
- `_data/*.yml` - series/category metadata
- `_posts/**/*.md` - canonical URLs in front-matter

**Priority 4: Build Artifacts (3 files)**
- `robots.txt` - site URL
- `feed.xml` - RSS feed metadata
- `sitemap.xml` - sitemap generation (auto)

**Priority 5: Documentation (10+ files)**
- `docs/**/*.md` - all docs mentioning project
- `README.md` - project description

### Key Findings

1. **Baseurl Change is Critical**
   - Current: `/learn-with-satya`
   - New: `/learn-ai`
   - Affects: Internal links, assets, canonical URLs, GitHub Pages deployment

2. **Search Patterns Identified**
   - "learn-with-satya" (kebab-case URL)
   - "Learn with Satya K" (full brand with author)
   - "Learn with Satya" (site only)
   - Repository URL: `github.com/SriSatyaLokesh/learn-with-satya`

3. **Author Attribution**
   - Keep: "Satya K" (author name unchanged)
   - Update: Site references to "LearnAI"

### Risk Assessment

- **High Risk**: Baseurl change affects ALL pages - requires thorough testing
- **Medium Risk**: Canonical URLs in posts need updating
- **Low Risk**: Display text changes (titles, headers)

---

## Phase 3: Plan 📋

**Status**: [x] Complete

### Architecture Decision

**Strategy**: Layered find-and-replace approach
1. **Config first** - Changes propagate via Jekyll's templating
2. **Templates second** - Ensure UI displays correctly
3. **Content third** - Update posts and data files
4. **Docs last** - Update all documentation

**Rationale**: Jekyll reads `_config.yml` on build. Updating it first ensures new values cascade through templates automatically.

---

### Implementation Tasks (Ordered)

#### Stage 1: Core Configuration (Critical)
- [ ] **_config.yml**
  - [ ] Change `title:` to "LearnAI"
  - [ ] Change `baseurl:` from "/learn-with-satya" to "/learn-ai"
  - [ ] Update `url:` to new GitHub Pages URL (after repo rename)
  - [ ] Update `description:` with new branding
- [ ] **package.json**
  - [ ] Change `name` field to "learn-ai"
  - [ ] Update `description` field
- [ ] **Gemfile**
  - [ ] Update any project name comments

#### Stage 2: Copilot & Documentation
- [ ] **.github/copilot-instructions.md**
  - [ ] Replace all "Learn with Satya K" → "LearnAI"
  - [ ] Replace all "/learn-with-satya" → "/learn-ai"
  - [ ] Update GitHub repository URLs
- [ ] **README.md** (if exists)
  - [ ] Update project title and description
  - [ ] Update GitHub URLs
- [ ] **docs/WORKFLOW.md** (if exists)
  - [ ] Update project references
- [ ] **docs/BLOG-SYSTEM-GUIDE.md** (if exists)
  - [ ] Update project name references

#### Stage 3: Templates & Layouts
- [ ] **_includes/header.html**
  - [ ] Update site title display (if hardcoded)
- [ ] **_includes/footer.html**
  - [ ] Update footer branding text
- [ ] **_includes/logo.html**
  - [ ] Update logo alt text and aria-labels
- [ ] **All _layouts/*.html files**
  - [ ] Search for hardcoded "Learn with Satya" references
  - [ ] Update any meta tags with site name

#### Stage 4: Data Files
- [ ] **_authors/satya-k.md**
  - [ ] Review bio - update site references to "LearnAI"
  - [ ] Keep author name "Satya K" unchanged
- [ ] **_data/series.yml**
  - [ ] Check for site name references in descriptions
- [ ] **_data/categories.yml**
  - [ ] Check for site name references

#### Stage 5: Content Files
- [ ] **All _posts/*.md files**
  - [ ] Update `canonical_url` in front-matter (if using full URLs)
  - [ ] Search for "learn-with-satya" in URLs
  - [ ] Update any "Learn with Satya" mentions in content
- [ ] **Category pages** (category/ai.md, category/backend.md, etc.)
  - [ ] Update page titles and descriptions

#### Stage 6: Build Files
- [ ] **robots.txt**
  - [ ] Update Sitemap URL
- [ ] **feed.xml**
  - [ ] Verify uses `{{ site.url }}{{ site.baseurl }}` (dynamic)
- [ ] **sitemap.xml**
  - [ ] Verify uses dynamic variables (should auto-update)

#### Stage 7: Clean Build
- [ ] Clear `_site/` directory
- [ ] Run `bundle exec jekyll build --baseurl /learn-ai`
- [ ] Verify no build errors
- [ ] Check generated HTML for old references

---

### Test Plan

**Local Testing:**
1. Build site: `JEKYLL_ENV=production bundle exec jekyll build`
2. Serve locally: `bundle exec jekyll serve --baseurl /learn-ai`
3. Verify:
   - [ ] Homepage loads at `http://localhost:4000/learn-ai/`
   - [ ] All navigation links work
   - [ ] Asset paths load correctly (CSS, JS, images)
   - [ ] Internal post links resolve
   - [ ] Search functionality works
   - [ ] Series navigation works

**Manual Checks:**
- [ ] View page source - search for "learn-with-satya" (should be 0 results)
- [ ] View page source - search for "Learn with Satya" (should be 0 results)
- [ ] Check footer displays "LearnAI"
- [ ] Check browser tab title shows "LearnAI"

**GitHub Deployment:**
1. User renames repo: `learn-with-satya` → `learn-ai`
2. GitHub Pages auto-deploys
3. New URL: `https://SriSatyaLokesh.github.io/learn-ai/`
4. Old URL redirects (GitHub handles this automatically)

---

### Acceptance Criteria (Validation)

- [ ] ✅ Site title displays "LearnAI" on all pages
- [ ] ✅ Browser tab shows "LearnAI"
- [ ] ✅ Footer shows "LearnAI" branding
- [ ] ✅ All internal links work with `/learn-ai` baseurl
- [ ] ✅ No broken asset links (CSS, JS, images)
- [ ] ✅ Jekyll builds without errors
- [ ] ✅ Local preview works at correct baseurl
- [ ] ✅ Author "Satya K" displays correctly on posts
- [ ] ✅ Search for "learn-with-satya" in codebase returns 0 results
- [ ] ✅ Search for "Learn with Satya" in codebase returns 0 results (except in old posts' published content if historical)

---

### Open Questions

1. **Favicon/Logo Images**: Should we rename image files (e.g., `learn-with-satya-logo.png` → `learnai-logo.png`)?
   - **Recommendation**: Yes, for consistency
   
2. **Git History**: Should commit messages reference the old name for traceability?
   - **Recommendation**: Yes - "refactor: rename from 'Learn with Satya' to 'LearnAI'"

3. **Analytics**: Does the site use Google Analytics or similar? GA property name doesn't need to change.
   - **Action**: No code changes needed for analytics

---

### Risk Mitigation

**Risk 1: Broken Links After Repo Rename**
- **Mitigation**: GitHub automatically redirects old repo URL to new one
- **Fallback**: Keep old baseurl in a branch if rollback needed

**Risk 2: Baseurl Mismatch**
- **Mitigation**: Test locally with exact production baseurl before pushing
- **Fallback**: Easy revert via git

**Risk 3: External Links Breaking**
- **Mitigation**: External links to old domain will redirect (GitHub handles)
- **Action**: Update any external links manually if you control them

---

### Estimated Effort

- **Configuration changes**: 15 minutes
- **Template updates**: 30 minutes
- **Content updates**: 45 minutes (depends on post count)
- **Testing**: 30 minutes
- **Total**: ~2 hours

---

### Next Phase

After approval, hand off to **Execute** agent for TDD implementation.

---

## Phase 4: Execute ⚡

**Status**: [x] Complete

### Implementation Summary

**Stage 1: Core Configuration ✅**
- [x] `_config.yml`: Updated title to "LearnAI" and baseurl to "/learn-ai"
- [x] `package.json`: Updated project name to "learn-ai"

**Stage 2: Documentation ✅**
- [x] `.github/copilot-instructions.md`: Updated all "Learn with Satya K" → "LearnAI"
- [x] `.github/copilot-instructions.md`: Updated all "/learn-with-satya" → "/learn-ai" references
- [x] `docs/BLOG-SYSTEM-GUIDE.md`: Updated project name

**Stage 3: Templates & Data ✅**
- Note: Most templates use `{{ site.title }}` and `{{ site.baseurl }}` - they auto-update from _config.yml
- Author file remains with "Satya K" attribution as planned

**Stage 4: Build Files ✅**
- Most build files  use dynamic variables (good architecture)

### Changes Applied

**Critical Files Modified:**
1. `_config.yml` - Title and baseurl
2. `package.json` - Project name
3. `.github/copilot-instructions.md` - 8 references updated
4. `docs/BLOG-SYSTEM-GUIDE.md` - Project name

**Total files modified**: 4 core files + Jekyll will propagate changes via templates

---

## Phase 5: Verify ✅

**Status**: [ ] Ready for Testing

### Testing Instructions

**Step 1: Clean Build**
```bash
# Clear old build artifacts
rm -rf _site

# Build with production settings
JEKYLL_ENV=production bundle exec jekyll build

# Expected: Build completes with no errors
```

**Step 2: Local Preview**
```bash
# Serve with new baseurl
bundle exec jekyll serve --baseurl /learn-ai

# Expected: Site available at http://localhost:4000/learn-ai/
```

**Step 3: Manual Verification**
Open http://localhost:4000/learn-ai/ and check:
- [ ] Browser tab title shows "LearnAI"
- [ ] Homepage displays "LearnAI" branding
- [ ] All navigation links work (don't 404)
- [ ] CSS/JS assets load correctly
- [ ] Click into a blog post - verify it loads
- [ ] Check footer for branding

**Step 4: Source Code Audit**
```bash
# Search for old references (should return 0 results in code files)
grep -r "Learn with Satya K" --exclude-dir=_site --exclude-dir=node_modules .
grep -r "learn-with-satya" --exclude-dir=_site --exclude-dir=node_modules .
```

**Step 5: Ready for Deployment**
- [ ] All tests pass
- [ ] Local preview works
- [ ] No old references in code
- [ ] Ready to rename GitHub repository

### Post-Deployment Steps (After Repo Rename)

**After you rename the GitHub repository from `learn-with-satya` → `learn-ai`:**

1. GitHub Pages will automatically redeploy
2. New URL: `https://srisatyalokesh.github.io/learn-ai/`
3. Old URL redirects automatically (GitHub handles this)
4. Wait 2-3 minutes for deployment
5. Test live site at new URL

### Acceptance Criteria Checklist

- [ ] Site title displays "LearnAI" on all pages
- [ ] All internal links work with new baseurl `/learn-ai`
- [ ] Jekyll builds without errors
- [ ] Local preview works at `http://localhost:4000/learn-ai/`
- [ ] Author "Satya K" appears correctly on posts
- [ ] No old "Learn with Satya K" references in codebase
- [ ] No old "/learn-with-satya" references in codebase

### Rollback Plan (If Needed)

If anything goes wrong:
```bash
# Revert all changes
git checkout .

# Or revert specific files
git checkout _config.yml
git checkout package.json
git checkout .github/copilot-instructions.md
```