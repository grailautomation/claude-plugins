---
name: multi-issue
description: Guide for analyzing multiple GitHub issues using parallel agents
---

# Multi-Issue Analysis Guide

When analyzing multiple GitHub issues, choose the appropriate parallelism strategy.

## Decision Matrix

| Scenario | Approach | Why |
|----------|----------|-----|
| 2-5 issues, want progressive results | Parallel agents | See results as each completes |
| 2-5 issues, want unified output | `/solve 1 2 3` | Single formatted summary |
| 5+ issues | `/solve 1 2 3 ...` | Context efficiency |
| Fault isolation needed | Parallel agents | One failure won't affect others |

## Approach 1: SDK-Level Parallelism (Batch Mode)

Use the `/issue-blaster:solve` command with multiple issue numbers:

```
/issue-blaster:solve 123 456 789
```

**Behavior**:
- The solve command spawns Task agents internally
- Uses `issue-blaster` subagent type
- Waits for all tasks to complete
- Reports unified summary

**Best for**:
- Batch processing many issues
- When you want a single unified report
- When issues are independent and similar

## Approach 2: Outer Claude Parallelism

Outer Claude directly spawns multiple `issue-blaster` agents:

```
Task(subagent_type="issue-blaster", prompt="Analyze issue #123...")
Task(subagent_type="issue-blaster", prompt="Analyze issue #456...")
Task(subagent_type="issue-blaster", prompt="Analyze issue #789...")
```

**Behavior**:
- Each agent runs independently
- Results appear progressively as agents complete
- Each agent produces a JSON summary for easy aggregation
- Failures in one agent don't affect others

**Best for**:
- Progressive result reporting
- Fault isolation between issues
- When outer Claude needs to aggregate or compare results
- When issues require different context or handling

## Aggregating Results

Each agent outputs a JSON summary block that can be collected:

```json
{
  "issue_number": 123,
  "issue_title": "Add feature X",
  "plans_created": 3,
  "recommended_option": 2,
  "recommended_effort": "medium",
  "location": "plans/issue-123/"
}
```

Outer Claude can combine results into a summary:

| Issue | Title | Plans | Recommended | Effort |
|-------|-------|-------|-------------|--------|
| #123 | Add dark mode support | 3 | Option 2 | medium |
| #456 | Fix login timeout | 2 | Option 1 | low |
| #789 | Refactor API client | 4 | Option 3 | high |

## Error Handling

- **Batch mode**: Reports per-issue status in summary table, continues on failures
- **Parallel agents**: Each failure is isolated, can retry individually

## Output Location

Both approaches write plans to the same location:

```
plans/
├── issue-123/
│   ├── option-1-minimal-fix.md
│   └── option-2-full-refactor.md
├── issue-456/
│   └── option-1-quick-patch.md
└── issue-789/
    ├── option-1-wrapper.md
    └── option-2-new-client.md
```
