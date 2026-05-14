---
name: spec-kit-guide
description: Use when the user asks how to use the spec-kit plugin, wants advice on spec-driven development, needs help choosing the next spec-kit workflow step, or asks for review of existing .specify specs, plans, tasks, constitution, or project context.
---

# Spec Kit Guide

Spec Kit is a streamlined Spec-Driven Development workflow for Claude Code and
Codex. It aims to deliver most of upstream GitHub Spec Kit's value with less
ceremony, especially inside existing repositories.

## Core Workflow

Canonical flow:

```text
/spec-kit:init -> /spec-kit:constitution -> /spec-kit:specify -> /spec-kit:clarify -> /spec-kit:plan -> /spec-kit:tasks -> /spec-kit:analyze -> /spec-kit:implement next
```

Minimum useful flow:

```text
/spec-kit:specify -> /spec-kit:plan -> /spec-kit:tasks -> /spec-kit:implement next
```

Use `/spec-kit:clarify` when the spec has material ambiguity. Use
`/spec-kit:analyze` before broad implementation or when artifacts drift.

Claude Code exposes the workflow through `/spec-kit:*` slash entries. Codex
exposes the same workflow skills with `$spec-kit:*`, for example
`$spec-kit:specify` or `$spec-kit:implement next`. The documented plugin source
surface is `skills/`, not `commands/`.

## Brownfield Defaults

- Treat existing repo conventions as the default architecture.
- Prefer the current package manager, test framework, modules, helpers, naming,
  and docs.
- Do not add frameworks, top-level directories, or abstraction layers unless the
  plan documents why existing patterns are insufficient.
- Use local-only `.specify/memory/project-context.md` to reduce repeated prompting.
- Keep changes small enough for one focused review.

## Workflow Roles

- `/spec-kit:init`: creates `.specify/`, a placeholder constitution, and project
  context. It should not initialize git unless explicitly asked.
- `/spec-kit:constitution`: creates pragmatic solo-dev guardrails with documented
  waiver support.
- `/spec-kit:specify`: turns a feature idea into a spec focused on what and why.
- `/spec-kit:clarify`: asks up to five high-impact questions and writes answers
  back to the spec.
- `/spec-kit:plan`: maps the spec to the existing repo with quality gates and
  verification commands.
- `/spec-kit:tasks`: creates dependency-ordered, file-specific tasks.
- `/spec-kit:analyze`: read-only consistency, coverage, and safety analysis.
- `/spec-kit:implement`: executes `next`, a named `phase`, or `all`; default to
  `next` for brownfield safety.

## Good Artifacts

A good spec:
- Has testable FR/NFR items and measurable acceptance criteria.
- Names material unknowns with `[NEEDS CLARIFICATION: ...]`.
- Includes explicit scope boundaries.
- Avoids implementation details unless the existing repo imposes them.

A good plan:
- Names exact existing files/modules/patterns to follow.
- Identifies verification commands or records why they are unknown.
- Documents constitution deviations and compensating validation.
- Flags risky migrations, external calls, credentials, and destructive steps.

A good task list:
- Uses exact file paths.
- Maps work to FR/NFR IDs or acceptance scenarios.
- Marks `[P]` only for independent files.
- Includes focused verification and context-update tasks where useful.

## Advisory Mode

When reviewing existing `.specify/` artifacts, start with the user's active goal:
planning, tasking, analysis, or implementation. Keep recommendations concrete:
which workflow step to run, which file to edit, or which gate is missing.
