---
name: implement
description: "Use when the user invokes $spec-kit:implement or /spec-kit:implement, or asks to safely execute spec-kit tasks in next, phase, or all mode."
argument-hint: "[next|phase <name>|all]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
disable-model-invocation: true
---

# Spec Kit Implement

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

User input:

$ARGUMENTS

Execute tasks from `tasks.md` with a Codex-safe brownfield preflight. Default
mode is `next` unless the user explicitly asks for `phase` or `all`.

## Feature Detection

Run from the project root:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```

Parse JSON for `SPECS_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, and
`PROJECT_CONTEXT`. All paths must be absolute.

## Required Inputs

Load:
- `SPECS_DIR/tasks.md` (required)
- `SPECS_DIR/plan.md` (required)
- `SPECS_DIR/spec.md` (required)
- `PROJECT_CONTEXT`, if present
- Optional design artifacts: `data-model.md`, `contracts/`, `research.md`,
  `quickstart.md`

Abort if `tasks.md` or `plan.md` is missing.

## Modes

- `next`: complete the first unchecked task only. This is the default.
- `phase <name>`: complete unchecked tasks in the named phase.
- `all`: complete all unchecked tasks. Before proceeding, summarize scope and
  ask for explicit confirmation.

## Safety Preflight

Before editing:
1. Inspect `git status --short --branch`.
2. Identify files with user changes. Do not overwrite, revert, or reformat
   unrelated changes.
3. Read target files before editing them.
4. Identify destructive operations, migrations, external service calls,
   credential use, generated artifact churn, or production-impacting commands.
   Ask for explicit confirmation before running those steps.
5. Confirm verification commands from `tasks.md`, `plan.md`, or
   `project-context.md`.

If the task is too broad or lacks exact files/outcomes, stop and recommend
regenerating or editing `tasks.md`.

## Execution Rules

- Complete only the selected mode's scope.
- Respect dependencies and phase ordering.
- `[P]` means tasks may be done in any order, not that Codex must spawn agents.
- Keep edits scoped to the task's files.
- Write tests before or alongside implementation according to the task and repo
  practice.
- After completing a task, mark it `[X]` in `tasks.md`.
- If a non-parallel task fails, stop and report the blocker.
- For phase/all mode, run focused verification after each phase when commands
  are known.

## Completion Validation

Before reporting:
- Confirm selected task(s) are marked `[X]`.
- Run the focused verification command when available and not destructive.
- Check implementation still matches the spec and plan.
- If verification could not be run, state why.

## Report

Report:
- Mode used
- Tasks completed
- Files changed
- Verification result
- Any skipped tasks or blockers
- Suggested next command only when useful, usually `/spec-kit:implement next` or
  `/spec-kit:analyze`
