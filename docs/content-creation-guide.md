# LearnAI — Content Creation Guide

## Overview

This guide explains how to create blog content using our 5-phase AI-powered workflow.

## Prerequisites

- GitHub Copilot enabled in VS Code
- `.github/agents/` and `.github/prompts/` loaded
- Understanding of the 7 categories and series structure

## The 5-Phase Workflow

### Phase 1: Requirements Definition

**Command**: `/start-content`

**What happens**:
- Copilot asks: Series or standalone?
- Gathers metadata (category, difficulty, series info)
- Creates content brief at `docs/series/CONTENT-{date}-{slug}.md`
- Marks Phase 1 complete

**Your input needed**:
- Topic description
- Content type (series/standalone)
- Category selection
- Difficulty level
- If series: series ID and part number

### Phase 2: Research

**Command**: `@research docs/series/CONTENT-{date}-{slug}.md`

**What happens**:
- Performs 4-6 web searches on the topic
- Extracts key insights and statistics
- Identifies content gaps
- Compiles sources with attribution
- Updates content brief with findings

**Your input needed**:
- Review research findings
- Approve or request additional research

### Phase 3: SEO Planning

**Command**: `@seo-planner docs/series/CONTENT-{date}-{slug}.md`

**What happens**:
- Generates SEO-optimized title
- Creates URL slug
- Writes meta description (140-160 chars)
- Identifies primary + secondary keywords
- Creates detailed H2/H3 outline
- Suggests internal links and images
- Updates content brief with SEO plan

**Your input needed**:
- Review and approve outline
- Request changes if needed

### Phase 4: Writing

**Command**: `@writer docs/series/CONTENT-{date}-{slug}.md`

**What happens**:
- Writes full post body following outline
- Includes code blocks and examples
- Uses image placeholders
- Incorporates internal links
- Ensures minimum word count
- Updates content brief with written content

**Your input needed**:
- Review draft
- Request revisions if needed

### Phase 5: Formatting & Validation

**Command**: `@formatter docs/series/CONTENT-{date}-{slug}.md`

**What happens**:
- Assembles complete front-matter
- Validates against TRD schema
- Processes image placeholders
- Creates final post file at `_posts/{category}/{date}-{slug}.md`
- Validates series metadata (if applicable)
- Provides action items for you

**Your input needed**:
- Source and add hero image
- Update series.yml (if series post)
- Test locally
- Commit and deploy

## After Formatting: Your Action Items

### 1. Source Hero Image
```bash
# 1. Search Unsplash for image (query provided by formatter)
# 2. Download to:
mkdir -p assets/images/posts/{slug}
# Save as: assets/images/posts/{slug}/hero.jpg
# 3. Update front-matter:
#    header.image_credit: "Photo by [Name] on Unsplash"
#    header.image_credit_url: "https://unsplash.com/photos/xyz"
```

### 2. Update Series Metadata (Series Posts Only)
```bash
# Edit _data/series.yml:
# - Add post to series posts array
# - Increment total_parts count
```

### 3. Local Preview
```bash
bundle exec jekyll serve --baseurl /learn-ai
# Visit: http://127.0.0.1:4000/learn-ai/{category}/{slug}/
```

### 4. Commit and Deploy
```bash
git add _posts/{category}/{date}-{slug}.md
git add _data/series.yml  # if series post
git commit -m "feat({category}): add {slug}"
git push origin main
```

## Tips

### DO
- ✅ Always start with `/start-content`
- ✅ Complete phases in order (1 → 2 → 3 → 4 → 5)
- ✅ Review and approve each phase before moving on
- ✅ Keep content briefs in `docs/series/` for reference

### DON'T
- ❌ Skip phases — each builds on the previous
- ❌ Edit final post files directly — use the workflow
- ❌ Forget to update series.yml for series posts
- ❌ Deploy without local preview

## Troubleshooting

### "Phase X must be complete first"
**Solution**: Go back and complete the missing phase. Each agent validates prior phases before proceeding.

### "Series does not exist in _data/series.yml"
**Solution**: Create the series entry first, or choose a different existing series.

### "Part number is not sequential"
**Solution**: Check `_data/series.yml` for existing parts. Ensure no gaps (e.g., if part 5, parts 1-4 must exist).

### "Front-matter validation failed"
**Solution**: Check the error message. Common issues:
- Title > 70 characters
- Description not 140-160 characters
- Invalid category
- Missing required fields

## Example Workflow

```bash
# 1. Start new content
/start-content
# Answer prompts: "Transformer Architecture", "series", "ai", "intermediate", "ai-fundamentals", "Part 3"

# 2. Research
@research docs/series/CONTENT-2026-03-10-transformer-architecture.md
# Review findings, approve

# 3. SEO Planning
@seo-planner docs/series/CONTENT-2026-03-10-transformer-architecture.md
# Review outline, approve

# 4. Writing
@writer docs/series/CONTENT-2026-03-10-transformer-architecture.md
# Review draft, approve

# 5. Formatting
@formatter docs/series/CONTENT-2026-03-10-transformer-architecture.md
# Follow action items

# 6. Deploy
# (After completing action items)
bundle exec jekyll serve --baseurl /learn-ai  # test
git add . && git commit -m "feat(ai): add transformer-architecture-explained"
git push origin main
```

## Questions?

Refer to:
- `.github/copilot-instructions.md` - Full project instructions
- `.github/agents/*.agent.md` - Individual agent specifications
- `docs/templates/` - Templates for various doc types
