---
description: Generate or update your project's development constitution
argument-hint: "[context about your project, reference files/dirs]"
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

The user's input provides context for generating the constitution. Use it to inform the principles.

User input:

$ARGUMENTS

You are creating or updating the project constitution at `.specify/memory/constitution.md`. This document defines the non-negotiable development principles for the project. All downstream specs, plans, and tasks must align with it.

## Auto-Bootstrap

Before starting, ensure `.specify/memory/` exists. If not, create it.

## Execution Flow

1. **Gather context**: Read any files or directories referenced in the user's input. Scan the project for existing code, README, docs, config files, and any prior constitution to understand the project's nature.

2. **Load existing constitution** at `.specify/memory/constitution.md` if present.
   - If this is an update (existing constitution has real content, not just the placeholder), identify what's changing and apply semantic versioning:
     * MAJOR: Principle removed or fundamentally redefined
     * MINOR: New principle or section added, material expansion
     * PATCH: Clarifications, wording, typo fixes
   - If this is initial creation, start at version 1.0.0.

3. **Generate the constitution** with these sections:

```markdown
# [Project Name] Constitution

## Core Principles

### I. [Principle Name]
[Concrete, testable rules. Use MUST/SHOULD language. No vague aspirational statements.]

### II. [Principle Name]
[...]

(Generate 3-7 principles appropriate to the project. Common themes:)
- Code quality / simplicity / YAGNI
- Testing strategy (TDD, integration tests, what level of coverage)
- Architecture constraints (monolith vs services, framework choices)
- Naming conventions and code style
- Dependency management
- Error handling approach
- Documentation expectations

### [Additional Sections as Needed]
(Technology constraints, performance standards, workflow requirements — only if relevant)

## Governance

- This constitution supersedes ad-hoc decisions during development.
- Amendments require: (1) documented rationale, (2) version bump, (3) update to Last Amended date.
- All specs, plans, and tasks must be checked against these principles.
- When a principle proves wrong in practice, amend it — don't silently ignore it.

**Version**: [X.Y.Z] | **Ratified**: [YYYY-MM-DD] | **Last Amended**: [YYYY-MM-DD]
```

4. **Principle quality rules**:
   - Each principle must be testable — someone reading a PR should be able to check compliance
   - Avoid vague language: "robust", "clean", "best practices" → replace with specific rules
   - Keep principles actionable: "Tests MUST be written before implementation" not "We value testing"
   - Fewer focused principles are better than many vague ones
   - Tailor to the actual project (a CLI tool has different needs than a web app)

5. **Write** the constitution to `.specify/memory/constitution.md`.

6. **Report** to the user:
   - Version number and rationale for the version
   - List of principles with one-line summaries
   - Suggested commit message: `docs: establish constitution vX.Y.Z` (or `docs: amend constitution to vX.Y.Z`)
   - Suggest next step: "Run `/spec-kit:specify <feature description>` to create your first feature spec."
