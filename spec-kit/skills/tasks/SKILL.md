---
name: tasks
description: "Use when the user invokes $spec-kit:tasks or /spec-kit:tasks, or asks to generate dependency-ordered tasks from the plan and repo context."
argument-hint: "[additional context]"
allowed-tools: [Read, Write, Bash, Glob, Grep]
disable-model-invocation: true
---

# Spec Kit Tasks

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

User input:

$ARGUMENTS

Generate `tasks.md` for the active feature. Tasks must be immediately usable by
Codex in the current repository, not a generic template.

## Feature Detection

Run from the project root:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```

Parse JSON for `SPECS_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, `FEATURE_SOURCE`, and
`PROJECT_CONTEXT`. If no active feature is found, instruct the user to run
`/spec-kit:specify` or set `SPECIFY_FEATURE`.

## Inputs

Load:
- `plan.md` from `SPECS_DIR` (required)
- `spec.md` from `SPECS_DIR` (required)
- `PROJECT_CONTEXT`, if present
- `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, if present

Abort if `plan.md` is missing. Do not fabricate missing design artifacts; adapt
the task list to what exists.

## Task Generation Rules

- Every task must name exact files or exact discovery work.
- Every implementation task should map to one or more FR/NFR IDs or acceptance
  scenarios when possible.
- Use existing repo commands from `project-context.md` or `plan.md`; if unknown,
  create a task to identify the command before implementation.
- Tests come before or alongside implementation according to the repo's normal
  practice. Strict TDD is preferred only when it fits the codebase.
- Mark `[P]` only when tasks touch different files and have no dependency.
- Do not create new top-level packages/directories unless the plan justified it.
- Include safety tasks for migrations, destructive changes, credentials,
  external services, or generated artifacts when applicable.
- Include a local project-context refresh task if the feature changes stack,
  commands, or important repo conventions.

## Output Format

Write `SPECS_DIR/tasks.md`:

```markdown
# Tasks: [FEATURE NAME]

**Plan**: [relative path to plan.md]
**Generated**: [today's date]
**Mode**: Brownfield

## Quality Gates
- [ ] Existing repo patterns identified
- [ ] Verification commands identified
- [ ] Risky operations flagged
- [ ] Requirements mapped to tasks
- [ ] Parallel tasks touch independent files

## Phase 1: Setup / Discovery
- [ ] T001 [specific setup or discovery task] in [path]

## Phase 2: Tests / Validation First
- [ ] T002 [P] [specific test or validation task] in [path]

## Phase 3: Core Implementation
- [ ] T003 [specific implementation task] in [path]

## Phase 4: Integration / Safety
- [ ] T004 [integration, migration, logging, auth, or safety task] in [path]

## Phase 5: Polish / Verification
- [ ] T005 Run [exact command] and record result
- [ ] T006 Refresh local `.specify/memory/project-context.md` if conventions changed

## Dependencies
- [specific dependency notes]

## Parallel Execution Guide
- [groups of `[P]` tasks that can run together]
```

## Validation Before Writing

Check:
- Each FR/NFR or acceptance scenario has at least one task or a documented waiver.
- No `[P]` tasks edit the same file.
- Verification commands are present.
- Tasks are small enough for one focused Codex pass.
- There is no vague task like "implement feature" without file path and outcome.

## Report

After writing, report:
- Path to tasks file
- Total task count
- Breakdown by phase
- Parallel-eligible count
- Any requirements intentionally deferred or waived
- Suggested next command: `/spec-kit:analyze` before broad implementation, or
  `/spec-kit:implement next` for the first task
