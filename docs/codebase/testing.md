# Learn with Satya K — Testing Strategy

**Document:** Testing Approach & Quality Assurance  
**Last Updated:** March 2026  
**Status:** Foundation Phase

---

## Current Testing Approach

**Maturity Level:** Manual + Build-time validation only

The project is in Foundation Phase (Phase 1–2) with no automated test suite yet. Testing is currently:
1. **Manual verification** by author before commit
2. **Jekyll build validation** on GitHub Actions (syntax errors only)
3. **Python content analysis** for blog quality scoring

---

## Testing Strategy by Component

### 1. Jekyll Build Validation

**When:** On every push to `main` (GitHub Actions)

**What's Tested:**
- All `.md` files parse as valid Markdown
- All YAML front-matter is syntactically correct
- All template references resolve (`_includes/`, `_layouts/`)
- All Jekyll plugins load and execute
- HTML output generated without errors

**Failure Behavior:**
- GitHub Actions workflow fails
- Site is NOT deployed
- Error message provided in Actions tab

**Manual Check (Local):**
```bash
# Run Jekyll in safe mode (same as GitHub)
bundle exec jekyll build --safe
```

---

### 2. Content Quality Analysis

**Tool:** `scripts/blog/analyze_blog.py`

**When:** Optional author usage before committing

**What's Analyzed:**

| Category | Points | Metrics |
|----------|--------|---------|
| **Content Quality** | 30 | Depth, readability (Flesch-Kincaid grade), originality, grammar, structure |
| **SEO Optimization** | 25 | Title quality, H2/H3 structure, keyword placement, meta description, internal links |
| **E-E-A-T Signals** | 15 | Author info, citations, trust signals, personal experience |
| **Technical Elements** | 15 | Schema.org JSON-LD, images, mobile compliance, page speed signals |
| **AI Citation Readiness** | 15 | Structured data, Q&A format, entity extraction, crawler accessibility |

**Output Formats:**

```bash
# JSON output (default)
python scripts/blog/analyze_blog.py _posts/ai/post.md

# Markdown report
python scripts/blog/analyze_blog.py _posts/ai/post.md --format markdown

# Compact table
python scripts/blog/analyze_blog.py _posts/ai/post.md --format table

# Single category detail
python scripts/blog/analyze_blog.py _posts/ai/post.md --category seo

# Batch analysis with sorting
python scripts/blog/analyze_blog.py _posts/ --batch --sort score
```

**Scoring Bands:**
- **90–100:** Exceptional (ready to publish)
- **80–89:** Strong (minor improvements optional)
- **70–79:** Acceptable (polish recommended)
- **60–69:** Below Standard (revision needed)
- **< 60:** Rewrite required

**Dependency Notes:**
- `textstat` (optional) — Text readability scoring
- `beautifulsoup4` (optional) — HTML parsing for SEO checks
- Graceful degradation if not installed

**Usage Workflow:**
```bash
# Analyze before committing
python scripts/blog/analyze_blog.py _posts/ai/2026-03-10-new-post.md --format markdown

# Address issues
# (Edit post)

# Re-analyze
python scripts/blog/analyze_blog.py _posts/ai/2026-03-10-new-post.md --format markdown

# If score ≥ 80: Commit and push
git add _posts/ai/2026-03-10-new-post.md
git commit -m "feat(ai): add new-post"
git push
```

---

### 3. Manual Pre-Publish Checklist

**Author Responsibility:** Before every commit

**Front-Matter Validation:**
- [ ] All required fields present (title, date, category, tags, excerpt, description, seo fields)
- [ ] Date matches filename and is ISO format with timezone
- [ ] Category exists in `_data/categories.yml`
- [ ] Series & part (if applicable) exist in `_data/series.yml`
- [ ] Tags are 3–7 lowercase hyphenated items
- [ ] Description is exactly 140–160 characters
- [ ] Difficulty is one of: beginner, intermediate, advanced
- [ ] seo.primary_keyword is specific and measurable
- [ ] seo.canonical_url is absolute (not relative)

