---
name: analyze
description: "Use when the user invokes $spec-kit:analyze or /spec-kit:analyze, or asks to run read-only consistency analysis across spec, plan, tasks, and repo context."
allowed-tools: [Read, Bash, Glob, Grep]
disable-model-invocation: true
---

# Spec Kit Analyze

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

User input:

$ARGUMENTS

Perform a read-only cross-artifact consistency and quality analysis. Do not
modify files, do not mark tasks complete, and do not fix findings during this
command.

## Feature Detection

Run from the project root:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh" --no-context
```

Parse JSON for `SPECS_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, `FEATURE_SOURCE`, and
`PROJECT_CONTEXT`. Derive:
- SPEC = `SPECS_DIR/spec.md`
- PLAN = `SPECS_DIR/plan.md`
- TASKS = `SPECS_DIR/tasks.md`

Abort with a clear message if `spec.md`, `plan.md`, or `tasks.md` is missing.

## Inputs

Load:
- `spec.md`
- `plan.md`
- `tasks.md`
- `.specify/memory/constitution.md`, if present
- `.specify/memory/project-context.md`, if present

## Detection Passes

Build deterministic inventories:
- Requirements: each FR/NFR with a stable slug
- Acceptance scenarios and edge cases
- Tasks: task ID, phase, description, file paths, `[P]` marker
- Constitution rules: principle names and MUST/SHOULD statements
- Verification commands and quality gates

Then check:
- Duplication: near-duplicate requirements or tasks
- Ambiguity: vague words, unresolved placeholders, unclear success criteria
- Underspecification: missing files, missing outcomes, missing validation
- Brownfield fit: plan/tasks ignore existing repo structure or commands
- Constitution alignment: conflicts with MUST/SHOULD principles
- Coverage gaps: requirements/scenarios without tasks, tasks without source need
- Safety gaps: migrations/destructive/external/credential work lacks guardrails
- Parallelism issues: `[P]` tasks touch same file or hidden dependency
- Verification gaps: no test/build/lint/smoke command or explicit waiver

## Severity

- CRITICAL: constitution MUST conflict, missing core artifact, unsafe operation
  without confirmation, or baseline requirement with zero coverage
- HIGH: conflicting requirements, untestable acceptance criterion, ignored repo
  architecture, ambiguous security/privacy/performance behavior
- MEDIUM: missing non-functional coverage, terminology drift, weak task path,
  verification gap with reasonable workaround
- LOW: wording cleanup, minor redundancy, optional polish

## Report Format

Emit Markdown only:

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | ... | ... | spec.md:12 | ... | ... |

### Coverage Summary
| Requirement Key | Has Task? | Task IDs | Notes |
|----------------|-----------|----------|-------|

### Unmapped Tasks
[task IDs or "None"]

### Constitution Alignment
[issues or "No conflicts detected"]

### Brownfield Fit
[issues or "Plan and tasks follow detected repo context"]

### Metrics
- Total Requirements: N
- Total Tasks: N
- Coverage: N%
- Ambiguities: N
- Duplications: N
- Critical Issues: N
```

Use stable IDs by category prefix and sorted location order so reruns without
file changes produce consistent IDs.

## Finish

If CRITICAL or HIGH issues exist, recommend resolving before implementation. If
only LOW/MEDIUM issues exist, say whether `/spec-kit:implement next` is
reasonable. Ask whether the user wants concrete remediation edits; do not apply
them in this command.
