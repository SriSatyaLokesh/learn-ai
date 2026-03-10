# Learn with Satya K — Coding & Content Conventions

**Document:** Style Guide & Standards  
**Last Updated:** March 2026  
**Status:** Foundation Phase

---

## File & Naming Conventions

### Blog Posts

**File Naming:**
```
_posts/{category}/{YYYY-MM-DD}-{slug}.md
```

**Rules:**
- **Date:** Must match front-matter `date` field (YYYY-MM-DD)
- **Category:** Directory must match front-matter `category` field
- **Slug:** 
  - kebab-case (lowercase, hyphens, no spaces)
  - Max 60 characters
  - No stop words (the, a, and, of, in, etc.)
  - Should include primary keyword naturally

**Examples:**
- ✅ `_posts/ai/2026-03-10-transformer-architecture-explained.md`
- ✅ `_posts/backend/2026-03-15-rest-api-design-patterns.md`
- ❌ `_posts/ai/transformer-architecture.md` (missing date)
- ❌ `_posts/ai/2026-03-10-the-transformer-architecture.md` (has stop word "the")

### URLs (Permalink Structure)

**Jekyll Permalink Setting:**
```yaml
permalink: /:categories/:title/
```

**Generated URL:**
```
https://yourusername.github.io/learn-with-satya/{category}/{slug}/
```

**Examples:**
- `https://yourusername.github.io/learn-with-satya/ai/transformer-architecture-explained/`
- `https://yourusername.github.io/learn-with-satya/backend/rest-api-design-patterns/`

### Image Files

**Hero Images:**
```
assets/images/posts/{post-slug}/hero.jpg
```

**Examples:**
- `assets/images/posts/transformer-architecture-explained/hero.jpg`
- `assets/images/posts/rest-api-design-patterns/hero.jpg`

**Inline Images:**
- Sourced from Unsplash or Wikimedia Commons (CC0/CC-BY)
- URLs embedded in Markdown
- Attribution block placed below each image

---

## Front-Matter Specification

### Complete Template

```yaml
---
title: "Understanding Transformer Architecture"
subtitle: "How attention mechanisms changed everything in AI"  # Optional
date: 2026-03-10 09:00:00 +0530
last_modified_at: 2026-03-10  # Updated by Formatter Agent

# Taxonomy (REQUIRED)
category: ai
tags: [transformers, attention, deep-learning, nlp]

# Series (OMIT for standalone posts)
series: ai-fundamentals
series_title: "AI Fundamentals"
part: 3

# Content Metadata (REQUIRED)
excerpt: "A deep dive into how transformer models use self-attention to process sequences in parallel."
description: "Learn transformer architecture: self-attention, encoder-decoder structure, positional encoding, BERT and GPT."

# Hero Image (Optional but recommended)
header:
  image: /assets/images/posts/transformer-architecture-explained/hero.jpg
  image_credit: "Photo by Jane Doe on Unsplash"
  image_credit_url: "https://unsplash.com/photos/xyz123"

# Learning Metadata (REQUIRED)
difficulty: intermediate   # beginner | intermediate | advanced
read_time: true
toc: true
toc_sticky: true

# Prerequisites (Optional)
prerequisites:
  - title: "AI Fundamentals Part 2: Backpropagation"
    url: /ai/ai-fundamentals-part-2/
  - title: "Neural Networks Explained"
    url: /ai/neural-networks-explained/

# SEO (REQUIRED)
seo:
  primary_keyword: "transformer architecture explained"
  secondary_keywords: [self-attention mechanism, encoder-decoder architecture, BERT vs GPT, positional encoding]
  canonical_url: "https://yourusername.github.io/learn-with-satya/ai/transformer-architecture-explained/"
---
```

### Field Rules & Constraints

