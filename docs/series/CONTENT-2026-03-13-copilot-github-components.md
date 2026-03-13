# Content Brief: The .github Folder for GitHub Copilot

**Status**: In Progress  
**Created**: 2026-03-13T00:00:00Z  
**Category**: tools  
**Type**: standalone  
**Difficulty**: beginner

---

## Phase 1: Requirements

**Status**: [x] Complete

### Topic

This post explains how the `.github` folder supports GitHub Copilot workflows in a real repository. It covers instructions, prompt files, custom agents, skills, hooks, and MCP, with emphasis on what each layer does, when it loads, and how teams should organize these layers without overlap.

### Target Audience

Developers and technical writers using GitHub Copilot in VS Code who want a practical guide to repository-level Copilot customization.

### Scope

- Explain the main `.github` customization layers used with GitHub Copilot.
- Clarify loading behavior for each layer.
- Show when to use instructions, prompts, agents, skills, hooks, and MCP.
- Provide a decision framework for choosing the right layer.
- Include practical examples and repository references.
- Keep the article accessible to new users while still useful for experienced teams.

### Out of Scope

- Deep implementation tutorials for external MCP servers.
- Product comparisons with non-Copilot platforms.
- Exhaustive documentation of every GitHub workflow file unrelated to Copilot behavior.

### Word Count Target

1800-2600 words

---

## Phase 2: Research

**Status**: [x] Complete

### Research Objective

Validate, from official GitHub and VS Code documentation, what each Copilot customization layer does, when it loads, and how to combine the layers efficiently inside a repository.

### Core Findings

1. Always-on instructions

- Primary files: `.github/copilot-instructions.md`, `AGENTS.md`, and optional compatibility files.
- Loading behavior: Automatically included in workspace chat requests.
- Best use: Repository-wide guardrails, stable conventions, and non-negotiable standards.

1. File-based instructions

- Primary files: `.github/instructions/*.instructions.md`.
- Loading behavior: Applied when `applyTo` patterns match files in context or when task relevance matches the description.
- Best use: Folder-specific or language-specific guidance.

1. Prompt files

- Primary files: `.github/prompts/*.prompt.md`.
- Loading behavior: Manually invoked through slash commands.
- Best use: Reusable one-shot workflows such as planning, research, and verification.

1. Custom agents

- Primary files: `.github/agents/*.agent.md`.
- Loading behavior: Active when selected directly or invoked as a subagent.
- Best use: Role-specific workflows with controlled tools and handoffs.

1. Skills

- Primary files: `.github/skills/<skill-name>/SKILL.md` plus optional templates or scripts.
- Loading behavior: Progressive loading based on metadata, relevance, and resource use.
- Best use: Reusable capability packs that go beyond a single prompt.

1. Hooks

- Primary files: `.github/hooks/*.json`.
- Loading behavior: Triggered by lifecycle events.
- Best use: Deterministic automation, safeguards, and governance.

1. MCP

- Primary config: `.vscode/mcp.json` or user-profile MCP config.
- Loading behavior: Available after trust approval and server startup.
- Best use: External tools, resources, prompts, and integrations.

### Loading and Use Matrix

| Component | Typical location | Loaded when | Best for | Efficiency guidance |
| --- | --- | --- | --- | --- |
| Always-on instructions | `.github/copilot-instructions.md` | Every workspace chat request | Stable repo-wide rules | Keep short and durable |
| File-based instructions | `.github/instructions/*.instructions.md` | Pattern or semantic match | Scoped rules | Use precise `applyTo` values |
| Prompt files | `.github/prompts/*.prompt.md` | Slash command invocation | Repeated workflows | Reuse structure, not policy |
| Custom agents | `.github/agents/*.agent.md` | Agent selected or invoked | Role workflows | Restrict tools by role |
| Skills | `.github/skills/<name>/SKILL.md` | On demand or relevance match | Reusable capabilities | Keep metadata specific |
| Hooks | `.github/hooks/*.json` | Lifecycle event triggers | Policy and automation | Use least privilege |
| MCP | `.vscode/mcp.json` | Trusted and started | External integrations | Prefer vetted servers |

### What To Emphasize In The Blog

- The `.github` folder is not a single Copilot config file. It is a container for multiple layers with different responsibilities.
- The main distinction is scope: global guidance, scoped guidance, reusable workflows, role behavior, reusable capabilities, enforcement, and integration.
- Clean architecture comes from giving each rule one clear home.
- Repositories such as `awesome-copilot` and `copilot-team-workflow` help readers see how these ideas look in practice.

### Risks and Caveats To Mention

