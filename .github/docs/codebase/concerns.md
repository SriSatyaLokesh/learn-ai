# LearnAI — Known Issues & Technical Debt

**Document:** Concerns, Limitations, and Future Improvements  
**Last Updated:** March 2026  
**Status:** Foundation Phase

---

## Summary

This project is in **Foundation Phase** with significant planned features not yet implemented. The current system is stable but minimal. Known concerns fall into three categories:

1. **Architectural Debt** — Planned features not yet built
2. **Performance Constraints** — GitHub Pages + Jekyll limitations
3. **Content Operations** — Manual processes that should be automated

---

## Tier 1: Critical Gaps (Block Phase 4–5)

### 1.1 Partial Content — Published vs. Planned

**Issue:** Only Tools category has published content; planned categories (AI, Backend, System Design, DevOps, Frontend) are empty  
**Impact:** Site has initial content but lacks depth in core learning areas  
**Status:** ✅ Partial; 🚀 requires Phase 3 (Agent Pipeline) for scale  
**Current Content:**

**Published (Live):**
```
_posts/
├── tools/               # ✅ 8 posts (Copilot CLI learning series)
│   ├── Part 1: introduction-to-copilot-cli (2024-06-10)
│   ├── Part 2: copilot-cli-getting-started (2026-03-20)
│   ├── Part 3: copilot-cli-vs-copilot-chat (2026-03-10)
│   ├── Part 4: copilot-cli-advanced-usage (2026-04-10)
│   ├── Part 5: copilot-cli-troubleshooting (2026-05-10)
│   ├── Part 6: project-build-with-copilot-cli (2026-03-10)
│   └── 2 additional standalone posts
│
└── career/              # ✅ 1 post (getting-started.md)

Planned (Empty):
├── ai/                  # Blocked until Phase 3
├── backend/             # Blocked until Phase 3
├── devops/              # Blocked until Phase 3
├── frontend/            # Blocked until Phase 3
└── system-design/       # Blocked until Phase 3
```

**Current Impact:**
- ✅ Homepage displays published posts
- ✅ Search index includes 9 posts
- ✅ Tools category is functional
- 🟡 Career category minimal (1 post)
- 🔴 Planned categories (AI, Backend, System Design, DevOps, Frontend) empty

**Timeline:**
- ✅ Phase 1–2: Completed (current state)
- 🚀 Phase 3: Build Agent Pipeline (2–3 weeks)
- 📝 Phase 4: Generate planned content (50+ posts for AI, Backend, System Design)
- ✨ Phase 5: Site fully functional with all categories populated

---

### 1.2 AI Agent System Not Implemented

**Issue:** Multi-agent content generation pipeline exists only in documentation  
**Impact:** All content must be written manually or using external tools  
**Status:** ⏳ In design phase (TRD section 15)  
**Effort:** ~2–3 weeks of development

**Missing Components:**
- [ ] Orchestrator Agent
- [ ] Research Agent (web search integration)
- [ ] SEO & Strategy Agent
- [ ] Writing Agent
- [ ] Formatter Agent
- [ ] AgentContext interface & handoff system
- [ ] CLI runner (`node agents/run.js`)
- [ ] Integration with Claude API

**Impact on Workflow:**
- Currently: Manual Markdown writing → commit
- Planned: Topic idea → Agent pipeline → commit

**Timeline:** Start Phase 3

---

### 1.3 No Custom Jekyll Layouts Built

**Issue:** Series navigation, difficulty badges, and custom components still in planning  
**Impact:** Cannot render series-specific features (prev/next, progress bars)  
**Status:** ⏳ Planned in Phase 2  
**Files Needed:**
- [ ] `_includes/series-navigation.html` — Prev/Next buttons
- [ ] `_includes/series-sidebar.html` — Learning path sidebar
- [ ] `_includes/difficulty-badge.html` — Difficulty display
- [ ] `assets/js/progress.js` — localStorage progress tracker
- [ ] `assets/js/series-progress.js` — Series completion calculator
- [ ] Custom CSS for series UI

