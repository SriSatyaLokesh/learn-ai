# Content Brief: Writing a New Blog on Spec-Driven Development

**Content ID**: CONTENT-058
**GitHub Issue**: <https://github.com/SriSatyaLokesh/learn-ai/issues/58>
**Status**: Written and locally verified - pull request authorized; not published
**Created**: 2026-10-03
**Branch**: content/58-spec-driven-development
**Category**: ai
**Type**: standalone
**Difficulty**: intermediate

## Phase 1: Discuss (Requirements)

**Status**: [x] Complete - approved on 2026-10-03 by the user's instruction to proceed with blog writing

### Topic

Write a new standalone blog on Spec-Driven Development (SDD): a practical guide to preserving product intent during AI-assisted development. Use the supplied SDD vs vibe coding sample as reference material, not as a post to expand or overwrite. Explain the author's Project Constitution and Plan-Implement-Verify-Replan model, its limitations, real toolkits, and a worked feature example.

### Target Audience

Developers already using AI coding assistants who need a repeatable workflow for maintainable projects, including both greenfield and brownfield repositories.

### Word Count Target

Target: 2,500-3,000 words of article prose, excluding front matter and code samples.

### Required Coverage

- Define SDD and vibe coding accurately; distinguish exploratory prototyping from accountable engineering without claiming that specifications guarantee correctness.
- Explain context rot, persistent intent, context budgets, architectural drift, and why specs must be reloaded and maintained rather than merely stored.
- Expand the constitution: mission, audience, non-goals, stack, architecture constraints, roadmap, testing, and security expectations.
- Explain greenfield interviews and brownfield discovery, with human review of inferred project rules.
- Develop Plan-Implement-Verify-Replan: requirements, measurable acceptance criteria, scoped execution, tests, review evidence, and updates when assumptions change.
- Include one coherent feature example with a short specification, acceptance criteria, an implementation plan, and verification evidence expectations.
- Explain scoped subagents and reusable skills, including coordination costs and when they are unnecessary.
- Discuss lightweight adoption, spec drift, over-documentation, prototype exceptions, and the limits of agent-as-compiler language.
- Retain ACP only with a verified explanation of its role and limits; do not equate client interoperability with automatic workflow portability.
- Explain each requested example separately, then compare its documented purpose, workflow, best fit, and limitations. Avoid unsupported rankings or treating every toolkit as the same form of SDD.

### Required Resources

| Resource | URL | Required Treatment |
| --- | --- | --- |
| Slides | <https://github.com/SriSatyaLokesh/slides/tree/main/spec-driven-development> | Clearly labeled slides link in the learning resources section |
| GitHub Spec Kit | <https://github.com/github/spec-kit> | Explain its verified specification-oriented workflow and a practical use case |
| GSD Core | <https://github.com/open-gsd/gsd-core> | Explain its documented planning/execution model and distinguish it from Spec Kit |
| Superpowers | <https://github.com/obra/superpowers> | Explain its documented skills and engineering discipline, without assuming identical SDD artifacts |
| Copilot Team Workflow | <https://github.com/SriSatyaLokesh/copilot-team-workflow> | Explain its documented team workflow and relationship to the author's phased approach |
| Course materials | <https://github.com/https-deeplearning-ai/sc-spec-driven-development-files> | Discuss its verified learning examples and place this link directly below the video player |
| Course video | <https://www.youtube.com/watch?v=hy8UstR2NEg> | Embed an accessible, responsive YouTube iframe with a descriptive title, fullscreen support, and no autoplay; retain a watch-on-YouTube link |

### Acceptance Criteria

1. A new standalone article meets the approved word-count target, explains the supplied core model, and includes the worked feature example and all five repository explanations. The sample post remains unchanged.
2. All seven supplied URLs are represented. The YouTube iframe uses video ID `hy8UstR2NEg`, and the course GitHub link appears directly below the player. The player fits mobile and desktop widths.
3. Technical descriptions are checked against primary sources. The article contains no unverified performance promises, invented toolkit commands, or claims about course contents not supported by reviewed materials.
4. Front matter includes `layout: post` as its first field, root-level image and attribution, category `ai`, a 140-160-character description, and a canonical URL matching the approved new slug. Add 2-3 relevant Liquid-based internal links and a concise FAQ.
5. Write publishable content rather than carrying over editorial placeholders from the sample. Any non-Jekyll template syntax in examples is escaped for Liquid processing.
6. Run the Jekyll build with future posts enabled and inspect the rendered article and responsive video before publication. Preserve unrelated work; do not publish or merge without verification.

### Editorial Options

- Recommended: a practical guide with one worked example and a concise toolkit comparison. This develops the author's ideas into a new, readable article.
- Alternative: an exhaustive toolkit installation tutorial. More hands-on, but substantially longer and sensitive to version-specific command changes.
- Alternative: a short conceptual overview with resource links. Easier to scan, but offers less depth than the requested detailed guide.