- Hooks are powerful and require security review.
- Incorrect `applyTo` patterns can make scoped guidance ineffective.
- Overlapping rules across layers create drift and confusion.
- MCP should be treated as a trust boundary, not just a convenience feature.

### Sources

- [VS Code overview](https://code.visualstudio.com/docs/copilot/overview)
- [VS Code custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [VS Code custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [VS Code hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [VS Code MCP servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [GitHub custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions)
- [GitHub repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- [GitHub custom agents](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-custom-agents)
- [GitHub agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [GitHub MCP context](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp)
- [Model Context Protocol introduction](https://modelcontextprotocol.io/introduction)
- [awesome-copilot](https://github.com/github/awesome-copilot)
- [copilot-team-workflow](https://github.com/SriSatyaLokesh/copilot-team-workflow)

---

## Phase 3: SEO Planning

**Status**: [x] Complete

### SEO Goal

Rank for practical queries from developers who want to understand the `.github` folder in a GitHub Copilot workflow and structure repository guidance more effectively.

### Search Intent

- Primary intent: educational and implementation guidance.
- Reader outcome: understand which file to use, when it loads, and how to avoid overlapping guidance.

### Primary Keyword

github copilot .github folder

### Secondary Keywords

- github copilot instructions
- prompt files vs custom agents
- github copilot skills and hooks
- model context protocol github copilot
- repository copilot customization

### Recommended Title

The .github Folder for GitHub Copilot: Instructions, Prompts, Agents, Skills, Hooks, and MCP

### Alternate Titles

- What the .github Folder Does in a GitHub Copilot Workflow
- GitHub Copilot Repository Guidance Explained

### Recommended Slug

github-copilot-github-components-explained

### Meta Description

Learn how the `.github` folder organizes GitHub Copilot instructions, prompt files, agents, skills, hooks, and MCP for clearer workflows and more consistent AI output.

### Target URL

`_posts/tools/2026-03-13-github-copilot-github-components-explained.md`

### Suggested Tags

`[github-copilot, github-folder, vscode, ai-agents, developer-tools, workflows, mcp]`

### Outline

1. What the `.github` folder is.
2. Which `.github` files affect GitHub Copilot.
3. When to use global instructions.
4. When to use scoped instruction files.
5. When prompt files are better than instructions.
6. When custom agents help.
7. Why skills scale.
8. When hooks should enforce policy.
9. How MCP fits into the picture.
10. Which file to use.
11. What a clean `.github` layout looks like.
12. How to learn from example repositories.
13. FAQ.

### FAQ Targets

- What is the `.github` folder used for?
- What is the difference between `copilot-instructions.md` and `.instructions.md`?
- When should I use a prompt file instead of a custom agent?
- Are skills better than prompts?
- Is MCP required?

---

## Phase 4: Writing

**Status**: [x] Complete

### Draft Output

- Post created at `_posts/tools/2026-03-13-github-copilot-github-components-explained.md`
- Includes answer-first intro, comparison table, decision guidance, and FAQ
- Uses `awesome-copilot` and `copilot-team-workflow` as example repositories
- Refocused toward SEO, GEO, and AEO-friendly phrasing

---

## Phase 5: Formatting and Validation

**Status**: [x] Complete

### Validation Checklist

- [x] Front matter present with required core fields
- [x] Category set to `tools`
- [x] Standalone format confirmed
- [x] SEO metadata included
- [x] Main `.github` customization layers covered
- [x] Practical examples and references included
- [x] FAQ section included
- [x] Local Jekyll build verification run

### Verification Report — 2026-03-13

**Pass/Fail**: Pass

#### Requirements Alignment

- ✅ Brief and final post align on topic and target audience.
- ✅ All planned layers are covered: instructions, prompts, agents, skills, hooks, and MCP.
- ✅ Decision framework, examples, repository references, and FAQ are present.

#### Markdown and Build Check

- ✅ No editor diagnostics were reported for the post or the brief.
- ✅ Heading hierarchy, tables, images, and code fences are structurally coherent.
- ✅ `bundle exec jekyll build --future` completed successfully.

#### Fixes Confirmed

- ✅ `seo.canonical_url` now matches `_config.yml` (`url` + `baseurl`).
- ✅ Related Guides links now use `relative_url`, making them baseurl-aware and deploy-safe.

#### Code Quality

- ✅ No hardcoded credentials or sensitive values.
- ✅ Front matter complete with author, SEO fields, and tags.
- ✅ Standalone post format confirmed.

### Verdict: ✅ READY FOR PR

---

## Final Output

**Post File**: `_posts/tools/2026-03-13-github-copilot-github-components-explained.md`  
**Status**: [x] Ready for Publish