**Impact on User Experience:**
- Users cannot navigate through series posts
- No visual progress indicators
- No difficulty level information
- Series structure not visible

**Timeline:** Start Phase 2

---

## Tier 2: High-Priority Technical Debt

### 2.1 Static Site Limitations

**Issue:** No server-side features; everything must be static or client-side  
**Impact:** Limited functionality compared to traditional blogs

| Feature | Limitation |
|---------|-----------|
| **User Accounts** | No authentication; cannot track individual user progress |
| **Real-Time Updates** | Site updates only on rebuild (1–3 min after push) |
| **Dynamic Search** | Limited to Lunr.js client-side; cannot search beyond built index |
| **Comments Moderation** | No spam filtering; depends on Giscus (GitHub Discussions) |
| **Custom Analytics** | Must use third-party services (Plausible, Google Analytics) |
| **Email Subscriptions** | Cannot store emails; would need external service |
| **A/B Testing** | Cannot test variations without separate builds |

**Workarounds:**
- Use GitHub Discussions (Giscus) for comments
- Use Plausible/Fathom for analytics (privacy-friendly)
- Use Substack/Mailchimp for email subscriptions (not integrated)

**Mitigation:** Document these limitations in portfolio context

---

### 2.2 GitHub Pages Constraints

**Issue:** Jekyll can only use GitHub Pages whitelist plugins  
**Impact:** Cannot use certain powerful Jekyll plugins

**Forbidden Plugins (Examples):**
- Custom Ruby plugins
- `jekyll-admin` (admin dashboard)
- Database-backed plugins
- External API plugins (except those built into Jekyll)

**Current Plugin Status:**
```ruby
# ✅ Allowed (GitHub Pages whitelist)
- jekyll-feed
- jekyll-sitemap
- jekyll-paginate
- jekyll-toc

# ❌ Would require custom CI (not allowed)
- jekyll-responsive-image (image optimization)
- jekyll-assets (asset pipeline)
```

**Consequence:** 
- Asset optimization must be done via Gulp (current approach)
- Image optimization cannot be automated in GitHub Actions
- Custom logic cannot be added to Jekyll directly

---

### 2.3 Build Performance Degradation Risk

**Issue:** Jekyll build time increases linearly with post count  
**Impact:** Deployment slow at 500+ posts; potential GitHub Actions timeout (15 min)

**Current Performance (Estimated):**
| Post Count | Build Time |
|-----------|------------|
| 50 | 3–5 sec |
| 100 | 6–10 sec |
| 200 | 12–20 sec |
| 500 | 30–60 sec |
| 1000+ | 2–5 min |

**Risk Threshold:** GitHub Actions timeout is 15 minutes  
**Mitigation:**
- Use incremental builds when possible: `jekyll build --incremental`
- Monitor build times quarterly
- If it approaches 5 minutes → refactor to split site into multiple Jekyll instances
- Implement build caching in GitHub Actions

**Current Risk Level:** 🟢 Low (at 0 posts, but monitor as content grows)

---

## Tier 3: Medium-Priority Improvements

### 3.1 No Automated Content Quality Checks in CI/CD

**Issue:** Blog analyzer runs manually; not integrated into GitHub Actions  
**Impact:** Low-quality content could be merged if author skips analysis

**Current Workflow:**
```
Author writes post
      ↓
Author runs analyzer (optional, manual)
      ↓
Author reviews score (if they remembered to run it)
      ↓
Commit & push
      ↓
[No check — anything can be deployed]
```

**Improvement:** Fail build if quality score < 80
```yaml
# Pseudo GitHub Actions step
- name: Analyze Blog Quality
  run: |
    SCORE=$(python scripts/blog/analyze_blog.py --category seo --format json | jq .score)
    if [ $SCORE -lt 80 ]; then
      echo "Blog quality score too low: $SCORE/100"
      exit 1
    fi
```

**Effort:** ~2 hours  
**Impact:** Ensures consistent quality

---

### 3.2 No Automated Link Validation

**Issue:** Broken external links can exist in published posts  
**Impact:** Hurts SEO, poor user experience

