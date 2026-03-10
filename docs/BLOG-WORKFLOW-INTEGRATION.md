# Blog-Workflow Integration Guide

**How the blog creation system integrates with the 5-phase content workflow**

---

## Two Approaches to Content Creation

### Approach 1: Automated (Single Command)

**Best for:** Standard blog posts, quick content creation, consistent quality

```
/blog write "Your Topic"
```

**What happens internally:**
1. ✅ **Discuss**: Asks category, difficulty, series, target length
2. ✅ **Research**: Searches for 8-12 statistics, finds images, validates sources
3. ✅ **Plan**: Selects template, generates outline, gets approval
4. ✅ **Execute**: Writes complete post with all required elements
5. ✅ **Verify**: Self-checks quality, estimates score

**Time:** ~15-20 minutes (mostly automated)

---

### Approach 2: Phased (Manual Control)

**Best for:** Complex posts, series content, high-stakes publishing, learning the system

```
Phase 1: /blog brief "Your Topic"         # Discuss + early Research
Phase 2: /blog outline "Your Topic"       # Research + Plan
Phase 3: /blog write "Your Topic"         # Execute (with approved outline)
Phase 4: /blog analyze [file]             # Verify (quality check)
Phase 5: /blog seo-check [file]           # Verify (SEO validation)
```

**Time:** ~20-30 minutes (more control, higher quality potential)

---

## Phase-by-Phase Mapping

### Phase 1: Discuss (Requirements Gathering)

**Traditional Workflow:**
```
/start-issue → /discuss
```
- Creates feature branch
- Generates content brief
- Defines requirements

**Blog Integration:**
```
/blog brief "Your Topic"
```

**Output:**
- Primary keyword and search intent
- Competitor analysis (SERP top 10)
- Required statistics and sources
- Recommended template
- Target word count
- Outline structure

**Example:**
```bash
/blog brief "Kubernetes Deployment Strategies"

# Returns:
# - Primary keyword: "kubernetes deployment strategies" (2,400/mo)
# - Search intent: Informational (70%), Tutorial (30%)
# - Recommended template: Tutorial
# - SERP analysis: Rolling updates (10/10), Blue-green (9/10)
# - Content gaps: Rollback procedures (2/10), Cost implications (0/10)
# - Required stats: 8-12 from CNCF, Google Cloud, Datadog
# - Target word count: 2,500-3,000 words
```

**When to use this phase:**
- Planning series content
- Competitive niches
- Need SERP research
- Multiple stakeholders

---

### Phase 2: Research (Source Gathering)

**Traditional Workflow:**
```
/research
```
- Web search for insights
- Collect sources
- Validate information

**Blog Integration:**
```
# Research happens automatically in /blog write
# OR manually via blog-researcher agent
```

**What gets researched:**
- 8-12 current statistics (2025-2026 preferred)
- Tier 1-3 sources (government, academic, major tech)
- Cover image (1200x630, OG-compatible)
- 3-5 inline images (Pixabay/Unsplash/Pexels)
- Competitor content patterns
- Common questions (for FAQ)

**Manual research (if needed):**
```bash
# Invoke the blog-researcher agent directly
# Use web_search for specific statistics
# Validate source tiers
```

**Quality criteria:**
- Minimum 8 unique sources
- All Tier 1-3 (no blogs, no AI-generated content)
- Current data (2024-2026)
- Proper attribution format: ([Source Name](url), year)

---

### Phase 3: Plan (Outline & Strategy)

**Traditional Workflow:**
```
/plan
```
- SEO strategy
- Content outline
- Keyword mapping

**Blog Integration:**
```
/blog outline "Your Topic"
```

**Output:**
- H2/H3 structure (60-70% question headings)
- Answer-first paragraph notes for each section
- Statistic placement markers
- Image/chart suggestions
- Internal linking zones
- Citation capsule reminders

**Example:**
```markdown
## H2: How Do Rolling Updates Work in Kubernetes?
**Word target:** 300-400 words

**Answer-first paragraph:**
- Stat: "Rolling updates reduce downtime by 94% compared to recreate strategy" (CNCF, 2025)
- Direct answer: Rolling updates deploy new pods incrementally while keeping old ones running

**Content points:**
- Step-by-step process
- [CODE: Rolling update YAML]
- [IMAGE: Rolling update diagram]
- [CITATION CAPSULE: 40-60 word passage]
- [INTERNAL-LINK: Kubernetes fundamentals]
```

**When to use this phase:**
- Complex topics requiring structure
- Series posts needing consistency
- Multiple writers collaborating
- Need approval before writing

---

### Phase 4: Execute (Content Writing)

**Traditional Workflow:**
```
/execute
```
- Write content
- Format according to standards
- Add front matter

**Blog Integration:**
```
/blog write "Your Topic"
```

**What gets written:**

