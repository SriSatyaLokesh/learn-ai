# Git Workflow with GitHub CLI — Complete Guide

**Skill Category**: Development Process  
**Use When**: Creating branches, managing PRs, automating GitHub operations  
**Auto-loads**: When task execution, Git workflow, GitHub CLI, PR management, or issue tracking is mentioned

---

## Overview

This skill documents the complete **Git workflow with GitHub CLI automation** for this project. It covers:
- Setting up GitHub CLI
- The 10-step automated workflow
- GitHub CLI commands (working vs non-working)
- Issue-to-PR linking strategy
- Auto-merge configuration

---

## GitHub CLI Setup

### Installation & Verification

```bash
# Verify GitHub CLI is installed
which gh  # macOS/Linux
Get-Command gh  # PowerShell

# Current version check
gh --version

# On Windows: Typically installed at:
C:\Program Files\GitHub CLI\gh.exe
```

### Authentication

```bash
# Login to GitHub
gh auth login

# Use existing token
gh auth login --with-token < token.txt

# Check authentication status
gh auth status

# Refresh to update scopes
gh auth refresh -s read:project
```

### Common Auth Issues

| Issue | Solution |
|-------|----------|
| `authentication token is missing required scopes [read:project]` | Run: `gh auth refresh -s read:project` |
| `Review: Can not approve your own pull request` | This is normal - you can't approve your own PR |
| `permission denied` | Check: `gh auth status` (must show authenticated) |

---

## Complete 10-Step Git Workflow

### Step 1: Create GitHub Issue

**Purpose**: Track the work and get an issue number for branching

```bash
# Simple issue
gh issue create --title "fix: Image paths missing baseurl" \
  --body "Image paths need baseurl prefix for GitHub Pages"

# Issue with labels
gh issue create --title "fix: Something broken" \
  --body "Description here" \
  --label bug,enhancement

# ⚠️ Common mistake: Multi-line body in single quotes
# This FAILS on Windows/PowerShell:
gh issue create --title "Title" --body "Line 1
Line 2"

# Use backslash continuation or single string:
gh issue create --title "Title" --body "Line 1 and Line 2"
```

**Output**: Returns issue number (e.g., `https://github.com/owner/repo/issues/42`)

---

### Step 2: Create Feature Branch

**Naming Convention**: `<type>/<issue-number>-<description>`

```bash
# Standard format
git checkout -b fix/42-image-paths-baseurl

# Type prefixes:
# fix/    - Bug fixes
# feature/ - New features
# docs/   - Documentation
# refactor/ - Code refactoring
# style/  - CSS/styling changes
# test/   - Tests
# chore/  - Dependencies, build config
```

**Output**: `Switched to a new branch 'fix/42-image-paths-baseurl'`

---

### Step 3: Implement Changes

```bash
# Edit files as needed
# Use local build verification
bundle exec jekyll build --future

# Check for build errors
# Exit code 0 = success
# Exit code 1 = errors

# Test with local server (optional)
bundle exec jekyll serve --future --baseurl /learn-with-satya
# Visit: http://127.0.0.1:4000/learn-with-satya/
```

---

### Step 4: Commit with Issue Reference

**Critical**: Include issue number in commit message

```bash
# Format
git commit -m "fix: Add baseurl to image paths

- Updated all placeholder.png paths
- Fixed off.jpg fallbacks
- Images now load on GitHub Pages

Resolves #42"

# Or shorter
git commit -m "fix: Add baseurl to image paths (Resolves #42)"

# Keywords that auto-close issues:
# - Fixes #42
# - Resolves #42
# - Closes #42
# - Fixed #42
```

**Output**: Commit hash and file changes listed

---

### Step 5: Push Branch to Remote

```bash
# Push feature branch
git push origin fix/42-image-paths-baseurl

# Output shows:
# * [new branch] fix/42-image-paths-baseurl -> fix/42-image-paths-baseurl
# remote: Create a pull request for 'fix/42-image-paths-baseurl' on GitHub by visiting:
```

---

### Step 6: Create Pull Request with "Fixes #X"

**⚠️ CRITICAL**: PR body MUST start with `Fixes #<issue-number>` for auto-closure