| Field | Type | Required | Constraints | Example |
|-------|------|----------|------------|---------|
| `title` | String | ✅ Yes | Max 70 chars; should include primary keyword in first 60 chars | "Transformer Architecture Explained: Self-Attention from Scratch" |
| `subtitle` | String | Optional | Max 120 chars; sub-heading shown below title | "How attention mechanisms changed everything in AI" |
| `date` | DateTime | ✅ Yes | ISO format: `YYYY-MM-DD HH:MM:SS +HHMM` | `2026-03-10 09:00:00 +0530` |
| `last_modified_at` | Date | Optional | YYYY-MM-DD format; auto-updated by Formatter Agent | `2026-03-10` |
| `category` | String | ✅ Yes | Must match slug from `_data/categories.yml`: `ai`, `backend`, `system-design`, `devops`, `frontend`, `career`, `tools` | `ai` |
| `tags` | Array | ✅ Yes | 3–7 lowercase hyphenated tags; max 3–5 words each | `[transformers, attention-mechanism, deep-learning]` |
| `series` | String | Conditional | Series slug from `_data/series.yml`; omit for standalone posts | `ai-fundamentals` |
| `series_title` | String | Conditional | Required if `series` is set; human-readable name | `AI Fundamentals` |
| `part` | Integer | Conditional | Required if `series` is set; must be unique within series | `3` |
| `excerpt` | String | ✅ Yes | 2–3 sentence post summary shown in cards; max 250 chars | "A deep dive into how transformer models use self-attention to process sequences in parallel." |
| `description` | String | ✅ Yes | SEO meta description; **140–160 chars exactly**; must include primary keyword | "Learn transformer architecture from scratch: self-attention, encoder-decoder structure, positional encoding, and how BERT and GPT use it." |
| `header.image` | Path | Optional | Relative path; format: `/assets/images/posts/{slug}/hero.jpg` | `/assets/images/posts/transformer-architecture-explained/hero.jpg` |
| `header.image_credit` | String | Conditional | Required if `header.image` is set; full attribution | `Photo by Jane Doe on Unsplash` |
| `header.image_credit_url` | URL | Conditional | Required if `header.image_credit` is set; original image link | `https://unsplash.com/photos/xyz` |
| `difficulty` | Enum | ✅ Yes | One of: `beginner`, `intermediate`, `advanced` | `intermediate` |
| `read_time` | Boolean | Optional | Default true; shows reading time estimate | `true` |
| `toc` | Boolean | Optional | Default true for posts > 800 words; enables table of contents | `true` |
| `toc_sticky` | Boolean | Optional | Default true; keeps TOC fixed on scroll | `true` |
| `prerequisites` | Array | Optional | Array of `{title, url}` objects; links to required prior knowledge | See template above |
| `seo.primary_keyword` | String | ✅ Yes | Main target keyword for SEO; used for Formatter validation | `transformer architecture explained` |
| `seo.secondary_keywords` | Array | Optional | 4–6 related keywords for context; lower priority than primary | See template above |
| `seo.canonical_url` | URL | ✅ Yes | Absolute canonical URL for this post; prevents duplicate content issues | `https://yourusername.github.io/learn-with-satya/ai/transformer-architecture-explained/` |

---

## Content Style Guide

### Tone & Voice

**Target Audience:** Developers (junior to mid-level, self-taught or transitioning)

**Style:**
- ✅ Conversational yet technically precise
- ✅ Active voice throughout
- ✅ Short paragraphs (3–4 sentences max)
- ✅ Use "you" when addressing reader
- ✅ Include practical examples and code blocks
- ❌ Avoid overly academic jargon without explanation
- ❌ No marketing-speak or AI-generated phrases (avoid: "in today's digital landscape", "dive into", "game-changer")

### Headings & Structure

**H1 (Title):**
- One per post
- Matches front-matter `title` field
- Includes primary keyword naturally

**H2 (Major Sections):**
- 4–8 per post (800+ word posts)
- Should match SEO-designed outline
- Include secondary keywords where natural

**H3 (Subsections):**
- 1–2 per H2 section
- Break up long content
- Support scanability

**Example Structure:**
```markdown
# Understanding Transformer Architecture (H1 - title)

## Introduction
### What are Transformers?
### Why Do They Matter?

## Self-Attention Mechanism
### Query, Key, Value
### Attention Score Calculation

## Encoder-Decoder Architecture
### The Encoder
### The Decoder

## Key Takeaways
```

### Keyword Placement

**Primary Keyword Must Appear In:**
1. Title (first 60 characters preferred)
2. Meta description (seo.description)
3. First paragraph (opening 100 words)
4. At least one H2 heading
5. Naturally throughout (2% max density)

**Secondary Keywords:**
- Sprinkled naturally in body
- Appear in H2/H3 headings where relevant
- No keyword stuffing

### Lists & Code Blocks

