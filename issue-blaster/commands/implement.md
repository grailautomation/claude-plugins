---
description: Implement one or more chosen solution plans
argument-hint: <issue:option> [<issue:option> ...] | <issue> <option>
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Task, AskUserQuestion
---

Implement the specified solution plan(s).

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

#### Multiple Plans (Parallel)
For EACH issue:option pair, use the Task tool with:
- **subagent_type**: `"plan-implementer"`
- **run_in_background**: `true`
- **description**: `"Implementing issue #{issue} option {option}"`
- **prompt**: `"{issue} {option}"`

After spawning all tasks, wait for completion using TaskOutput.

### Step 3: Report Results

**Single plan**: The plan-implementer agent handles its own reporting.

**Multiple plans**: Output a summary table:

| Issue | Option | Branch | Worktree | Status |
|-------|--------|--------|----------|--------|
| #{N}  | {opt}  | `{branch}` | `.worktrees/{branch}` | SUCCESS/FAILED |

Then offer to merge any or all of them.