```bash
# Complete PR with all info
gh pr create \
  --title "fix: Add baseurl prefix to all image paths" \
  --body "Fixes #42

## Changes
- Updated all placeholder.png paths in home.html
- Fixed off.jpg fallback images
- Images now resolve correctly on GitHub Pages

## Testing
✅ Local build passes
✅ No console errors" \
  --base main

# ⚠️ MUST include "Fixes #42" or issues won't auto-close
# ✅ Fixes #42 - auto-closes on merge
# ❌ Related to #42 - does NOT auto-close
# ❌ Closes #42 - works but "Fixes" is standard

# Output: https://github.com/owner/repo/pull/3
```

**Why "Fixes #X" is Critical**:
- GitHub detects this keyword and prevents merging without linking
- When PR merges → issue automatically closes
- Without it → issue stays open even after code is merged
- Creates zombie issues and breaks audit trails

---

### Step 7: Assign Reviewer

```bash
# Get PR number from create output, or use:
gh pr view -q  # Shows current PR info

# Assign reviewer
gh pr edit 3 --add-reviewer SriSatyaLokesh

# Verify assignment
gh pr view 3
```

**Output**: `https://github.com/owner/repo/pull/3 (OPEN)`

---

### Step 8: Approve Pull Request

```bash
# Standard approval
gh pr review 3 --approve

# Approval with comment
gh pr review 3 --approve --body "Looks good! Ready to merge."

# ⚠️ Known limitation: Can't approve your own PR
# If you create the PR, you are the author
# GitHub prevents self-approval (this is intentional)
# Solution: Have a teammate approve, or skip approval
```

**Output**: `Reviewed 1 pull request` or error if self-approval

---

### Step 9: Merge Pull Request

```bash
# Squash merge (recommended for smaller PRs)
gh pr merge 3 --squash --delete-branch

# Create merge commit (for important features)
gh pr merge 3 --create-branch --delete-branch

# Rebase merge (for clean history)
gh pr merge 3 --rebase --delete-branch

# Standard merge
gh pr merge 3 --merge --delete-branch
```

**Output**:
```
✓ Merged pull request #3 (fix: Add baseurl to image paths)
   Commit: 38ba60e
   Deleted fix/3-image-paths-baseurl branch
```

**After merge**:
- ✅ Feature branch deleted (local and remote)
- ✅ Issue auto-closes (if PR had "Fixes #X")
- ✅ Changes on main branch
- ✅ Site auto-deploys to GitHub Pages

---

### Step 10: Verify on Main Branch

```bash
# Checkout main
git checkout main

# Verify merge
git log --oneline -3

# Expected output:
# 38ba60e fix: Add baseurl to image paths (#3)
# b2931b9 fix: Progress tracking issues (#1)
# 9ad2525 updated copilot instructions
```

---

## GitHub CLI Commands Reference

### Issues

```bash
# Create issue
gh issue create --title "Title" --body "Body" --label bug

# List issues
gh issue list --state open

# View issue
gh issue view 42

# Close issue
gh issue close 42 --comment "Fixed in PR #3"

# Reopen issue
gh issue reopen 42
```

### Pull Requests

```bash
# Create PR with auto-link to issue
gh pr create --title "Title" --body "Fixes #42\n\nDetails..."

# View current PR
gh pr view

# View specific PR
gh pr view 3

# List PRs
gh pr list --state open

# Edit PR (add reviewers, assignees, labels)
gh pr edit 3 --add-reviewer SriSatyaLokesh
gh pr edit 3 --add-assignee SriSatyaLokesh
gh pr edit 3 --add-label bug

# Review PR
gh pr review 3 --approve
gh pr review 3 --request-changes
gh pr review 3 --comment "Need fix on line 42"

# Merge PR
gh pr merge 3 --squash --delete-branch

# Close PR without merge
gh pr close 3
```

### Repository

```bash
# View repo info
gh repo view

# Get current remote URL
gh repo view --json url

# Clone repo with SSH
gh repo clone owner/repo
```

---

## Complete Automated Workflow (One-Liner)

```bash
# NOT recommended (too complex) but technically works:
gh pr create --title "Your Title" --body "Fixes #42
Your description" --base main && \
sleep 2 && \
gh pr review 3 --approve && \
gh pr merge 3 --squash --delete-branch
```

**Why separate steps are better**:
- ✅ Allows verification at each stage
- ✅ Easier debugging if something fails
- ✅ Clear output and feedback
- ✅ Time for local testing before merge
- ✅ Follows professional Git practices

---

## Common Errors & Solutions