1. **Jekyll Front Matter:**
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

2. **Introduction (100-150 words):**
   - Hook with surprising statistic
   - Problem/opportunity statement
   - What reader will learn

3. **TL;DR Box:**
   ```markdown
   > **TL;DR:** [40-60 word standalone summary with 1 statistic]
   ```

4. **H2 Sections (5-8 sections):**
   - Answer-first paragraphs (40-60 words with stat)
   - Supporting evidence
   - Code examples (for technical posts)
   - Images with alt text and credits
   - Citation capsules (40-60 word passages)
   - Internal linking zones

5. **FAQ Section (3-5 questions):**
   ```markdown
   ### Question?
   [40-60 word answer with statistic]
   ```

6. **Conclusion (100-150 words):**
   - Key takeaways (bulleted)
   - Call to action
   - Link to next content

**Quality controls during writing:**
- Paragraph discipline (40-80 words)
- Sentence discipline (15-20 words)
- 60-70% question headings
- 8+ unique statistics
- 2-3 information gain markers
- Citation capsules per H2
- 5-10 internal linking zones

---

### Phase 5: Verify (Quality Assurance)

**Traditional Workflow:**
```
/verify
```
- Validate quality
- Check standards
- Deploy readiness

**Blog Integration:**
```
/blog analyze [file]
/blog seo-check [file]
```

**Analysis includes:**

**1. Quality Scoring (0-100):**
```bash
/blog analyze _posts/ai/2026-03-10-transformer-architecture.md

# Returns:
# Overall Score: 87/100 (Strong)
# 
# Breakdown:
# - Content Quality: 26/30 ✅
# - SEO Optimization: 22/25 ✅
# - E-E-A-T Signals: 13/15 ✅
# - Technical Elements: 14/15 ✅
# - AI Citation Readiness: 12/15 ✅
#
# AI Detection: Likely Human-written ✅
#
# Priority Fixes:
# - High: Add 2 more citation capsules
# - Medium: Add FAQ section
# - Low: Shorten meta description by 5 chars
```

**2. SEO Validation:**
```bash
/blog seo-check _posts/ai/2026-03-10-transformer-architecture.md

# Returns:
# ✅ Title: 56 chars (target: 50-60)
# ✅ Meta description: 158 chars (target: 150-160)
# ✅ Heading hierarchy: Proper (no skips)
# ✅ Keyword density: 1.8% (target: 1-2%)
# ✅ Internal links: 5 zones marked
# ⚠️ URL length: 42 chars (recommend <40)
# 
# Overall SEO Score: 92/100 (Excellent)
```

**3. Publishing Checklist:**

Before publishing, ensure:
- [ ] Overall score: 80+ (Strong or Exceptional)
- [ ] Zero Critical issues
- [ ] All High priority issues resolved
- [ ] AI detection: "Likely Human-written"
- [ ] Valid Jekyll front matter
- [ ] Correct category (one of 7)
- [ ] File saved to `_posts/[category]/YYYY-MM-DD-[slug].md`
- [ ] Images downloaded to `/assets/img/posts/`
- [ ] Internal links resolved (no `[INTERNAL-LINK: ...]` placeholders)
- [ ] Previewed locally with `jekyll serve`
- [ ] Git committed with descriptive message

---

## Workflow Decision Tree

```
Start: New Blog Post Idea
│
├─ Is this a quick standard post?
│  └─ YES → Use /blog write "topic" (Approach 1)
│      └─ Done in 15-20 minutes
│
├─ Is this a complex topic needing research?
│  └─ YES → Start with /blog brief "topic"
│      ├─ Review brief output
│      ├─ Then /blog outline "topic"
│      ├─ Approve outline
│      └─ Then /blog write "topic"
│
├─ Is this part of a series?
│  └─ YES → Use Approach 2 (Phased)
│      ├─ /blog brief to ensure consistency
│      ├─ /blog outline with series context
│      ├─ /blog write with series metadata
│      └─ Compare quality scores across series (±5 points)
│
└─ Is this a rewrite of existing content?
   └─ YES → Use /blog rewrite [file]
       ├─ Preserves original voice
       ├─ Updates statistics
       ├─ Applies answer-first formatting
       └─ Adds missing elements (FAQ, links, capsules)
```

---

## Integration with Existing Workflow Commands

### Enhanced /start-issue

**Before:**
```bash
/start-issue "Create blog post about transformers"
```

**Now (with blog integration):**
```bash
/start-issue "Create blog post about transformers"

# After branch creation, automatically suggest:
# "Would you like to generate a content brief?"
# → If yes, runs /blog brief automatically
# → Creates .github/content-brief.md in branch
```

### Enhanced /execute

**Before:**
```bash
/execute
# Prompts user to write content manually
```

