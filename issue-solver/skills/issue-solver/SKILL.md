---
name: issue-solver
description: Workflow for analyzing GitHub issues, generating solution plans, and implementing chosen approaches. Use when working with GitHub issues, creating implementation plans, comparing solution options, editing plans, or implementing solutions.
---

# issue-solver Workflow

A two-phase approach to solving GitHub issues with AI assistance.

## Quick Reference

| Task | How | Agent |
|------|-----|-------|
| Generate plans (single) | `/issue-solver:solve 123` | issue-solver |
| Generate plans (batch) | `/issue-solver:solve 1 2 3` | issue-solver (via Task) |
| Execute plan | "implement option 1 for issue 123" | plan-implementer |

## Parallelism Approaches

| Approach | How | Best For |
|----------|-----|----------|
| Single issue | Direct agent call or `/solve N` | Normal usage |
| Batch mode | `/solve 1 2 3` (SDK parallelism) | Many similar issues |
| Outer Claude | Spawn multiple agents | Progressive results, fault isolation |

See [multi-issue.md](multi-issue.md) for detailed guidance.

## Workflow Phases

### Phase 1: Solve (Analysis)
Analyzes an issue and generates 2-4 distinct solution approaches.

**Input**: GitHub issue number(s)
**Output**: Plan files in `plans/issue-{N}/option-{n}-{slug}.md`

**Parallel Solving**: When multiple issues are provided, they are solved concurrently using the Task tool.

Each plan includes:
- Issue summary
- Implementation approach
- Step-by-step instructions
- Pros/cons and effort estimate

### Phase 2: Implement (Execution)
The `plan-implementer` agent executes a chosen plan.

**Input**: Issue + option number, OR path to plan file
**Output**: Git commits on a new branch in `.worktrees/{branch_name}`

The agent handles the full lifecycle: worktree creation, code changes, commit, merge options, and cleanup. You can defer merging by choosing "Leave it" to keep the worktree for later.

**Prerequisites**:
- Clean git working directory
- Plan file must exist

## Plan Files

Plans use YAML frontmatter + markdown. See [plan-format.md](plan-format.md) for specification.

To modify a plan before implementation, see [plan-editing.md](plan-editing.md).

## Context Tips

When asking to solve issues, include relevant context:
- "We use the repository pattern for data access"
- "Avoid modifying the legacy auth module"
- "Must maintain Python 3.9 compatibility"

This context helps generate more appropriate solutions.