**Current Approach:** Manual checking (error-prone)

**Solution:** Add link checker to GitHub Actions
```yaml
- name: Check Links
  uses: gaurav-nelson/github-action-markdown-link-check@v1
  with:
    use-quiet-mode: 'yes'
    max-depth: 3
```

**Effort:** ~1 hour  
**Impact:** Catches broken links before deploy

---

### 3.3 No Image Optimization Pipeline

**Issue:** Large hero images not compressed; could slow page load  
**Impact:** Performance score may be penalized if images > 500KB

**Current Approach:** Manual author optimization

**Improvement:** Automated WebP conversion + compression
```bash
# Could be added to Gulp or GitHub Actions
convert hero.jpg -quality 85 -strip all hero.webp
# Reduce 2MB JPEG → 300KB WebP
```

**Effort:** ~3 hours  
**Impact:** Better performance, faster page loads

---

### 3.4 No Spell Check Automation

**Issue:** Typos and grammar errors possible in content  
**Impact:** Low-quality posts hurt credibility

**Current Approach:** Manual proofreading

**Improvement:** GitHub Actions spell check
```yaml
- uses: rojopolis/spellcheck-github-actions@0.29.0
  with:
    config_path: .spellcheck.yml
```

**Effort:** ~2–3 hours  
**Impact:** Catches common typos before merge

---

## Tier 4: Low-Priority / Nice-to-Have

### 4.1 No Search Analytics

**Issue:** Cannot see what users search for  
**Impact:** Miss insights into what content users want

**Current Approach:** None (static site)

**Improvement:** 
- Add client-side logging of search queries
- Send to Plausible Events API
- Analyze popular searches API

**Effort:** ~4 hours  
**Impact:** Data-driven content planning

---

### 4.2 No Series Completion Analytics

**Issue:** Cannot see how many users complete series  
**Impact:** Miss data on series effectiveness

**Current Approach:** localStorage only (not persisted)

**Improvement:**
- Optional: Send completion events to Plausible
- Privacy-first: No identification, only aggregate stats

**Effort:** ~3 hours  
**Impact:** Understand learning outcomes

---

### 4.3 No Mobile App

**Issue:** No native app experience (not critical for blog)  
**Impact:** Users on mobile must use browser

**Status:** Out of scope  
**Effort:** Not planned

---

## Dependency Health

### Ruby Gems (`Gemfile`)

| Gem | Purpose | Status | Notes |
|-----|---------|--------|-------|
| `jekyll` | Static site generator | ✅ Current | Monitor for updates |
| `kramdown` | Markdown parser | ✅ Current | Stable |
| `rouge` | Code syntax highlighting | ✅ Current | Widely used |
| `jekyll-paginate` | Post pagination | ✅ Current | GitHub Pages official |

**Health Check Frequency:** Monthly  
**Command:** `bundle outdated`

### npm Dependencies (`package.json`)

| Package | Purpose | Version | Status |
|---------|---------|---------|--------|
| `gulp` | Build automation | 4.0.2 | ✅ Latest stable |
| `browser-sync` | Dev server | 2.26.7 | ⚠️ Check for updates |
| `gulp-imagemin` | Image optimization | 8.0.0 | ⚠️ Last updated 2021 |
| `gulp-uglify` | JS minification | 3.0.0 | ⚠️ Stable but old |

**Health:** ⚠️ Some packages outdated  
**Action:** Test upgrade to latest versions in Phase 2–3  
**Command:** `npm audit`, `npm outdated`

---

## Security Concerns

### Low Priority (Static Site)

**Note:** Static sites have much smaller attack surface than dynamic sites.

| Concern | Severity | Mitigation |
|---------|----------|-----------|
| **Supply Chain (npm)** | Low | Run `npm audit` monthly |
| **Dependency vulnerabilities** | Low | GitHub Dependabot enabled (repo setting) |
| **API key exposure** | Medium | Use `.env`, check git log regularly |
| **Third-party tracking** | Low | Use privacy-first analytics (Plausible) |
| **XSS in comments** | Medium | Giscus sanitizes GitHub Discussions input |