**Content Validation:**
- [ ] Minimum 800 words (series) or 600 words (standalone)
- [ ] No placeholder text or [TODO] markers
- [ ] Title matches content
- [ ] All links functional (test with curl or browser)
- [ ] Code examples execute without syntax errors
- [ ] All external images have attribution

**SEO Validation:**
- [ ] Primary keyword appears in: title, first paragraph, meta description, at least one H2
- [ ] Keyword density is 1–2% (not stuffed)
- [ ] 2–3 internal links included
- [ ] Meta description is exactly 140–160 chars and compelling

**Markdown Validation:**
- [ ] All code blocks have language specified
- [ ] No broken links (anchors, external URLs)
- [ ] Tables render correctly
- [ ] No orphaned formatting (unmatched backticks, etc.)

**Image Validation:**
- [ ] Hero image placed at `assets/images/posts/{slug}/hero.jpg`
- [ ] All external images have attribution in format: `*Photo by Name on Source — License*`
- [ ] No copyrighted/restricted images

---

## Planned Testing Infrastructure

### Phase 3: End-to-End Agent Testing

**When:** During agent development (Agents introduced in Phase 3)

**Test Workflow:**

```bash
# 1. Manual test run of full pipeline
node scripts/agents/orchestrator.js "Write Part 1 of AI Fundamentals series" --dry-run

# 2. Review generated AgentContext, outline, body

# 3. Run full pipeline (creates .md file)
node scripts/agents/orchestrator.js "Write Part 1 of AI Fundamentals series"

# 4. Validate output .md file
python scripts/blog/analyze_blog.py _posts/ai/ai-fundamentals-part-1.md --format markdown

# 5. Check score is ≥ 80
# 6. Author reviews and commits if OK
```

**Agent Output Validation:**
- Each agent's output conforms to `AgentContext` interface
- Formatter Agent produces valid YAML + Markdown
- Front-matter passes Jekyll validation
- Word count meets minimum
- SEO rules enforced (keyword placement, density, etc.)
- Image attribution present for all external images

---

### Phase 4: Integration Testing

**When:** First content posts created via agent pipeline

**Test Scope:**
1. **Build Integration:**
   - Generated posts build successfully with Jekyll
   - No warnings or errors in build log
   - search.json updated correctly
   - Category pages render without breakage

2. **SEO Integration:**
   - All generated posts pass Lighthouse SEO audit (≥ 95)
   - Meta tags properly injected
   - Schema.org JSON-LD valid per Google Structured Data Tool
   - sitemap.xml includes all new posts

3. **User Experience:**
   - Series navigation (prev/next) renders correctly
   - Series sidebar shows correct progress
   - Series index pages list all parts in order
   - Search index includes all new posts

**Manual QA Steps:**
```bash
# 1. Local build
npm run dev

# 2. Test in browser
# - Verify post renders
# - Click series navigation links
# - Test search box (search for keywords from new posts)
# - Inspect meta tags: F12 → Network/Elements tab
# - Validate Schema: https://validator.schema.org/

# 3. Check Lighthouse
# - Run Lighthouse audit on post page
# - Target: Performance ≥ 90, SEO ≥ 95, Accessibility ≥ 90

# 4. Test on mobile
# - Resize browser to 375px width
# - Verify responsive layout
# - Test navigation (hamburger menu, links)

# 5. Check build output
JEKYLL_ENV=production bundle exec jekyll build --safe
# Verify no errors, check file sizes in _site/
```

---

### Phase 5: Browser Testing (Playwright)

**Status:** [PLANNED] — Not yet implemented

**Tool:** Playwright (E2E testing framework)

**Planned Test Scenarios:**

