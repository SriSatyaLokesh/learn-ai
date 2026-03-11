# LearnHub Content Creation Workflow

## Overview

We use a **5-phase structured workflow** adapted from the Copilot Team Workflow for creating blog content. This ensures quality, consistency, and completeness.

## The 5-Phase Workflow

```
/start-issue → /discuss → /research → /plan → /execute → /verify
    ↓            ↓           ↓          ↓         ↓          ↓
  Setup    Requirements  Codebase   Planning  Writing  Validation
                        & Topic    SEO/     Content   Front-matter
                        Research   Outline            & Deploy
```

### Phase 1: Discuss (Requirements) 💬

**Command**: `/discuss` or say "Start the discussion phase"

**Purpose**: Define WHAT to write before HOW to write it

**Agent**: `@discuss`

**Activities**:
- Determine content type (series or standalone)
- Select category (one of 7)
- Set difficulty level
- Define target audience
- Specify scope (what to cover)
- Specify out of scope (what NOT to cover)
- If series: confirm series ID and part number

**Output**: Phase 1 section in content brief with approved requirements

**Gate**: Must get developer approval before proceeding to Phase 2

---

### Phase 2: Research 🔍

**Command**: `/research` or `@research docs/series/CONTENT-{id}-{slug}.md`

**Purpose**: Gather information, sources, and insights before planning structure

**Agent**: `@research`

