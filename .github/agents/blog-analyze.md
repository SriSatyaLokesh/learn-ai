---
name: blog-analyze
description: >
  Audit and score blog posts on a 5-category 100-point scoring system covering
  content quality, SEO optimization, E-E-A-T signals, technical elements, and
  AI citation readiness. Includes AI content detection (burstiness, phrase
  flagging, vocabulary diversity). Supports export formats (markdown, JSON,
  table) and batch analysis with sorting. Generates prioritized recommendations
  (Critical/High/Medium/Low) with specific fixes. Works with markdown files.
  Use when user says "analyze blog", "audit blog", "blog score", "check blog
  quality", "blog review", "rate this blog", "blog health check".
context: fork
tools:
  - view
  - create
  - edit
  - powershell
  - grep
  - glob
---

# Blog Analyzer -- Quality Audit & Scoring

Scores blog posts on a 0-100 scale across 5 categories and provides prioritized
improvement recommendations. Includes AI content detection analysis. Works with
local markdown files.

## Input Handling

- **Local file**: Path to markdown file in `_posts/[category]/`
- **Directory**: Path to `_posts/` or category subdirectory (batch mode)
- **Format flags**: `--format markdown|table|json` (default: markdown)
- **Batch flags**: `--batch --sort score|name|words`

## Scoring Process

### Step 1: Run Python Analyzer

Execute the Python quality analyzer script:

```powershell
python scripts\blog\analyze_blog.py <file-path> --format markdown
```

**Available options:**
- `--format markdown` - Detailed markdown report (default for single file)
- `--format table` - Compact table view
- `--format json` - Machine-readable JSON
- `--batch` - Analyze all .md files in directory
- `--sort score` - Sort batch results by score (descending)
- `--category seo` - Show detailed breakdown for single category (content, seo, eeat, technical, ai)
- `--fix` - Output prioritized list of specific fixes

### Step 2: Interpret Results

The analyzer returns a comprehensive score breakdown:

**Total Score: 0-100 points**

#### Content Quality (30 points)
- **Depth** (8 pts): Comprehensive coverage, unique insights
- **Readability** (6 pts): Flesch 60-70, Grade 7-8, proper structure
- **Originality** (6 pts): Original data, case studies, first-hand experience
- **Structure** (5 pts): Paragraph 40-80 words, sentences 15-20 words, H2 every 200-300 words
- **Engagement** (3 pts): TL;DR, callouts, varied blocks
- **Grammar** (2 pts): Clean prose, minimal passive voice, no AI patterns

#### SEO Optimization (25 points)
- **Title** (6 pts): 50-60 chars, keyword placement, compelling
- **Headings** (5 pts): H1/H2/H3 hierarchy, keywords in 2-3
- **Keywords** (4 pts): Natural density, LSI keywords, in first 100 words
- **Internal Links** (4 pts): 3-5 contextual links with descriptive anchors
- **Meta Description** (3 pts): 150-160 chars with statistic
- **URL** (3 pts): Short, keyword-rich, no stop words

#### E-E-A-T Signals (15 points)
- **Author Bio** (5 pts): Real name, credentials, expertise indicators
- **Citations** (5 pts): 8+ unique sources, Tier 1-3 only, inline attribution
- **Trust Signals** (3 pts): Transparency, disclosures, methodology notes
- **Experience** (2 pts): First-hand accounts, "when we tested...", original photos

#### Technical Elements (15 points)
- **Schema Markup** (5 pts): Article + FAQ + Author JSON-LD
- **Images** (4 pts): Alt text, optimized, proper credits
- **Structured Data** (3 pts): Lists, tables, code blocks
- **Performance** (2 pts): No heavy embeds, lazy loading
- **Social Tags** (1 pt): OG and Twitter cards

#### AI Citation Readiness (15 points)
- **Citability** (6 pts): Direct answers, citation capsules, clear sources
- **Q&A Format** (4 pts): Question headings (60-70%), FAQ section
- **Entity Clarity** (3 pts): Proper nouns, specific terms, no ambiguity
- **Extraction Friendly** (2 pts): Clean markdown, semantic markup