```typescript
// Example: Series navigation flow
test('Navigate through an entire series', async ({ page }) => {
  // 1. Visit Series index page
  await page.goto('/series/ai-fundamentals/');
  
  // 2. Verify series metadata displays
  await expect(page.getByRole('heading', { name: 'AI Fundamentals' })).toBeVisible();
  await expect(page.getByText(/8 parts/)).toBeVisible();
  
  // 3. Verify part list shows all parts with completion
  const parts = page.getByRole('list').getByRole('listitem');
  await expect(parts).toHaveCount(8);
  
  // 4. Click Part 1
  await page.getByRole('link', { name: 'Part 1: What is Machine Learning?' }).click();
  
  // 5. Verify post page loads
  await expect(page.getByRole('heading', { level: 1 }).first()).toContainText('Machine Learning');
  
  // 6. Verify prev/next navigation
  await expect(page.getByRole('link', { name: /Part 2/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Previous/ })).toBeDisabled(); // No prev for part 1
  
  // 7. Click Next to Part 2
  await page.getByRole('link', { name: /Next: Part 2/ }).click();
  
  // 8. Verify Part 2 loads and prev/next updated
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Part 2');
  await expect(page.getByRole('link', { name: /Part 1/ })).toBeVisible();
  await expect(page.getByRole('link', { name: /Part 3/ })).toBeVisible();
});
```

**Test Coverage Areas (Planned):**
- Series navigation (prev/next buttons)
- Search functionality
- Category filtering
- Author profile links
- Share buttons
- Mobile responsiveness
- Dark mode toggle
- Difficulty badge display

---

## Performance Testing

**Current Approach:** Manual via Lighthouse

**Lighthouse Targets:**
- **Performance:** ≥ 90
- **Accessibility:** ≥ 90
- **Best Practices:** ≥ 90
- **SEO:** ≥ 95

**Testing Procedure:**
```bash
# 1. Build production version
JEKYLL_ENV=production bundle exec jekyll build

# 2. Serve locally
python3 -m http.server 8000 --directory _site

# 3. Open in Chrome
# https://localhost:8000/ai/your-post/

# 4. Run Lighthouse (F12 → Lighthouse tab)
# Record baseline scores
```

**Optimization Targets:**
- Page size < 500KB (uncompressed)
- First Contentful Paint < 1.5s (on 4G)
- Largest Contentful Paint < 2.5s (on 4G)
- Cumulative Layout Shift < 0.1

---

## Security Testing

**Areas (Planned):**
- No sensitive data in commits (API keys, etc.)
- markdown rendering safe (no XSS via user input)
- External links validated (no broken/malicious URLs)
- Image attribution verified (actual photographer, source)

**Manual Checks:**
```bash
# 1. Scan for API keys in git history
git log -p | grep -i "apikey\|secret\|password"

# 2. Check .gitignore
cat .gitignore | grep ".env"

# 3. Verify all links
# (Use online link checker or curl)
curl -I https://external-link-from-post.com

# 4. Check for JavaScript vulnerabilities
# (No custom JS yet; Lunr.js is audited)
npm audit
```

---

## Testing Checklist (Before Production Merge)

| Phase | Testing Required | Responsible |
|-------|-----------------|-------------|
| **Local Dev** | Manual + Quality analyzer | Developer |
| **Commit to main** | Jekyll build validation (GitHub Actions) | Auto |
| **Phase 3+ (Agents)** | Agent output validation, score check | Developer |
| **Phase 4+ (First Posts)** | Full build integration, Lighthouse audit | Developer |
| **Phase 5+ (E2E Tests)** | Playwright series/search/category flows | Auto (GitHub Actions) |
| **Post-Publish (Monthly)** | Broken link check, Security scan | Developer (manual) |

---

## Continuous Improvement

**Monitoring Plan:**
- Track Lighthouse scores across all posts (monthly)
- Monitor build success rate
- Track content quality scores for trends
- Collect user feedback on post usefulness

**Gaps & Future Work:**
- [ ] Automated Playwright tests (E2E suite)
- [ ] Performance regression testing (compare page load times)
- [ ] Accessibility automated scanning (axe, Pa11y)
- [ ] Link checker in GitHub Actions (automated broken link detection)
- [ ] Spell check in GitHub Actions
- [ ] Image optimization automation (WebP conversion)

---

## References

- **Directory Structure:** [structure.md](structure.md)
- **Tech Stack:** [stack.md](stack.md)
- **Conventions:** [conventions.md](conventions.md)
- **Blog Analysis Tool:** `scripts/blog/analyze_blog.py`
- **Playwright Instructions:** `.github/instructions/playwright-typescript.instructions.md`