**Now (with blog integration):**
```bash
/execute

# Detects content type:
# → If blog post, suggests: "Use /blog write?"
# → If technical doc, uses existing formatter agent
# → If README, uses existing documentation agent
```

### Enhanced /verify

**Before:**
```bash
/verify
# Runs basic validation
```

**Now (with blog integration):**
```bash
/verify

# Detects if file is in _posts/:
# → YES: Runs /blog analyze automatically
#        Runs /blog seo-check automatically
#        Reports score and blocks if <80
# → NO: Runs standard validation
```

---

## Complete Workflow Example

### Scenario: Writing "Understanding Transformer Architecture" (Beginner, AI Category, Part 1 of Series)

#### Step 1: Generate Brief (Phase 1: Discuss)

```bash
/blog brief "Understanding Transformer Architecture"
```

**Output review:**
- Primary keyword: "transformer architecture explained" ✅
- Search intent: Informational + Tutorial ✅
- Recommended template: Tutorial ✅
- Target audience: Beginners ✅
- SERP gaps: Beginner-friendly explanations, visual aids ✅
- Required stats: Attention mechanism performance, usage rates ✅

#### Step 2: Create Outline (Phase 3: Plan)

```bash
/blog outline "Understanding Transformer Architecture"
```

**Output review:**
- 7 H2 sections (5 questions = 71%) ✅
- Covers: basics, attention mechanism, positional encoding, architecture, applications, advantages, getting started ✅
- FAQ section included ✅
- Visual aids planned (4 diagrams) ✅
- Code examples planned (3 snippets) ✅

**Approved!** ✅

#### Step 3: Write Complete Post (Phase 4: Execute)

```bash
/blog write "Understanding Transformer Architecture"

# Answers:
# - Category? ai
# - Difficulty? beginner
# - Series? transformer-series (new)
# - Series title? "Transformer Architecture Deep Dive"
# - Part number? 1
# - Target length? 2500 words
# - Use approved outline? yes
```

**Post created:**
- File: `_posts/ai/2026-03-10-understanding-transformer-architecture.md`
- Word count: 2,547 words
- Statistics: 10 unique sources (all Tier 1-2)
- Images: 5 (4 diagrams + 1 cover)
- Code examples: 3 (with comments)
- FAQ: 5 questions
- Self-estimated score: 85 (Strong)

#### Step 4: Quality Check (Phase 5: Verify)

```bash
/blog analyze _posts/ai/2026-03-10-understanding-transformer-architecture.md
```

**Results:**
- Overall Score: 87/100 (Strong) ✅
- Content Quality: 27/30 ✅
- SEO Optimization: 23/25 ✅
- E-E-A-T Signals: 13/15 ✅
- Technical Elements: 13/15 ✅
- AI Citation Readiness: 11/15 ⚠️

**Priority Fixes:**
- High: Add 1 more citation capsule (currently 5, target 6)
- Medium: Add alt text to diagram 4
- Low: None

**AI Detection:** Likely Human-written ✅

#### Step 5: SEO Check

```bash
/blog seo-check _posts/ai/2026-03-10-understanding-transformer-architecture.md
```

**Results:**
- SEO Score: 91/100 (Excellent) ✅
- All critical checks passed ✅
- 1 warning: URL could be 5 chars shorter (non-blocking)

#### Step 6: Apply Fixes

- Added 1 more citation capsule to H2 section 4 ✅
- Added alt text: "Transformer architecture diagram showing encoder-decoder structure" ✅
- Re-ran analysis: Score improved to 89/100 (Strong) ✅

#### Step 7: Final Pre-Publish

**Checklist:**
- [x] Score 80+ (89/100) ✅
- [x] Zero Critical/High issues ✅
- [x] AI detection passed ✅
- [x] Images downloaded to `/assets/img/posts/` ✅
- [x] Internal links resolved (6 links added) ✅
- [x] Previewed locally - looks great! ✅
- [x] Added to `_data/series.yml`:
  ```yaml
  - id: transformer-series
    title: "Transformer Architecture Deep Dive"
    category: ai
    description: "Complete guide to transformer architecture..."
    difficulty: beginner
    total_parts: 5
    posts:
      - slug: understanding-transformer-architecture
        part: 1
  ```

#### Step 8: Publish

```bash
git add _posts/ai/2026-03-10-understanding-transformer-architecture.md
git add _data/series.yml
git add assets/img/posts/understanding-transformer-*
git commit -m "feat: Add transformer architecture post (Part 1 of series)

Understanding Transformer Architecture - Beginner's Guide

Part 1 of 'Transformer Architecture Deep Dive' series in AI category.
Explains attention mechanisms, positional encoding, and real-world applications.

Quality Score: 89/100 (Strong)
- Content Quality: 27/30
- SEO Optimization: 23/25
- E-E-A-T: 13/15
- Technical: 13/15
- AI Citations: 13/15

Stats: 2,547 words, 10 sources (Tier 1-2), 5 images, 3 code examples, 5 FAQs
AI Detection: Human-written ✅

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

git push origin main
```