**Activities**:
- Perform 4-6 web searches on the topic
- Extract key insights and statistics
- Identify common misconceptions
- Find expert perspectives
- Identify content gaps (what's missing from existing content)
- Compile sources with proper attribution

**Output**: Phase 2 section with research findings, sources, and recommended angles

**Gate**: Research must be complete before planning SEO/structure

---

### Phase 3: Plan (SEO & Outline) 📋

**Command**: `/plan` or `@plan docs/series/CONTENT-{id}-{slug}.md`

**Purpose**: Create SEO strategy and detailed content outline

**Agent**: `@plan`

**Activities**:
- Generate SEO-optimized title (60-70 chars)
- Create URL-friendly slug (kebab-case, no stop words)
- Write meta description (140-160 chars exactly)
- Identify primary + 4-6 secondary keywords
- Create detailed H2/H3 outline (5-8 main sections)
- Suggest internal links (2-3 related posts)
- Suggest image search queries for Unsplash

**Output**: Phase 3 section with complete SEO strategy and outline

**Gate**: Outline must be approved before writing content

---

### Phase 4: Execute (Write Content) ⚡

**Command**: `/execute` or say "Start writing the content"

**Purpose**: Write the actual blog post following the approved outline

**This phase uses sub-agents**:
1. **Content Agent** (`@writer`) - Writes full post body
2. **Formatter Agent** (`@formatter`) - Assembles front-matter and creates final file

**Activities**:
- Write full post body (800+ words for series, 600+ for standalone)
- Follow SEO outline exactly (H2/H3 structure)
- Include code blocks where relevant
- Use image placeholders for diagrams
- Include internal links from Phase 3
- Incorporate research insights naturally
- Write in developer-friendly tone
- Create complete Jekyll front-matter
- Validate front-matter against TRD schema
- Generate final `.md` file in `_posts/{category}/`

**Output**:
- Phase 4 section with written content
- Final post file at `_posts/{category}/{date}-{slug}.md`
- Action items list for developer

**Gate**: Content must pass validation checks before verify phase

---

### Phase 5: Verify ✅

**Command**: `/verify` or `@verify docs/series/CONTENT-{id}-{slug}.md`

**Purpose**: Final validation before deployment

**Agent**: `@verify`

**Activities**:
- Validate front-matter completeness
- Check word count meets minimum
- Verify SEO keyword placement
- Confirm image placeholders are formatted correctly
- Check series metadata (if series post)
- Verify internal links are valid
- Confirm all required fields present
- Generate deployment checklist

**Output**: Phase 5 section with validation results and deployment instructions

**Gate**: All checks must pass before deployment

---

## Quick Start Guide

### 1. Start New Content

```
/start-issue
```

This will:
- Confirm/create working branch
- Create content brief document
- Set up tracking structure

### 2. Define Requirements

```
/discuss
```

Answer questions about:
- Content type (series/standalone)
- Category and difficulty
- Target audience
- Scope and learning objectives

### 3. Research Topic

```
/research
```

Or with explicit path:
```
@research docs/series/CONTENT-042-transformer-architecture.md
```

### 4. Plan Structure

```
/plan
```

Review and approve:
- SEO title and meta description
- Content outline (H2/H3 structure)
- Keyword strategy

### 5. Write Content

```
/execute
```

This runs sub-phases:
- Writing the post body
- Formatting front-matter
- Creating final file

### 6. Validate & Deploy

```
/verify
```

Complete action items:
- Source hero image
- Update series.yml (if series)
- Test locally
- Deploy

---

## Content Brief Structure

Every piece of content is tracked in `docs/series/CONTENT-{id}-{slug}.md`:

```markdown
# Content Brief: [Title]

**Content ID**: CONTENT-042
**Status**: 📝 In Progress
**Branch**: content/CONTENT-042-transformer-architecture

## Phase 1: Discuss (Requirements) 💬
**Status**: [x] Complete
{Requirements details}

## Phase 2: Research 🔍
**Status**: [x] Complete
{Research findings}

## Phase 3: Plan (SEO & Outline) 📋
**Status**: [x] Complete
{SEO strategy and outline}

## Phase 4: Execute (Write Content) ⚡
**Status**: [x] Complete
{Written content and final file}

## Phase 5: Verify ✅
**Status**: [x] Complete
{Validation results}
```

---

## Phase Gates (Critical!)

**Each phase validates the previous one is complete:**

- **Research** checks Phase 1 (Discuss) complete
- **Plan** checks Phases 1-2 complete
- **Execute** checks Phases 1-3 complete
- **Verify** checks Phases 1-4 complete

**If you see an error like:**
> "Requirements must be defined first. Run `/discuss`."

**This means you skipped a phase. Go back and complete it.**

---

## Available Commands

| Command | Phase | Purpose |
|---------|-------|---------|
| `/start-issue` | Setup | Create branch and content brief |
| `/discuss` | 1 | Define requirements |
| `/research` | 2 | Gather sources and insights |
| `/plan` | 3 | Create SEO strategy and outline |
| `/execute` | 4 | Write content and create final file |
| `/verify` | 5 | Validate and prepare for deployment |
| `/status` | Any | Check current phase progress |
| `/debug` | Any | Troubleshoot issues |
| `/summarize` | Any | Save session context |

---

## Specialized Agents

### Workflow Agents (Phases 1-3, 5)
- `@discuss` - Requirements gathering
- `@research` - Web research and source compilation
- `@plan` - SEO planning and outline creation
- `@verify` - Final validation

### Content Agents (Used in Phase 4 - Execute)
- `@writer` - Writes full post body following outline
- `@formatter` - Assembles front-matter and creates final file

### Supporting Agents
- `@review` - Code/content quality review
- `@parallel-builder` - Orchestrate multiple independent tasks

---

## Directory Structure

```
.github/
├── agents/          ← Workflow + content agents
├── prompts/         ← Slash commands
├── instructions/    ← Auto-loading context rules
└── workflows/       ← Process documentation

docs/
├── series/          ← Content briefs (work in progress tracking)
├── templates/       ← Templates for briefs, front-matter
└── codebase/        ← Jekyll/project documentation

_posts/
└── {category}/      ← Published posts organized by category

_data/
├── series.yml       ← Series metadata
└── categories.yml   ← Category definitions
```

---

## Tips for Success

### DO ✅
- Always start with `/start-issue`
- Complete phases in order
- Review and approve each phase output
- Use content briefs to track progress
- Let agents handle validation

### DON'T ❌
- Skip phases
- Try to do multiple phases at once
- Edit final files manually (use the workflow)
- Forget to update series.yml for series posts
- Deploy without running `/verify`

---

## Troubleshooting

### "Agent says phase X must be complete"
**Solution**: Go back and complete that phase. Check content brief status.

### "Series doesn't exist in _data/series.yml"
**Solution**: Create series entry first, or select existing series in discuss phase.

### "Part number is not sequential"
**Solution**: Check series.yml. If part 5, parts 1-4 must exist (no gaps).

### "Front-matter validation failed"
**Solution**: Check error message. Common issues:
- Title > 70 chars
- Description not 140-160 chars
- Invalid category
- Missing required fields

### "Can't find content brief"
**Solution**: Run `/start-issue` first to create tracking document.

---

## Example Full Workflow

```bash
# 1. Start
/start-issue
# Input: "Part 3 of AI Fundamentals on Transformer Architecture"
# Input: "CONTENT-AI-FUND-03"

# 2. Define Requirements
/discuss
# Answer questions about audience, scope, learning objectives
# Approve requirements

# 3. Research
/research
# Review research findings
# Approve sources and angles

# 4. Plan
/plan
# Review SEO strategy and outline
# Request any changes
# Approve outline

# 5. Write
/execute
# Content is written and formatted
# Review draft
# Approve

# 6. Validate
/verify
# Complete action items:
#   - Source hero image from Unsplash
#   - Update _data/series.yml
#   - Test locally: bundle exec jekyll serve --baseurl /learn-with-satya
#   - Commit and push

# Done! Post published to GitHub Pages
```

---

**For detailed agent specifications**, see individual agent files in `.github/agents/`

**For prompt templates**, see `.github/prompts/`

**For auto-loading instructions**, see `.github/instructions/`
