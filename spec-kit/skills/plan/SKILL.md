---
name: plan
description: "Use when the user invokes $spec-kit:plan or /spec-kit:plan, or asks to generate a brownfield-aware implementation plan from the active feature spec."
argument-hint: "[tech stack preferences, constraints]"
allowed-tools: [Read, Write, Bash, Glob, Grep]
disable-model-invocation: true
---

# Spec Kit Plan

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

User input:

$ARGUMENTS

Generate an implementation plan from the active feature specification. Optimize
for an existing repository unless the user explicitly says this is greenfield.

## Preflight

Run from the project root:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```

Parse JSON for `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`,
`FEATURE_SOURCE`, and `PROJECT_CONTEXT`. All file paths must be absolute.

If `FEATURE_SOURCE` is `latest`, pause and state that the feature was inferred
from the latest spec directory. Continue only if the user confirms or if the
user explicitly set `SPECIFY_FEATURE`.

Read before planning:
- `FEATURE_SPEC`
- `.specify/memory/constitution.md`, if present
- `PROJECT_CONTEXT`, if present
- Repo docs/config that affect architecture, commands, or tests

## Brownfield Planning Rules

- Prefer existing project structure, dependencies, helper APIs, naming, and test
  style.
- Do not introduce a new framework, package manager, architectural layer, or
  top-level directory unless the plan explains why existing patterns are
  insufficient.
- Name the exact existing modules/directories the feature should fit into.
- If no analogous pattern exists, record the uncertainty and choose the smallest
  reversible implementation.
- Use user arguments for tech preferences only when they do not contradict repo
  reality or constitution constraints.

## Clarification Gate

Before writing the plan, inspect `FEATURE_SPEC` for `[NEEDS CLARIFICATION]`.
Pause only for material ambiguity: an answer that would change architecture,
data model, task split, tests, safety, UX, or operational behavior. For
non-material ambiguity, document the assumption in the plan and continue.

## Plan Artifact

Write `IMPL_PLAN` with this structure:

```markdown
# Implementation Plan: [FEATURE NAME]

**Branch**: `[BRANCH]` | **Date**: [today] | **Spec**: [relative path]
**Mode**: Brownfield unless explicitly greenfield

## Summary
[Primary requirement plus chosen implementation approach in 2-3 sentences]

## Repo Context
**Existing Area**: [module/package/app this fits]
**Relevant Patterns**: [existing files/classes/routes/tests to follow]
**Verification Commands**: [exact commands or "to confirm from repo docs"]

## Technical Context
**Language/Version**: [detected or provided]
**Primary Dependencies**: [existing deps preferred]
**Storage**: [if applicable]
**Testing**: [repo's actual test tools]
**Target Platform**: [detected]
**Constraints**: [performance, safety, auth, data, ops constraints]

## Constitution Compliance
[For each relevant principle, state compliance or documented deviation]

## Quality Gates
- [ ] Requirements are mapped to implementation areas
- [ ] Existing architecture and style are reused where practical
- [ ] Test/verification commands are identified
- [ ] Non-functional requirements have validation or explicit waiver
- [ ] Risky data migrations, destructive actions, or external calls are flagged
- [ ] Project context update is required or explicitly not needed

## Project Structure
[Concrete files/directories to create or modify. No generic option lists.]

## Phase 0: Research
- **Decision**: [what was chosen]
- **Rationale**: [why]
- **Alternatives considered**: [what else was evaluated]

## Phase 1: Design

### Data Model
[Entities/fields/relationships, only if applicable]

### Contracts / Interfaces
[APIs, CLI contracts, UI contracts, background jobs, schemas, or events]

### Validation Scenarios
[Integration/manual scenarios from acceptance criteria]

## Phase 2: Task Planning Approach
- Task categories: Setup, Tests, Core, Integration, Polish
- Test ordering: tests before or alongside implementation, as appropriate for this repo
- Parallel markers `[P]` only for independent files
- Estimated task count

## Complexity Tracking
| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

## Progress
- [ ] Phase 0: Research complete
- [ ] Phase 1: Design complete
- [ ] Phase 2: Task planning approach described
- [ ] Quality gates reviewed
```

## Supporting Artifacts

Generate only the artifacts that are useful for this feature:
- `research.md` for material technical decisions
- `data-model.md` when the feature changes persistent/domain data
- `contracts/` for API/CLI/schema/event contracts
- `quickstart.md` for integration or manual validation scenarios

Also refresh local-only `.specify/memory/project-context.md` by running the
detector when the plan discovers new stack, commands, or conventions not
captured there.

## Stop Rule

Do not generate `tasks.md`; `/spec-kit:tasks` owns that. Report:
- Plan path
- Generated artifacts
- Key repo-fit decision
- Verification commands/gaps
- Any documented deviations or risks
- Next workflow step: `/spec-kit:tasks`
