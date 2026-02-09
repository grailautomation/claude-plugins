---
description: Generate an implementation plan from the feature spec
argument-hint: "[tech stack preferences, constraints]"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

User input:

$ARGUMENTS

Generate a complete implementation plan from the current feature's specification.

## Auto-Bootstrap / Feature Detection

Run from the project root:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```
Parse JSON for `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`. All file paths must be absolute.

If no feature is found, instruct the user to run `/spec-kit:specify` first.

## Execution Flow

1. **Pre-check**: Read `FEATURE_SPEC`. Look for a `## Clarifications` section with at least one session. If missing and the spec has `[NEEDS CLARIFICATION]` markers, PAUSE and suggest running `/spec-kit:clarify` first. Only continue if: (a) clarifications exist, (b) no ambiguity markers remain, or (c) user explicitly overrides.

2. **Read the feature spec** thoroughly:
   - Requirements and user stories
   - Functional and non-functional requirements
   - Success/acceptance criteria
   - Technical constraints or dependencies mentioned

3. **Read the constitution** at `.specify/memory/constitution.md` for alignment constraints.

4. **Incorporate user arguments**: tech stack preferences, constraints, or design decisions from `$ARGUMENTS`.

5. **Generate the implementation plan** — write `plan.md` to `SPECS_DIR` with this structure:

```markdown
# Implementation Plan: [FEATURE NAME]

**Branch**: `[BRANCH]` | **Date**: [today] | **Spec**: [relative path to spec.md]

## Summary
[Primary requirement + chosen technical approach in 2-3 sentences]

## Technical Context
**Language/Version**: [e.g., Python 3.12, TypeScript 5.x]
**Primary Dependencies**: [key frameworks/libraries]
**Storage**: [if applicable — database, file system, etc.]
**Testing**: [test framework and approach]
**Target Platform**: [e.g., Linux server, browser, CLI]
**Project Type**: [single/web/mobile]

## Constitution Compliance
[For each relevant constitution principle, note how this plan aligns. Flag any tensions.]

## Project Structure
[Concrete directory layout for this feature — NOT a template with options, but the actual chosen structure]

## Phase 0: Research
[For each unknown or technology choice:]
- **Decision**: [what was chosen]
- **Rationale**: [why]
- **Alternatives considered**: [what else was evaluated]

## Phase 1: Design

### Data Model
[Entities, fields, relationships, validation rules — write to `data-model.md`]

### API Contracts / Interfaces
[Endpoints, request/response shapes, error formats — write to `contracts/` directory]

### Integration Test Scenarios
[Key user journeys as test scenarios — write to `quickstart.md`]

## Phase 2: Task Planning Approach
[Describe how tasks will be generated — DO NOT create tasks.md here]
- Task categories: Setup, Tests, Core, Integration, Polish
- TDD ordering: tests before implementation
- Parallel markers [P] for independent work
- Estimated task count

## Complexity Tracking
[Only if constitution compliance required justified deviations]
| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

## Progress
- [ ] Phase 0: Research
- [ ] Phase 1: Design (data-model.md, contracts/, quickstart.md)
- [ ] Phase 2: Task planning approach described
- [ ] Constitution compliance verified
```

6. **Generate supporting artifacts** in `SPECS_DIR`:
   - `research.md` — technology decisions and rationale
   - `data-model.md` — entity definitions (if the feature involves data)
   - `contracts/` directory — API contracts or interface definitions (if applicable)
   - `quickstart.md` — key integration test scenarios

   Only generate artifacts that are relevant to the feature. A CLI tool doesn't need API contracts. A library doesn't need a data model. Use judgment.

7. **Constitution check**: Verify the plan doesn't violate any constitutional principles. Document any tensions in the Complexity Tracking section.

8. **STOP here** — do NOT generate tasks. That's the `/spec-kit:tasks` command.

9. **Report** to the user:
   - Branch and plan file path
   - Summary of technical choices
   - List of generated artifacts
   - Any constitution compliance notes
   - Suggest next step: "Run `/spec-kit:tasks` to generate the task breakdown"
