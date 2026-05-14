---
name: issue-blaster
description: Workflow for analyzing GitHub issues, generating solution plans, and implementing chosen approaches. Use when working with GitHub issues, creating implementation plans, comparing solution options, editing plans, or implementing solutions.
---

# issue-blaster Workflow

A two-phase approach to solving GitHub issues with AI assistance. This plugin
supports Claude Code slash-command/subagent usage and Codex direct workflow
usage.

## Quick Reference

| Task | Claude Code | Codex |
|------|-------------|-------|
| Generate plans (single) | `/issue-blaster:solve 123` | Inspect the issue with `gh`, research with `rg`, then write `plans/issue-{N}/option-*.md` |
| Generate plans (batch) | `/issue-blaster:solve 1 2 3` | Process sequentially unless the user explicitly authorizes Codex subagents |
| Execute plan (single) | `/issue-blaster:implement 123:1` | Read the selected plan, verify git state, implement in the current branch or an explicit worktree |
| Execute plans (parallel) | `/issue-blaster:implement 123:1 456:2` | Only when the user explicitly authorizes parallel Codex agents with disjoint worktrees |
| Execute plan (direct) | `@issue-blaster:plan-implementer 123 1` | Use normal Codex repo-editing, validation, commit, push, and PR workflow |

## Parallelism Approaches

| Approach | How | Best For |
|----------|-----|----------|
| Single issue | Direct agent call or `/solve N` | Normal usage |
| Batch solve | `/solve 1 2 3` in Claude; sequential loop in Codex | Many issues to analyze |
| Batch implement | `/implement 123:1 456:2 789:1` in Claude; explicit Codex subagents only | Many plans to execute |
| Outer agent parallelism | Claude Task agents or user-authorized Codex subagents | Progressive results, fault isolation |

See [multi-issue.md](references/multi-issue.md) for detailed guidance.

## Workflow Phases

### Phase 1: Solve (Analysis)
Analyzes an issue and generates 2-4 distinct solution approaches.

**Input**: GitHub issue number(s)
**Output**: Plan files in `plans/issue-{N}/option-{n}-{slug}.md`

**Parallel Solving**: When multiple issues are provided, they are solved concurrently using the Task tool.

**Codex Solving**: For one issue, use `gh issue view` to fetch issue metadata,
`rg` to inspect the codebase, and local file reads to ground the plans. For
multiple issues, process them one at a time unless the user explicitly asks for
Codex subagents or parallel agent work.

Each plan includes:
- Issue summary
- Implementation approach
- Step-by-step instructions
- Pros/cons and effort estimate

### Phase 2: Implement (Execution)
The `plan-implementer` agent executes a chosen plan.

**Input**: Issue:option pair(s), OR path to plan file
**Output**: Git commits on a new branch in `.worktrees/{branch_name}`

The agent handles the full lifecycle: worktree creation, code changes, commit, merge options, and cleanup. You can defer merging by choosing "Leave it" to keep the worktree for later.

**Parallel Implementing**: `/issue-blaster:implement 123:1 456:2` dispatches multiple plan-implementer agents concurrently, each in its own worktree.

**Codex Implementing**: Implementation is explicit and inherits the current
Codex permissions and sandbox. Prefer normal Codex branch/PR workflow for one
selected plan. Use worktrees only when they reduce risk or the user asks for
isolation. Do not merge, push, or delete worktrees without explicit user intent.

**Prerequisites**:
- Clean git working directory
- Plan file must exist

## Plan Files

Plans use YAML frontmatter + markdown. See [plan-format.md](references/plan-format.md) for specification.

To modify a plan before implementation, see [plan-editing.md](references/plan-editing.md).

## Context Tips

When asking to solve issues, include relevant context:
- "We use the repository pattern for data access"
- "Avoid modifying the legacy auth module"
- "Must maintain Python 3.9 compatibility"

This context helps generate more appropriate solutions.