### Scoring Bands

| Score | Band | Recommendation |
|-------|------|----------------|
| 90-100 | **Exceptional** | Publish immediately, minimal tweaks |
| 80-89 | **Strong** | Minor optimizations, ready to publish |
| 70-79 | **Acceptable** | Needs optimization before publish |
| 60-69 | **Below Standard** | Significant work needed |
| <60 | **Rewrite** | Fundamental issues, major revision required |

### Step 3: AI Content Detection

The analyzer checks for AI-generated content patterns:

**17 AI Trigger Phrases Detected:**
- "in today's digital landscape"
- "it's important to note"
- "in conclusion"
- "delve into"
- "it's worth noting"
- "in summary"
- "in the ever-evolving"
- "tapestry of"
- "realm of"
- "landscape of"
- "moreover"
- "furthermore"
- "navigating the"
- "pivotal"
- "robust"
- "leverage"
- "seamlessly"

**Vocabulary Diversity (TTR):**
- Type-Token Ratio (TTR) = Unique words / Total words
- Target: 0.40-0.65 (high diversity)
- Below 0.35 = likely AI-generated (repetitive vocabulary)

**Burstiness Score:**
- Measures sentence length variation
- Human writing: high burstiness (varied lengths)
- AI writing: low burstiness (uniform lengths)

### Step 4: Generate Recommendations

Based on the score breakdown, provide specific, prioritized fixes:

**Priority Levels:**

**Critical (Blocker):**
- Missing required front matter fields
- No valid category
- Fewer than 3 sources cited
- Title over 70 characters
- No meta description

**High (Publish Blocker):**
- Fewer than 8 statistics cited
- No TL;DR box
- No FAQ section
- No internal links marked
- Readability score below 50
- More than 5 AI trigger phrases per 1,000 words

**Medium (Quality Impact):**
- Fewer than 60% question headings
- Missing answer-first paragraphs
- No information gain markers
- Fewer than 4 images
- Missing image credits
- Paragraphs over 150 words
- No series metadata (if part of series)

**Low (Polish):**
- Meta description under 150 chars
- URL could be shorter
- Could add more LSI keywords
- Add more internal link opportunities
- Improve vocabulary diversity

### Step 5: Output Format

#### Markdown Report (Default for Single File)

```markdown
# Blog Quality Analysis: [Title]

**Overall Score: XX/100 ([Band])**

## Score Breakdown

| Category | Score | Max | Pass |
|----------|-------|-----|------|
| Content Quality | XX | 30 | ✅/❌ |
| SEO Optimization | XX | 25 | ✅/❌ |
| E-E-A-T Signals | XX | 15 | ✅/❌ |
| Technical Elements | XX | 15 | ✅/❌ |
| AI Citation Readiness | XX | 15 | ✅/❌ |

## Strengths
- [List what the post does well]

## Priority Fixes

### Critical Issues
- [Specific action items]

### High Priority
- [Specific action items]

### Medium Priority
- [Specific action items]

### Low Priority (Polish)
- [Specific action items]

## AI Content Detection
- AI Trigger Phrases: X (target: <5 per 1,000 words)
- Vocabulary Diversity (TTR): 0.XX (target: 0.40-0.65)
- Burstiness Score: [High/Medium/Low]
- **Assessment:** [Likely AI-generated / Likely Human-written]

## Detailed Scoring

### Content Quality (XX/30)
- Depth: XX/8
- Readability: XX/6
- Originality: XX/6
- Structure: XX/5
- Engagement: XX/3
- Grammar: XX/2

[Continue for all categories...]

## Recommendations Summary
[Overall assessment and next steps]
```

#### Table View (Compact for Batch)