### Error: "No commits yet on this branch"
**Cause**: Pushed empty branch without changes  
**Fix**: Make changes, commit, push again
```bash
git add .
git commit -m "Initial work"
git push origin feature-branch
```

---

### Error: "cannot parse 'n' in multiline body"
**Cause**: Multi-line string in PowerShell without proper escaping  
**Fix**: Use single-line body or escape properly
```bash
# ❌ Doesn't work on Windows:
gh issue create --title "Title" --body "Line 1
Line 2"

# ✅ Works:
gh issue create --title "Title" --body "Line 1 and Line 2"

# ✅ Alternative - use @-symbol for file
echo "Line 1
Line 2" > body.txt
gh issue create --title "Title" --body-file body.txt
```

---

### Error: "Review: Can not approve your own pull request"
**Cause**: You created the PR, can't approve it yourself  
**Fix**: This is normal - skip approval or have teammate approve
```bash
# It's fine to skip step 8 when you're the author
# The PR is still valid and can be merged by maintainers
```

---

### Error: "authentication token is missing required scopes"
**Cause**: GitHub CLI authenticated but missing project scopes  
**Fix**: Refresh authentication
```bash
gh auth refresh -s read:project
# Or full scope refresh:
gh auth refresh
```

---

## Best Practices

### ✅ DO

- **Create an issue FIRST** before any work
- **Include issue number in branch name** (`fix/42-description`)
- **Start PR body with "Fixes #42"** (not "Fixes #" or just issue link)
- **Test locally before pushing** (`bundle exec jekyll build`)
- **Use squash merge** for smaller PRs (keep history clean)
- **Delete branch after merge** (keep repo tidy)
- **Verify on main** after merge (confirm changes present)
- **Reference issues in commits** (`Resolves #42`)

### ❌ DON'T

- **Commit directly to main** (always use feature branch)
- **Create PR without issue** (lose tracking)
- **Forget "Fixes #X" in PR body** (issue stays open)
- **Push without testing** (catches errors early)
- **Leave stale branches** (clean up after merge)
- **Approve your own PR** (not allowed by GitHub)
- **Merge without review** (even if you're the reviewer)

---

## Integration with Project Workflow

This Git workflow is **mandatory** for all work in `learn-with-satya`:

```
User Request
    ↓
Issue #42 created (gh issue create)
    ↓
Branch fix/42-description created
    ↓
Changes implemented locally
    ↓
Build verified (bundle exec jekyll build)
    ↓
Commit with "Resolves #42" message
    ↓
Push to origin
    ↓
PR created with "Fixes #42" in body
    ↓
Reviewer assigned (gh pr edit)
    ↓
PR approved (gh pr review --approve)
    ↓
PR merged with squash (gh pr merge --squash --delete-branch)
    ↓
Issue auto-closes ✅
    ↓
Changes live on GitHub Pages 🚀
```

---

## Testing GitHub CLI Locally

```bash
# Test issue creation (don't create dummy issues)
gh issue list --state open  # Check what exists

# Test PR listing
gh pr list --state open

# Test auth
gh auth status

# View current repo info
gh repo view
```

---

## Troubleshooting Checklist

Before running workflow:
- [ ] `gh auth status` shows authenticated
- [ ] Project is initialized as git repo (`git status` works)
- [ ] On feature branch (not main)
- [ ] Local build passes (`bundle exec jekyll build --future`)
- [ ] Changes staged (`git add .`)
- [ ] Commit message includes issue reference

Before creating PR:
- [ ] Branch pushed (`git push origin fix/42-...`)
- [ ] GitHub shows branch in repo
- [ ] Issue exists (can reference it)
- [ ] PR body starts with "Fixes #42"

---

## Recap: The One Thing That Stopped Issues Auto-Closing

**Problem**: PR #1 merged but Issue #2 stayed open  
**Root Cause**: PR body didn't include "Fixes #2" keyword  
**Solution**: Always start PR body with exactly: `Fixes #<issue-number>`  
**Mechanism**: GitHub detects this keyword and auto-closes issue on merge  
**Verification**: Check issue status after merge — should show "closed by PR #X"

This single detail prevents zombie issues and keeps audit trails clean!

---

**Last Updated**: March 11, 2026  
**Status**: Complete & Tested  
**Tool Versions**: GitHub CLI v2.88.0+, Git 2.x, Jekyll 3.10.0
