---
description: Analyze GitHub issues and generate solution plans
argument-hint: <issue-numbers> [--repo owner/repo]
allowed-tools: Bash, Read, Write, Glob, Grep, Task
---

Analyze the specified GitHub issue(s) and generate 2-4 solution plans.

## Arguments
$ARGUMENTS

## Instructions

### Step 1: Parse Arguments

Extract from $ARGUMENTS:
- Issue numbers (one or more integers)
- Optional `--repo owner/repo` flag

### Step 2: Detect Repository

If `--repo` not provided, detect it:
```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

### Step 3: Validate Issues

For each issue number, verify it exists:
```bash
gh issue view {number} --repo {repo} --json number
```

### Step 4: Solve Issues

#### Single Issue
If only one issue number is provided:
- Use the issue-solver agent directly to analyze the issue
- The agent will create plans in `plans/issue-{N}/`

#### Multiple Issues (Parallel)
If multiple issue numbers are provided, spawn parallel Task agents:

For EACH issue number, use the Task tool with:
- **subagent_type**: `"general-purpose"`
- **run_in_background**: `true`
- **description**: `"Solving issue #{N}"`
- **prompt**: Include the full issue-solver instructions:
  ```
  You are a senior software architect. Analyze GitHub issue {repo}#{number}.

  1. Fetch the issue: gh issue view {number} --repo {repo} --json number,title,body,comments,labels
  2. Research the codebase with rg (ripgrep)
  3. Create directory: mkdir -p plans/issue-{number}
  4. Write 2-4 plan files at plans/issue-{number}/option-{n}-{slug}.md

  Each plan must have YAML frontmatter with: issue_number, issue_url, repo, option, title, created, status, effort, breaking_changes

  Output a summary table when done.
  ```

After spawning all tasks, wait for completion using TaskOutput.

### Step 5: Report Results

Output a summary:

| Issue | Status | Plans Created | Location |
|-------|--------|---------------|----------|
| #{N}  | SUCCESS | {count} options | `plans/issue-{N}/` |

**Total**: {X}/{Y} issues solved successfully

### Step 6: Offer Follow-up

Offer to:
- Summarize the options for any issue
- Compare trade-offs between approaches
- Explain any option in detail