**Bulleted Lists:**
```markdown
**Key Points:**
- Point 1 (complete sentence)
- Point 2 (complete sentence)
- Point 3 (complete sentence)
```

**Numbered Lists:**
```markdown
**Steps:**
1. First step with explanation
2. Second step with explanation
3. Third step with explanation
```

**Code Blocks:**
```markdown
\`\`\`python
# Language specified in fence
def transformer_attention(query, key, value):
    scores = query @ key.transpose() / sqrt(d_k)
    return softmax(scores) @ value
\`\`\`
```

**Inline Code:**
- Use backticks for: function names, variables, file paths, CLI commands
- Example: The `transformer_attention()` function computes...

### Images & Attribution

**Image Markdown Format:**
```markdown
![Description of the image](https://images.unsplash.com/photo-xyz)
*Photo by [Photographer Name] on [Source](source-url) — License Type*
```

**Attribution Requirements:**
- Every external image must have attribution
- Format: `Photo by [Name] on [Source] — [License]`
- Hyperlink the source URL
- Include below image using italic markdown

**Approved Image Sources:**
- Unsplash (free, CC0, no attribution required but appreciated)
- Wikimedia Commons (various CC licenses, attribution required)
- Personal screenshots/diagrams (no attribution needed)

**Prohibited:**
- Getty Images, Shutterstock, iStock (restrictive licenses)
- Screenshots of copyrighted content

### Links & Internal References

**Internal Linking:**
- Include 2–3 internal links per post
- Link to related posts in same category or prerequisite series
- Use descriptive anchor text (not "click here")

**Example:**
```markdown
You can read more about [neural network backpropagation](/ai/neural-networks-backpropagation/) 
in our prerequisites series.
```

**External Links:**
- Use descriptive anchor text
- Open in new tab when appropriate
- Verify no dead links before publish

### Series-Specific Sections

**For Series Posts (Required):**

1. **Opening:** Orient reader within series
   ```markdown
   This is **Part 3 of the AI Fundamentals series**. 
   We've covered [Part 1: ...] and [Part 2: ...].
   ```

2. **Key Takeaways Section:** Bulleted summary
   ```markdown
   ## Key Takeaways

   - Point 1
   - Point 2
   - Point 3
   ```

3. **What's Next Section:** Link to next part
   ```markdown
   ## What's Next

   In **Part 4**, we'll explore [topic of part 4].
   Read next: [Part 4: Topic Name](/ai/series-slug-part-4/)
   ```

**For Standalone Posts:**
- Include "Key Takeaways" section
- Omit "What's Next" section

---

## YAML Data File Conventions

### series.yml Structure

```yaml
- id: ai-fundamentals                    # Unique series slug
  title: "AI Fundamentals"               # Display name
  category: ai                           # Must match category slug
  description: "..."                     # 1–2 sentence overview
  difficulty: beginner                   # beginner | intermediate | advanced
  total_parts: 8                         # Update as posts added
  posts:                                 # Array of parts
    - slug: what-is-machine-learning     # Part slug
      part: 1                            # Part number
      title: "What is Machine Learning?" # Optional; for display
    - slug: neural-networks-explained
      part: 2
      title: "Neural Networks Explained"
```

### categories.yml Structure

```yaml
- slug: ai                               # Unique category slug
  title: "Artificial Intelligence"      # Full name
  display_name: "AI & Machine Learning" # Shorter version for UI
  description: >
    Master LLMs, ML fundamentals, RAG systems, embeddings, 
    and AI agents. From theory to production deployments.
  icon: "🤖"                            # Emoji icon
  order: 1                               # Display order on homepage
```

---

## Formatting & Markdown Guidelines

### Self-Explanatory Code

**Comment WHY, not WHAT:**

❌ **Bad:**
```python
# Increment counter by one
counter += 1

# Multiply by tax rate
total_tax = price * 0.08
```

✅ **Good:**
```python
# Reset counter after 10 retries to prevent blocking
counter += 1

# Apply 8% sales tax (state rate) 
# Note: Federal tax calculated separately in validate_tax()
total_tax = price * 0.08
```

### Minimal Comments

Use comments only to explain:
- Non-obvious business logic
- Algorithm choices (e.g., why Floyd-Warshall vs Dijkstra)
- API constraints or gotchas
- Workarounds for bugs in dependencies
- Complex regex patterns