**Total time:** ~25 minutes (including fixes)  
**Quality:** 89/100 (Strong) - Ready for immediate publish  
**Ready for Part 2!**

---

## Best Practices

### For Series Content

1. **Start with brief:**
   ```bash
   /blog brief "[Series Title] Part 1: [Specific Topic]"
   ```

2. **Maintain consistency:**
   - Same difficulty level across series
   - Similar word counts (±500 words)
   - Similar quality scores (±5 points)
   - Consistent readability (±5 Flesch score)

3. **Link between parts:**
   - Reference previous parts in introduction
   - Preview next part in conclusion
   - Use `series` and `part` in front matter

4. **Update series metadata:**
   - Add new posts to `_data/series.yml`
   - Increment `total_parts` as you go
   - Keep `posts` array in order

### For High-Stakes Content

1. **Use phased approach:**
   - Brief → Outline → Write → Analyze → Fix → SEO Check

2. **Target 90+ score:**
   - Add extra citation capsules (8-10 instead of 6)
   - Include 12+ statistics (instead of 8)
   - Add more visual aids
   - Extensive FAQ section (7-10 questions)

3. **Peer review:**
   - Share analysis results with team
   - Get feedback on outline before writing
   - Review internal links for accuracy

### For Batch Content Creation

1. **Generate briefs first:**
   ```bash
   /blog brief "Topic 1"
   /blog brief "Topic 2"
   /blog brief "Topic 3"
   ```

2. **Prioritize by score potential:**
   - Topics with rich data sources first
   - Topics with clear search intent
   - Topics matching our expertise

3. **Maintain quality floor:**
   - Never publish below 80 score
   - Batch analyze after writing all posts
   - Fix all posts below 85 before publishing any

---

## Troubleshooting Workflow Integration

### Issue: Outline doesn't match brief

**Problem:** Generated outline doesn't address gaps identified in brief

**Solution:**
1. Copy gaps from brief into outline prompt
2. Manually specify H2 sections to include
3. Emphasize differentiation points

### Issue: Score too low after writing

**Problem:** Post scores 72/100 (Acceptable, below 80 threshold)

**Solution:**
1. Run `/blog analyze [file] --category [lowest-category]` for details
2. Focus on lowest-scoring category first
3. Common quick wins:
   - Add 3-5 more statistics → +5-8 pts
   - Add FAQ section → +3-5 pts
   - Add citation capsules → +4-6 pts
   - Fix heading hierarchy → +2-4 pts
4. Re-analyze after each fix
5. Target +8-10 points to reach 80+

### Issue: AI detection failure

**Problem:** "Likely AI-generated" assessment

**Solution:**
1. Check AI trigger phrases (`--fix` flag shows list)
2. Rewrite sentences with triggers (use simpler language)
3. Add personal experiences ("In our testing...")
4. Vary sentence lengths (mix 10-word and 25-word sentences)
5. Include specific numbers and names (not generic "Company X")
6. Re-run analyzer

### Issue: Internal links can't be resolved

**Problem:** Don't have related content yet to link to

**Solution:**
1. Keep `[INTERNAL-LINK: ...]` placeholders
2. Document in issue tracker: "Need posts: X, Y, Z"
3. Replace with external authoritative links temporarily:
   ```markdown
   For now, see [official docs](url). We'll publish our guide soon.
   ```
4. Update when related content exists

---

## Success Metrics

### Individual Post

- ✅ Score: 80+ (Strong) or 90+ (Exceptional)
- ✅ Time to publish: <30 minutes
- ✅ Zero Critical/High issues
- ✅ AI detection: Human-written
- ✅ Zero rework needed after publish

### Series

- ✅ All posts: 80+ score
- ✅ Score variance: ±5 points max
- ✅ Readability variance: ±5 Flesch points
- ✅ Consistent structure across all parts
- ✅ Clear progression (beginner → advanced)

### Batch (Monthly)

- ✅ Average score: 85+
- ✅ 90%+ posts score 80+
- ✅ <10% require rework
- ✅ Consistent publishing cadence
- ✅ Quality trend improving (not declining)

---

## Summary

**The blog system IS the workflow - just specialized for blog content.**

- **Automated approach** (`/blog write`) = All 5 phases in one command
- **Phased approach** (`brief → outline → write → analyze`) = Manual control at each phase
- **Both approaches** produce the same quality (80+ scores)
- **Choose based on** complexity, stakes, learning needs, and time available

**Remember:** The goal is not just to create content, but to create **80+ quality content consistently and efficiently**.

🎯 **Default recommendation:** Start with automated approach, switch to phased for complex topics.
