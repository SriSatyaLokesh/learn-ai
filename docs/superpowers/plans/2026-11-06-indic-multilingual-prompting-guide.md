# Hands-On Indic Multilingual Prompting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author, structure, and verify a comprehensive, hands-on blog post on prompting AI coding agents directly in Telugu, Tamil, Hindi, and Kannada (via voice, code-mixed typing, and native script) without translation skills, published under LearnAI Jekyll standards.

**Architecture:** A dual-optimized (Google SEO + AI AEO citation) technical guide structured across developer lifecycle phases: Voice-driven architecture, Romanized code-mixed scaffolding, native-script traceback debugging, and the "Zero-Translation" architectural rationale backed by AI4Bharat benchmarks. Includes valid Jekyll frontmatter, answer-first paragraphs, TL;DR, citation capsules, and FAQ schema.

**Tech Stack:** Jekyll, Liquid, Markdown, GitHub CLI (`gh`).

**Spec:** [`docs/series/CONTENT-062-indic-multilingual-prompting.md`](file:///D:/professional/code/SriSatyaLokesh/learn-ai/docs/series/CONTENT-062-indic-multilingual-prompting.md)

## Global Constraints

- File destination: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`
- `layout: post` MUST be the very first line of front matter.
- `image:` MUST be root-level (not nested in `header:`).
- Meta description MUST be between 140 and 160 characters.
- Canonical URL: `https://srisatyalokesh.is-a.dev/learn-ai/indic-multilingual-prompting-guide/`
- Category MUST be `ai`; difficulty MUST be `intermediate`; author `satya-k`.
- Word count target: 2,200–2,800+ words.
- All four target languages (Telugu, Tamil, Hindi, Kannada) must be represented with concrete prompts and outputs.
- Any non-Jekyll template syntax must be escaped so Liquid doesn't fail compilation.

## Review Focus

1. **Front matter rendering failure**: If `layout: post` is missing or `image:` is inside `header:`, the page renders as plain text or loses its banner. *Check: verify exact lines 1-20 of front matter.*
2. **Liquid interpolation collisions**: Curly braces in prompt examples (e.g., `{{ variable }}` or `{% ... %}`) triggering Liquid syntax errors during Jekyll build. *Check: wrap any raw curly brace templates in `{% raw %}...{% endraw %}`.*
3. **Meta description character limit**: Ensure description is strictly 140–160 characters. *Check: character count verification.*
4. **Token efficiency assertion accuracy**: Ensure technical claims regarding BPE tokenizers and cross-lingual latent spaces accurately cite AI4Bharat / IIT Madras / IBM Research MILU benchmarks. *Check: verify citation capsule in Section 4.*
5. **Language representation balance**: Ensure no language is omitted (Telugu, Tamil, Hindi, and Kannada each receive explicit prompts and analysis). *Check: scan all H2 sections for all 4 languages.*

---

### Task 1: Front Matter, Introduction & TL;DR Box

**Files:**
- Create: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`

**Interfaces:**
- Produces: Base post file with complete valid YAML front matter, problem hook, and 50-word TL;DR block.

- [ ] **Step 1: Draft front matter adhering strictly to `blog-post-frontmatter.instructions.md`**
  - `layout: post` as line 1
  - Title: "How to Prompt AI Coding Agents in Indic Languages: A Hands-On Guide"
  - Subtitle: "Voice mode, code-mixed typing, and native scripts: prompt Telugu, Tamil, Hindi, and Kannada without translation plugins"
  - Date: `2026-11-06 17:30:00 +0530`
  - Category: `ai`
  - Tags: `[multilingual-ai, indic-languages, prompt-engineering, ai-coding-assistants, developer-productivity]`
  - Excerpt: "Prompt AI coding agents directly in Telugu, Tamil, Hindi, and Kannada. Learn voice workflows, Tenglish/Hinglish typing, and why translation plugins add latency."
  - Description: "Prompt AI agents in Telugu, Tamil, Hindi, and Kannada. Master voice mode and code-mixed typing without slow translation skills." (147 chars)
  - Image: `/assets/images/posts/indic-multilingual-prompting-guide/hero.jpg`
  - Header attribution, author `satya-k`, canonical URL.

- [ ] **Step 2: Write Introduction (150-200 words)**
  - Open with industry data on Indian developer momentum (GitHub Octoverse data: India as the fastest-growing developer population, 17M+ developers).
  - Introduce the common misconception: developers believing they need translation skills, wrappers, or English-only prompts.
  - Detail the core premise: Modern frontier models map intent directly in cross-lingual latent space.

- [ ] **Step 3: Add TL;DR Box (40-60 words)**
  - Blockquote immediately following introduction with 1 statistic and attribution.

- [ ] **Step 4: Verify front matter and description length**
  - Run powershell check on character count of `description` and line 1 validation.

---

### Task 2: Phase 1 — Spoken Architecture & Ideation (Voice Mode in Hindi & Tamil)

**Files:**
- Modify: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`

**Interfaces:**
- Consumes: Base post from Task 1.
- Produces: Section on Voice Mode hands-free system design with Hindi and Tamil spoken prompts, agent architecture output, and citation capsule.

- [ ] **Step 1: Write H2 heading in question format**
  - Heading: `## Can You Design Distributed Systems Using Spoken Indic Voice Mode?`
  - Answer-first opening paragraph (40-60 words with statistic on speech latency and frontier model voice integration).

- [ ] **Step 2: Provide Hindi Voice Prompt & Architecture Workflow**
  - Spoken prompt: Spoken architectural design for an asynchronous payment reconciliation service (Kafka + Redis + Go).
  - Agent response and architectural reasoning.

- [ ] **Step 3: Provide Tamil Voice Prompt & Edge-Case Workflow**
  - Spoken prompt in Tamil specifying rate-limiting and circuit-breaker patterns.
  - Analysis of how voice models interpret colloquial pronunciation and technical terms.

- [ ] **Step 4: Add Information Gain marker and Citation Capsule**
  - Inline callout: `> **Engineering Observation:** [Direct acoustic-to-semantic embeddings eliminate STT-English translation artifacts]`.
  - Self-contained 40-60 word citation capsule.

---

### Task 3: Phase 2 — High-Velocity Scaffolding with Code-Mixed Typing (Tenglish & Tanglish)

**Files:**
- Modify: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`

**Interfaces:**
- Consumes: Spoken voice section from Task 2.
- Produces: Section on Romanized code-mixing (Tenglish and Tanglish) with code snippets and tokenizer analysis.

- [ ] **Step 1: Write H2 heading in question format**
  - Heading: `## How Does Code-Mixed Typing (Tenglish & Tanglish) Accelerate Everyday Coding?`
  - Answer-first opening paragraph with 2026 BPE tokenizer efficiency data.

- [ ] **Step 2: Provide Tenglish Prompt & Python/FastAPI Implementation**
  - Prompt: *"Eee FastAPI endpoint lo Redis caching pettu. Cache miss aithe Postgres nunchi fetch chesi 5 minutes TTL tho save cheyali. Distributed lock kuda add cheyyi."*
  - Generated code snippet with comments.
  - Explanation of why code-mixing allows maintaining developer flow state.

- [ ] **Step 3: Provide Tanglish Prompt & React Performance Optimization**
  - Prompt: *"Intha React component-la re-rendering issue irukku. `useMemo` mattrum `useCallback` use panni optimize pannu, search input-ku 300ms debounce podu."*
  - Generated TypeScript React component snippet.

- [ ] **Step 4: Tokenizer comparison: Romanized vs. Native Unicode**
  - Table or explanation contrasting sub-word token fragmentation.
  - Citation capsule on BPE efficiency.

---

### Task 4: Phase 3 — Deep Debugging & Traceback Triaging in Native Script (Telugu & Kannada)

**Files:**
- Modify: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`

**Interfaces:**
- Consumes: Code-mixing section from Task 3.
- Produces: Section on debugging distributed tracebacks using native Telugu and Kannada scripts.

- [ ] **Step 1: Write H2 heading in question format**
  - Heading: `## Can Agents Debug Complex Stack Traces from Native Indic Script Prompts?`
  - Answer-first paragraph with AI4Bharat Indic-HumanEval benchmark data.

- [ ] **Step 2: Provide Telugu Script Debugging Prompt**
  - Native script prompt: *"ఈ Node.js క్లస్టర్‌లో కింది Stack Trace లో కనిపించే Memory Leak మరియు `UnhandledPromiseRejection` ను విశ్లేషించండి. కనెక్షన్ పూల్ సరిగ్గా డ్రైన్ అయ్యేలా పరిష్కారం ఇవ్వండి."*
  - Stack trace sample and agent's diagnosis.

- [ ] **Step 3: Provide Kannada Script Middleware & Auth Prompt**
  - Native script prompt: *"ಈ REST API ಎಂಡ್‌ಪಾಯಿಂಟ್‌ಗೆ JWT authentication ಮತ್ತು Role-Based Access Control (RBAC) middleware ರಚಿಸಿ. Expired token ಬಂದರೆ `401 Unauthorized` ಕೊಡಬೇಕು."*
  - Agent's middleware implementation.

- [ ] **Step 4: Add Information Gain marker and Citation Capsule**
  - First-hand observation on cross-lingual reasoning preserving code syntax.
  - Quotable citation capsule.

---

### Task 5: Phase 4 & 5 — The Zero-Translation Architecture, FAQ & Polish

**Files:**
- Modify: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`

**Interfaces:**
- Consumes: Debugging section from Task 4.
- Produces: Architectural analysis of why translation plugins fail, 4 best practice rules, FAQ section, and conclusion.

- [ ] **Step 1: Write Section on The "Zero-Translation" Principle**
  - Heading: `## Why Translation Plugins and Middleware Are an Anti-Pattern`
  - 3-column comparison table: Metric / Direct Prompting / Translation Middleware (Latency, Context Bloat, Semantic Drift, Technical Terms).
  - Citations of AI4Bharat and IBM MILU research.

- [ ] **Step 2: Practical Rules for Production Multilingual Prompting**
  - Rule 1: Keep syntax keywords in English.
  - Rule 2: Declare explicit output constraints.
  - Rule 3: Use native voice for high-level specs, code-mixing for implementation.

- [ ] **Step 3: FAQ Section**
  - 4 questions (35-60 word answers with stats):
    1. Do Indic prompts consume more tokens than English?
    2. Does the AI generate code with Indian language variable names?
    3. How does voice mode handle regional accents?
    4. Do I need any special settings in VS Code or Cursor?

- [ ] **Step 4: Conclusion & Actionable Checklist**
  - Summary of key takeaways.
  - 2 internal links using Liquid filters to related posts.

---

### Task 6: Verification, Local Build & Image Provisioning

**Files:**
- Create: `assets/images/posts/indic-multilingual-prompting-guide/hero.jpg` (or SVG banner fallback)
- Verify: `_posts/ai/2026-11-06-indic-multilingual-prompting-guide.md`

**Interfaces:**
- Consumes: Complete post from Task 5.
- Produces: Verified post passing Jekyll build and front-matter rules.

- [ ] **Step 1: Create hero banner asset or fallback in assets directory**
  - Ensure image path matches front matter `image:` attribute.

- [ ] **Step 2: Run Jekyll build verification**
  - Run: `bundle exec jekyll build --future`
  - Expected: Exit code 0, 0 build errors.

- [ ] **Step 3: Verify front matter and link integrity**
  - Check `layout: post`, `canonical_url`, and Liquid tags.

- [ ] **Step 4: Commit all changes to feature branch**
  - Commit message: `feat: add hands-on guide to Indic multilingual prompting` with issue reference `Resolves #62`.