### Out of Scope

- Expanding, overwriting, or publishing the supplied sample post as part of this issue.
- Installing the linked toolkits or modifying their repositories.
- Rebuilding the site's design or changing shared templates solely for this post.
- Reproducing slides, course transcripts, or third-party documentation verbatim.
- Publishing, committing, pushing, or merging during issue setup.

## Phase 2: Research

**Status**: [x] Complete - primary sources reviewed on 2026-10-03

### Source Findings

- Spec Kit's current README describes constitution, specify, plan, tasks, implement, and converge. Invocation syntax varies by integration; its methodology document still contains dotted command examples. Describe stages rather than present one universal command syntax. Source: <https://github.com/github/spec-kit> and <https://github.com/github/spec-kit/blob/main/spec-driven.md>.
- GSD Core documents Discuss -> Plan -> Execute -> Verify -> Ship, fresh-context subagents, and durable state/decision artifacts. Its context-engineering explanation explicitly acknowledges overhead, latency, and lighter paths for small changes. Sources: <https://github.com/open-gsd/gsd-core> and <https://github.com/open-gsd/gsd-core/blob/next/docs/explanation/context-engineering.md>.
- Superpowers describes brainstorming, approved design, small implementation plans, TDD, agent execution, code review, and branch completion. Present it as composable engineering skills, not an identical implementation of Spec Kit. Source: <https://github.com/obra/superpowers>.
- Copilot Team Workflow documents Discuss -> Research -> Plan -> Execute -> Verify, repository instructions/prompts/agents/skills/hooks, and documentation templates. Its V2 README uses local work folders, unlike this site's content-brief convention; distinguish local execution logs from shared reviewed specs. Source: <https://github.com/SriSatyaLokesh/copilot-team-workflow>.
- DeepLearning.AI's course materials include AgentClinic snapshots for constitution creation, feature specification/implementation/validation, replanning, MVP, legacy support, skills, and agent replaceability. The README identifies `specs/mission.md`, `tech-stack.md`, `roadmap.md`, and phase `plan.md`, `requirements.md`, `validation.md`. Source: <https://github.com/https-deeplearning-ai/sc-spec-driven-development-files>.
- The official course page identifies instructor Paul Everitt and partnership with JetBrains. Source: <https://www.deeplearning.ai/short-courses/spec-driven-development-with-coding-agents/>.
- YouTube's watch page rejected direct retrieval, but its oEmbed endpoint verified video `hy8UstR2NEg`, title "Full Course: Spec-Driven Development with Coding Agents", publisher DeepLearningAI, and an embed URL. Playback remains subject to browser/network restrictions. Metadata: <https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dhy8UstR2NEg&format=json>.
- The slides directory contains two PDFs. Link the directory without claiming to have read the PDF contents. Source: <https://github.com/SriSatyaLokesh/slides/tree/main/spec-driven-development>.
- ACP standardizes agent-editor communication; it does not guarantee instruction-file, skill, permission, or workflow compatibility. Source: <https://agentclientprotocol.com/overview/introduction>.

### Site Findings and Risks

- `_config.yml` uses `/:title/`, which matches a slug-only canonical URL under `/learn-ai/`.
- `_layouts/post.html` renders `page.image` and uses `header.credit` / `header.credit_url`. Include these alongside the required `image_credit` fields rather than alter shared layout code.
- No existing YouTube embed was found in the targeted post search. Keep responsive iframe styling local to the new article and use a descriptive title, lazy loading, fullscreen, no autoplay, and a watch-link fallback.
- Use verified existing internal slugs for Copilot repository customization, context documentation, and software factories.
- Do not copy claims of guaranteed correctness, fixed context-window sizes, productivity percentages, or exact completion times from promotional descriptions.
- The existing sample is untracked user work and must remain unchanged. No shared application files need edits.

## Phase 3: Plan (SEO & Outline)

**Status**: [x] Complete - user authorized autonomous execution of the proposed outline for later review on 2026-10-03

### Proposed Publication

- Title: "Spec-Driven Development: A Practical Guide to Building with AI"
- Primary keyword: "Spec-Driven Development"
- Secondary keywords: vibe coding, context engineering, project constitution, AI coding workflow, Spec Kit, GSD Core.
- Date: 2026-10-03 11:00:00 +0530.
- New post: `_posts/ai/2026-10-03-spec-driven-development-practical-guide.md`.
- Canonical URL: <https://srisatyalokesh.is-a.dev/learn-ai/spec-driven-development-practical-guide/>.
- Format: practical guide, standalone, intermediate; target 2,500-3,000 prose words.
- Cover image: user-provided Microsoft Dev Blogs Spec Kit workflow image, <https://devblogs.microsoft.com/wp-content/uploads/2026/06/GitHub-Spec-Kit-Workflow.webp>, with matching source attribution.

