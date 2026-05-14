---
name: solve
description: "Issue Blaster solve command: analyze GitHub issue numbers and generate 2-4 solution plans using gh, rg, and repo-local research."
argument-hint: <issue-numbers> [--repo owner/repo]
allowed-tools: Bash, Read, Write, Glob, Grep, Task
disable-model-invocation: true
---

Analyze the specified GitHub issue(s) and generate 2-4 solution plans. In
Claude Code this skill is normally invoked as `/issue-blaster:solve`. In Codex,
use the same workflow directly from the user's prompt; do not rely on Claude
`Task` or `TaskOutput` dispatch.

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
- Use the issue-blaster agent directly to analyze the issue
- The agent will create plans in `plans/issue-{N}/`

In Codex:
- Fetch issue details with `gh issue view {number} --repo {repo} --json number,title,body,comments,labels,assignees,url`
- Research the local codebase with `rg`, `git grep`, and targeted file reads
- Create `plans/issue-{N}/`
- Ensure `plans/` is ignored if writing plan files in the current repo
- Write 2-4 plan files using the format in `references/plan-format.md`
- Report the recommended option and plan file locations

#### Multiple Issues (Parallel)
If multiple issue numbers are provided, spawn parallel Task agents:

For EACH issue number, use the Task tool with:
- **subagent_type**: `"issue-blaster"`
- **run_in_background**: `true`
- **description**: `"Solving issue #{N}"`
- **prompt**: `"Analyze GitHub issue {repo}#{number}. The repository is {repo}."`

After spawning all tasks, wait for completion using TaskOutput.

In Codex:
- Process multiple issues sequentially by default
- Use Codex subagents only when the user explicitly asks for parallel agent work
- If subagents are authorized, assign one issue per subagent and keep write
  ownership disjoint by issue plan directory
- Aggregate each issue's JSON summary after all work completes

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