**No Known Vulnerabilities:** ✅

---

## Future Roadmap Risks

### Phase 3 Risk: Agent Pipeline Complexity

**Risk:** Multi-agent system is complex; agents may hallucinate or produce low-quality content  
**Mitigation:**
- Manual author review before every publish
- Quality analyzer integration (score ≥ 80 threshold)
- Test agents thoroughly with 5–10 manual runs first
- Formatter Agent validation prevents malformed posts

**Effort:** 2–3 weeks of development + testing

---

### Phase 4 Risk: Content Velocity

**Risk:** If agents work well, producing 50+ posts quickly may saturate bandwidth or market  
**Mitigation:**
- Start with 1–2 posts/week
- Gather feedback on post quality
- Adjust content themes based on user interest
- Don't publish everything immediately

**Planning Impact:** Schedule content thoughtfully

---

### Phase 5 Risk: Analytics Privacy Compliance

**Risk:** Collecting analytics data across countries requires:  
- GDPR compliance (EU)
- CCPA compliance (California)
- Opt-in/consent (some jurisdictions)

**Mitigation:**
- Use Plausible (GDPR-compliant by design, no cookies)
- Plausible = no consent banner required
- Document privacy policy on site
- No third-party cookies

**Compliance Status:** ✅ Using Plausible = Built in

---

## Recommendations for Next Phase

### Immediate (Next Month)

1. **Close Phase 1 Gaps:**
   - ✅ Document tech stack ([DONE] → stack.md)
   - ✅ Document structure ([DONE] → structure.md)
   - ✅ Document architecture ([DONE] → architecture.md)
   - ✅ Document conventions ([DONE] → conventions.md)
   - ✅ Document integrations ([DONE] → integrations.md)
   - ✅ Document testing ([DONE] → testing.md)
   - ✅ Document concerns ([DONE] → concerns.md)

2. **Start Phase 2:**
   - Build custom Jekyll includes (series-nav, difficulty-badge, etc.)
   - Implement localStorage progress tracker
   - Test Lunr.js search integration
   - Set up development environment on local machine

### Month 2 (Phase 3)

1. **Begin Agent Development:**
   - Start with Orchestrator Agent (simplest)
   - Progress through Research → SEO → Writer → Formatter

2. **External Integration Setup:**
   - Get Anthropic API key
   - Get Unsplash API key
   - Test API calls in isolation

3. **Testing & Validation:**
   - Test each agent individually
   - Test full pipeline with 3–5 sample topics
   - Validate output .md files pass Jekyll build

### Month 3 (Phase 4)

1. **First Content Wave:**
   - Generate 2 complete series (16–20 posts)
   - 5–10 standalone posts
   - Gather feedback on content quality

2. **Site Polish:**
   - Verify all category pages work
   - Test search functionality
   - Check Lighthouse scores
   - Fix any bugs in series navigation

3. **SEO Setup:**
   - Submit sitemap to Google Search Console
   - Submit to Bing Webmaster Tools
   - Monitor indexing status

---

## Conclusion

The project is well-designed in documentation but **not yet functionally complete**. Core gaps are:

1. ✅ **Design & Documentation** — EXCELLENT
2. ⏳ **Agent System** — Not implemented
3. ⏳ **Custom Components** — Not implemented
4. ⏳ **Content** — Not generated

**Risk Level:** 🟡 **Medium**
- No blocking technical debt
- Planned architecture is sound
- Implementation work is substantial (2–3 months)
- No critical unknowns (everything designed in TRD)

**Recommendation:** Proceed with Phase 2 (custom components) while simultaneously starting Phase 3 (agent development).

---

## References

- **Stack:** [stack.md](stack.md)
- **Structure:** [structure.md](structure.md)
- **Architecture:** [architecture.md](architecture.md)
- **Integrations:** [integrations.md](integrations.md)
- **PRD:** `.github/docs/LearnHub_PRD.md`
- **TRD:** `.github/docs/LearnHub_TRD.md`
