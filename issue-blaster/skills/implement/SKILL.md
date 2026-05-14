---
name: implement
description: "Issue Blaster implement command: implement a selected issue plan from plans/issue-* with explicit git, validation, commit, and PR handling."
argument-hint: <issue:option> [<issue:option> ...] | <issue> <option>
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Task, AskUserQuestion
disable-model-invocation: true
---

Implement the specified solution plan(s). In Claude Code this skill is normally
invoked as `/issue-blaster:implement`. In Codex, implement directly from the
selected plan using normal repo-editing, validation, commit, push, and PR
workflow; do not rely on Claude `Task`, `TaskOutput`, or `AskUserQuestion`.

## Arguments
$ARGUMENTS

## Instructions

### Step 1: Parse Arguments

Determine the invocation style:

**Single plan — two separate numbers** (e.g., `123 1`):
- Issue number = first argument, option number = second
- Invoke the plan-implementer agent directly with: `123 1`

**Single plan — colon syntax** (e.g., `123:1`):
- Same as above, invoke directly with: `123 1`

**Multiple plans — colon syntax** (e.g., `123:1 456:2 789:1`):
- Parse each `issue:option` pair
- Proceed to parallel dispatch

**Single path** (e.g., `plans/issue-123/option-1-fix.md`):
- Invoke the plan-implementer agent directly with the path

### Step 2: Dispatch

#### Single Plan
Invoke the plan-implementer agent directly with the parsed arguments.

In Codex:
- Read the selected plan file and verify it matches the requested issue/option
- Check `git status --short --branch` before editing
- Use the current branch when that matches the user's request; create a new
  `codex/` branch or explicit worktree when isolation is needed
- Implement the plan with normal Codex file edits
- Run focused validation that matches the changed files
- Commit, push, open a PR, and merge only when the user has asked for those
  actions

#### Multiple Plans (Parallel)
For EACH issue:option pair, use the Task tool with:
- **subagent_type**: `"plan-implementer"`
- **run_in_background**: `true`
- **description**: `"Implementing issue #{issue} option {option}"`
- **prompt**: `"{issue} {option}"`

After spawning all tasks, wait for completion using TaskOutput.

In Codex:
- Do not implement multiple plans in parallel unless the user explicitly asks
  for subagents or parallel agent work
- If parallel work is authorized, use one disjoint branch/worktree per plan and
  keep ownership boundaries explicit
- If parallel work is not authorized, implement one selected plan or ask which
  plan should go first

### Step 3: Report Results

**Single plan**: The plan-implementer agent handles its own reporting.

**Multiple plans**: Output a summary table:

| Issue | Option | Branch | Worktree | Status |
|-------|--------|--------|----------|--------|
| #{N}  | {opt}  | `{branch}` | `.worktrees/{branch}` | SUCCESS/FAILED |

Then offer to merge any or all of them.
