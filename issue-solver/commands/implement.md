---
description: Execute a chosen solution plan
argument-hint: <issue-number> <option> | <path-to-plan.md>
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

Implement the specified solution plan.

## Arguments
$ARGUMENTS

## Prerequisites
- Git working directory must be clean (no uncommitted changes)
- Plan file must exist

## Instructions

### Step 1: Check Git Status

```bash
git status --porcelain
```

If output is non-empty, warn the user about uncommitted changes and STOP.

### Step 2: Locate Plan File

Parse $ARGUMENTS to determine the plan file:

**If two numeric arguments** (e.g., `123 1`):
- Issue number = first argument
- Option number = second argument
- Find plan at: `plans/issue-{issue}/option-{option}-*.md`

**If single path argument** (e.g., `plans/issue-123/option-1-fix.md`):
- Use the provided path directly

Verify the plan file exists before continuing.

### Step 3: Read Plan Frontmatter

Read the plan file and extract from YAML frontmatter:
- `issue_number`
- `title`
- `option`

### Step 4: Create Worktree

Generate branch name from frontmatter:
- Format: `issue-{issue_number}-{slug}`
- `{slug}` = title in lowercase, spaces to hyphens, max 50 chars

Determine worktree location:
```bash
repo_name=$(basename $(git rev-parse --show-toplevel))
worktree_path="../${repo_name}-worktrees/{branch_name}"
```

Check if worktree already exists:
```bash
git worktree list | grep -q "{branch_name}"
```
If exists, ask user whether to reuse or remove it.

Create worktree with new branch:
```bash
mkdir -p "../${repo_name}-worktrees"
git worktree add "../${repo_name}-worktrees/{branch_name}" -b {branch_name}
```

Report the worktree path to the user. Store `worktree_path` for subsequent steps.

### Step 5: Execute Implementation

Use the plan-implementer agent to execute the plan. Pass the `worktree_path` so the agent knows where to make changes.

The agent will:
1. Read the full plan
2. Execute each implementation step **within the worktree directory**
3. Verify changes
4. Run tests if available
5. Create a commit

### Step 6: Report Results

Report on:
- Worktree created: `{worktree_path}`
- Branch created: `{branch_name}`
- Commits made
- Files changed
- Any errors encountered

### Step 7: Analyze Merge Options

After implementation completes, analyze the git state to determine available merge strategies:

```bash
# Count commits on feature branch not on main
git log --oneline main..HEAD

# Count commits on main not on feature branch
git log --oneline HEAD..main

# Get common ancestor
git merge-base main HEAD
```

Determine the merge situation:
- **Fast-forward possible**: main has 0 commits since branching (most common for quick fixes)
- **Diverged**: main has new commits - requires merge commit, rebase, or PR

### Step 8: Offer Merge Options

Present options to the user based on the analysis:

**If fast-forward is possible:**
> Main hasn't moved since you branched. You can do a clean fast-forward merge:
>
> | Option | Command | Description |
> |--------|---------|-------------|
> | 1. Fast-forward (Recommended) | `git checkout main && git merge --ff-only {branch}` | Moves main pointer forward, no merge commit |
> | 2. Create PR | `gh pr create` | For code review before merging |
>
> Which would you prefer?

**If branches have diverged:**
> Main has new commits since you branched. Options:
>
> | Option | Command | Description |
> |--------|---------|-------------|
> | 1. Create PR (Recommended) | `gh pr create` | Handles merge via GitHub with review |
> | 2. Merge commit | `git checkout main && git merge {branch}` | Creates merge commit |
> | 3. Rebase | `git rebase main && git checkout main && git merge --ff-only {branch}` | Replay commits on top of main |
>
> Which would you prefer?

Use the AskUserQuestion tool to get the user's choice.

### Step 9: Execute Merge

All merge commands run from the **main repository** (not the worktree).

Based on user's choice:

**Fast-forward merge:**
```bash
git merge --ff-only {branch_name}
```

**Create PR:**
```bash
git push -u origin {branch_name}
gh pr create --title "{commit_title}" --body "Fixes #{issue_number}"
```
Report the PR URL.

**Merge commit:**
```bash
git merge {branch_name}
```

**Rebase:**
```bash
# Rebase in worktree first
cd {worktree_path}
git rebase main
cd -
# Then fast-forward merge
git merge --ff-only {branch_name}
```

### Step 10: Push to Remote

After successful merge to main (skip for PR workflow):

```bash
git push origin main
```

### Step 11: Cleanup Worktree

Remove the worktree after completion:

```bash
git worktree remove {worktree_path}
```

Delete local branch if merged (not for PR workflow):
```bash
git branch -d {branch_name}
```

Report completion:

**For merge (fast-forward, merge commit, or rebase):**
> ✓ Merged `{branch_name}` into main
> ✓ Pushed to origin/main
> ✓ Cleaned up worktree at `{worktree_path}`
>
> Issue #{issue_number} fix is now live on main.

**For PR:**
> ✓ Pushed `{branch_name}` to origin
> ✓ Created PR: {pr_url}
> ✓ Cleaned up worktree at `{worktree_path}`
>
> Issue #{issue_number} will close when PR is merged.