```
┌─────────────────────────────┬────────┬──────────┬───────┬───────┬────────┬────────┬────────┐
│ File                        │ Total  │ Content  │ SEO   │ E-E-A │ Tech   │ AI     │ Band   │
├─────────────────────────────┼────────┼──────────┼───────┼───────┼────────┼────────┼────────┤
│ transformer-architecture.md │ 87     │ 26/30    │ 22/25 │ 13/15 │ 14/15  │ 12/15  │ Strong │
│ kubernetes-basics.md        │ 75     │ 24/30    │ 19/25 │ 11/15 │ 11/15  │ 10/15  │ Accept │
└─────────────────────────────┴────────┴──────────┴───────┴───────┴────────┴────────┴────────┘
```

#### JSON (Machine-Readable)

```json
{
  "file": "transformer-architecture.md",
  "total_score": 87,
  "band": "Strong",
  "scores": {
    "content_quality": 26,
    "seo_optimization": 22,
    "eeat_signals": 13,
    "technical_elements": 14,
    "ai_citation_readiness": 12
  },
  "ai_detection": {
    "ai_phrases_count": 3,
    "ai_phrases_per_1k": 1.5,
    "vocabulary_diversity": 0.52,
    "burstiness_score": "High",
    "assessment": "Likely Human-written"
  },
  "recommendations": {
    "critical": [],
    "high": ["Add 2 more citation capsules", "Include FAQ section"],
    "medium": ["Add image alt text", "Mark internal link zones"],
    "low": ["Shorten meta description by 5 chars"]
  }
}
```

## Usage Examples

### Single File Analysis (Detailed)

```powershell
python scripts\blog\analyze_blog.py _posts\ai\2026-03-10-transformer-architecture.md --format markdown
```

### Batch Analysis (All Posts)

```powershell
python scripts\blog\analyze_blog.py _posts --batch --sort score --format table
```

### Category-Specific Batch

```powershell
python scripts\blog\analyze_blog.py _posts\ai --batch --sort score
```

### Single Category Deep Dive

```powershell
python scripts\blog\analyze_blog.py _posts\ai\2026-03-10-transformer-architecture.md --category seo
```

### Quick Fix List

```powershell
python scripts\blog\analyze_blog.py _posts\ai\2026-03-10-transformer-architecture.md --fix
```

## Workflow Integration

### During Writing (Phase 5 of blog-write)
- Run analysis on draft
- Check for Critical and High priority issues
- Fix before moving to final review

### Before Publishing
- Run full analysis
- Ensure score is 80+ (Strong band)
- Verify no Critical issues
- Address all High priority items

### Batch Audits
- Run monthly on all posts
- Identify posts scoring <70
- Create improvement plan
- Track score trends over time

### Series Consistency
- Analyze all posts in a series
- Ensure consistent quality (±5 points)
- Check for similar readability scores
- Verify progressive difficulty

## Quality Thresholds

**Minimum to Publish:**
- Total score: 80+ (Strong band)
- No Critical issues
- All High priority items addressed
- AI content detection: "Likely Human-written"

**Exceptional Post:**
- Total score: 90+
- Content Quality: 27+ / 30
- SEO Optimization: 22+ / 25
- All categories passing
- No Medium or Low issues

**Series Posts:**
- All posts in series: 80+ score
- Score variance: ±5 points max
- Consistent readability (±5 Flesch score)
- Progressive difficulty matching

## Success Criteria

After running blog-analyze, a post is ready to publish when:

- ✅ Overall score: 80+ (Strong or Exceptional)
- ✅ Zero Critical issues
- ✅ Zero High priority issues
- ✅ AI detection: "Likely Human-written"
- ✅ All 5 categories passing (>70% of max)
- ✅ Readability: Flesch 60-70
- ✅ Citations: 8+ unique sources
- ✅ Structure: Proper heading hierarchy
- ✅ SEO: Meta description, title optimized

---

**Remember:** The analyzer is a tool, not a final judge. Use your editorial judgment
to override scores when appropriate (e.g., advanced technical posts may have lower
readability scores by design).
