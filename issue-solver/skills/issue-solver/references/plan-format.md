---
name: plan-format
description: Specification for issue-solver plan file format
---

# Plan File Format

Plan files are markdown with YAML frontmatter.

## Location

```
plans/
└── issue-{number}/
    ├── option-1-{slug}.md
    ├── option-2-{slug}.md
    └── option-3-{slug}.md
```

## YAML Frontmatter

```yaml
---
issue_number: 123
issue_url: https://github.com/owner/repo/issues/123
repo: owner/repo
option: 1
title: "Brief Approach Name"
created: 2024-12-18T10:30:00Z
status: proposed          # proposed | accepted | implemented | rejected
effort: medium            # low | medium | high
breaking_changes: false   # true | false
---
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `issue_number` | int | GitHub issue number |
| `issue_url` | string | Full URL to the issue |
| `repo` | string | Repository in `owner/repo` format |
| `option` | int | Option number (1-4) |
| `title` | string | Short name for this approach |
| `created` | ISO 8601 | When plan was generated |
| `status` | enum | Current status of this plan |
| `effort` | enum | Estimated implementation effort |
| `breaking_changes` | bool | Whether this introduces breaking changes |

## Markdown Body Structure

```markdown
# Option {N}: {Title}

## Issue Summary
Brief description of what the issue asks for.

## Approach
High-level explanation of this solution strategy.

## Pros
- Advantage 1
- Advantage 2

## Cons
- Disadvantage 1
- Disadvantage 2

## Implementation Plan

### Step 1: {Description}
- **File**: `path/to/file.py`
- **Action**: create | modify | delete
- **Changes**: Description of what to change

### Step 2: {Description}
...
```