### Markdown Formatting

**Bold:** `**text**` → for emphasis, keywords
**Italic:** `*text*` → for file names, metadata
**Code:** `` `code` `` → for technical terms, commands
**Links:** `[text](url)` → for references, CTAs

### Avoid

- Decorative dividers: `======`, `----`
- Multiple exclamation marks: `!!!`
- SHOUTING: AVOID ALL CAPS (OK for acronyms: API, JSON)
- Excessive emoji: Use 1–2 per post max, only when adding value
- Hidden HTML comments: Confuses Markdown parsers

---

## SEO Conventions

### Primary Keyword Strategy

1. **Selection:** Target a single, specific keyword (not a phrase)
   - ✅ "transformer architecture explained"
   - ❌ "transformers in AI" (too vague)

2. **Placement:**
   - Title (first 60 chars preferred)
   - Meta description
   - First paragraph opening
   - At least one H2 heading
   - Throughout body (natural, 1–2% density)

3. **Density:** Max 2%; no stuffing
   ```
   Word count: 1200
   Max keyword mentions: ~24 times
   ```

### Meta Description Rules

- **Length:** 140–160 characters (+ or - 5 OK)
- **Include:** Primary keyword naturally
- **Structure:** Lead with answer, add modifiers
- **Avoid:** Clickbait, keyword stuffing

**Example:**
```
"Learn transformer architecture from scratch: how self-attention works, 
encoder-decoder structure, positional encoding, and why BERT and GPT use it."
```

### Internal Linking

- Include 2–3 internal links per post minimum
- Link to related posts, prerequisites, follow-ups
- Use descriptive anchor text (not "read more")
- Link to established posts (avoid dead links)

---

## Code Conventions (for embedded examples)

### Language Specificity

Always specify language in code fence:
```python
# Python example
def hello():
    print("Hello, World!")
```

```javascript
// JavaScript example
function hello() {
    console.log("Hello, World!");
}
```

```bash
# Bash example
echo "Hello, World!"
```

### Clarity Over Cleverness

- Use descriptive variable names
- Include comments only for non-obvious logic
- Keep examples short (5–20 lines max)
- Test code examples before publishing

---

## Validation & QA

### Pre-Publish Checklist

Before committing a post:

- [ ] **Front-Matter Complete:**
  - [ ] `title` (max 70 chars, includes primary keyword)
  - [ ] `date` (ISO format with timezone)
  - [ ] `category` (exists in `_data/categories.yml`)
  - [ ] `tags` (3–7 tags)
  - [ ] `excerpt` (max 250 chars)
  - [ ] `description` (140–160 chars, includes primary keyword)
  - [ ] `difficulty` (beginner/intermediate/advanced)
  - [ ] `seo.primary_keyword`
  - [ ] `seo.canonical_url`

- [ ] **Content Quality:**
  - [ ] Minimum 800 words (series) or 600 words (standalone)
  - [ ] Active voice throughout
  - [ ] Scannable structure (H2/H3 headings)
  - [ ] Key Takeaways section present
  - [ ] What's Next section (if series post)

- [ ] **SEO:**
  - [ ] Primary keyword in title, meta description, first paragraph, at least one H2
  - [ ] Keyword density: 1–2%
  - [ ] 2–3 internal links present
  - [ ] Meta description exactly 140–160 chars

- [ ] **Images:**
  - [ ] Hero image placed at `assets/images/posts/{slug}/hero.jpg`
  - [ ] All external images have attribution
  - [ ] Attribution format: `Photo by Name on Source — License`
  - [ ] No copyrighted or restricted images

- [ ] **Links:**
  - [ ] All internal links verified (no `/coming-soon/`)
  - [ ] External links use descriptive anchor text
  - [ ] No dead links (curl or browser check)

- [ ] **Formatting:**
  - [ ] Markdown syntax valid (no broken code fences)
  - [ ] Indentation consistent
  - [ ] Lists properly formatted
  - [ ] No decorative dividers or excessive emoji

---

## References

- **Directory Structure:** [structure.md](structure.md)
- **Tech Stack:** [stack.md](stack.md)
- **PRD (Features & Content Types):** `.github/docs/LearnHub_PRD.md`
- **TRD (Front-Matter Spec):** `.github/docs/LearnHub_TRD.md`