### Outline and Word Budget

| Section | Purpose | Approximate Prose Words |
| --- | --- | --- |
| Opening and SDD definition | Answer-first definition and an everyday failure example | 220 |
| Vibe coding and context rot | Explain scope, persistent intent, and a concise comparison | 300 |
| Project Constitution | Mission, stack, roadmap, guardrails, and a small example | 330 |
| Greenfield and brownfield | Interview versus evidence-based discovery | 180 |
| Plan-Implement-Verify-Replan | Scoped contexts, tests, verification evidence, amendments | 390 |
| Worked reading-progress feature | Requirements, acceptance criteria, implementation boundaries, verification | 350 |
| Toolkit examples | Spec Kit, GSD Core, Superpowers, Copilot Team Workflow, course materials, comparison | 570 |
| Skills, subagents, and ACP | Benefits, coordination cost, interoperability limits | 210 |
| Adoption and pitfalls | Lightweight start, spec drift, ownership, prototypes | 170 |
| Course, slides, takeaways, FAQ | Embedded video, direct course link below, slides, concise FAQ | 230 |

### Execution and Verification Tasks

1. Write the new article with sourced claims, original illustrative examples, and no invented personal experience or measured results.
2. Include the hero image and valid attribution, matching front matter and canonical slug, a 140-160-character description, and relevant internal links using `relative_url`.
3. Add a local 16:9 YouTube iframe, then the course GitHub link immediately below. Include watch-on-YouTube and slides links.
4. Check Markdown diagnostics, prose word count, required URLs, front matter, iframe attributes/order, and sample preservation.
5. Build Jekyll with future posts enabled; inspect rendered content and internal links. Serve locally and check desktop/mobile player dimensions and screenshot evidence, reporting any third-party playback restrictions.
6. Update this brief and local phase logs with actual verification outcomes. Do not commit, push, publish, or merge without explicit authorization.

## Phase 4: Execute (Write Content)

**Status**: [x] Complete

Created `_posts/ai/2026-10-03-spec-driven-development-practical-guide.md` using the authorized outline. Includes the constitution, greenfield/brownfield adoption, Plan-Implement-Verify-Replan loop, illustrative reading-progress feature, five repository explanations and comparison, skills/subagents/ACP caveats, adoption advice, course player, slides, takeaways, and five FAQs. The original sample remains unchanged.

No shared templates, configuration, or application logic changed. The user authorized committing, pushing, and opening a pull request on 2026-10-03. Merge and publication remain pending.

## Phase 5: Verify

**Status**: [x] Complete - local article checks passed

### Verification Results

- Content checker: 2,991 body words after excluding fenced code, HTML, and Markdown link destinations; within the approved range. SEO description: 157 characters.
- Required repositories, slides, video URL, and embed ID are present. The rendered course GitHub paragraph immediately follows the iframe wrapper.
- Markdown diagnostics: no errors in the article or brief. The required HTML embed has a narrowly scoped MD033 exception.
- Front matter: first field `layout: post`, root image, valid category, attribution fields for both instruction and actual layout conventions, approved date/title/slug, and required canonical URL.
- Build: `bundle exec jekyll build --future --baseurl /learn-ai` exited successfully; the preview server's subsequent build also succeeded.
- Desktop browser check at 1440px: player 730 x 410.625px, 16:9 aspect ratio, fullscreen attribute and descriptive title present, hero image loaded.
- Cover update: rebuilt successfully with the user-provided Microsoft Dev Blogs image; browser verified it loaded at a natural size of 752 x 482px and displayed the matching source credit.
- Mobile browser check at 390px: player approximately 375.2 x 211.05px, 16:9 aspect ratio, player and article title fit the viewport.
- Desktop and mobile screenshots show the actual course thumbnail and YouTube controls. Full video playback was not tested; the article includes a watch-on-YouTube fallback for browser/network restrictions.
- All three internal article links returned HTTP 200 and use the `/learn-ai/` base path.
- The `code-reviewer` agent found no material issues in the supplied article excerpts and verification evidence. Its workspace access was unavailable, so this was an excerpt review, not whole-repository verification.
- Git status confirms the original sample remains separate untracked user work; only the new article and this brief were added as tracked-work candidates. Local phase logs were updated separately.

**Preview**: <http://127.0.0.1:4081/learn-ai/spec-driven-development-practical-guide/>
**Verdict**: Ready for pull request review; PR creation authorized by the user. Merge and publication remain pending explicit authorization.

## Final Output

**Post File**: `_posts/ai/2026-10-03-spec-driven-development-practical-guide.md`
**Reference Sample**: `_posts/ai/2026-10-03-spec-driven-development-vs-vibe-coding.md` (leave unchanged).
**Status**: [ ] Not Published
