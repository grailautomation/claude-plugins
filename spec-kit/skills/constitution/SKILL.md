---
name: constitution
description: "Use when the user invokes $spec-kit:constitution or /spec-kit:constitution, or asks to generate or update a pragmatic solo-dev project constitution."
argument-hint: "[context about your project, reference files/dirs]"
allowed-tools: [Read, Write, Glob, Grep, Bash]
disable-model-invocation: true
---

# Spec Kit Constitution

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

User input:

$ARGUMENTS

Create or update `.specify/memory/constitution.md`. The constitution is a small
set of guardrails for future specs, plans, and tasks. For this plugin, it must
be useful to a solo indie developer working in existing repos, not a ceremonial
process document.

## Preflight

1. Ensure `.specify/memory/` exists.
2. Run the context detector if available:
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect-project-context.sh" --write
   ```
3. Read project context, README, AGENTS.md, package/tooling files, and any
   existing constitution.

## Constitution Style

Generate 4-7 principles. Prefer these themes unless project context demands
otherwise:
- Existing architecture first
- Small, reviewable changes
- Risk-proportional testing and verification
- Clear contracts for data, APIs, jobs, CLI, or UI behavior
- Safety around migrations, credentials, external services, and destructive
  operations
- Documentation/context updates only when they reduce future prompting

## Required Waiver Language

Include a governance rule like:

"Documented waivers are allowed for solo-dev pragmatism. A waiver must name the
principle, explain why the simpler compliant option is worse for this change,
and record the compensating validation in `plan.md`."

This keeps the constitution authoritative without forcing upstream Spec Kit's
library-first, CLI-first, or strict TDD rules onto every brownfield repo.

## Output Structure

Write:

```markdown
# [Project Name] Constitution

## Core Principles

### I. [Principle]
[Concrete MUST/SHOULD rules and brief rationale]

### II. [Principle]
...

## Brownfield Workflow
[Rules for fitting existing repos]

## Quality Gates
[How plans/tasks prove compliance]

## Governance
[Versioning, amendment, waiver, and review rules]

**Version**: [X.Y.Z] | **Ratified**: [YYYY-MM-DD] | **Last Amended**: [YYYY-MM-DD]
```

## Versioning

- Initial real constitution: `1.0.0`
- MAJOR: principle removed or fundamentally redefined
- MINOR: principle or required gate added
- PATCH: clarification, wording, or non-semantic tightening

## Sync Impact

Do not update every template like upstream Spec Kit. Instead, report the
affected gates/artifacts:
- `plan.md` constitution compliance
- `tasks.md` quality gates
- `.specify/memory/project-context.md`
- Any repo guidance file such as `AGENTS.md`, only if the user asks

## Report

Report:
- Version and bump rationale
- Principle list with one-line summaries
- Any deferred TODOs
- Suggested commit message
- Next workflow step: `/spec-kit:specify <feature description>`
