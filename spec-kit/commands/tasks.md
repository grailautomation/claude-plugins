---
description: Generate a dependency-ordered task breakdown from the implementation plan
argument-hint: "[additional context]"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

User input:

$ARGUMENTS

Generate an actionable, dependency-ordered task breakdown for the current feature.

## Feature Detection

Run from the project root:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```
Parse JSON for `SPECS_DIR` and `FEATURE_SPEC`. All paths must be absolute.

## Execution Flow

1. **Load design documents** from `SPECS_DIR`:
   - **REQUIRED**: `plan.md` — tech stack, architecture, file structure. Abort if missing.
   - **IF EXISTS**: `data-model.md` — entities and relationships
   - **IF EXISTS**: `contracts/` — API specifications
   - **IF EXISTS**: `research.md` — technical decisions
   - **IF EXISTS**: `quickstart.md` — test scenarios

   Not all projects have all documents. Generate tasks based on what's available.

2. **Generate tasks** organized by phase:

```markdown
# Tasks: [FEATURE NAME]

**Plan**: [relative path to plan.md]
**Generated**: [today's date]

## Phase 1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize project with dependencies
- [ ] T003 [P] Configure linting and formatting

## Phase 2: Tests First (TDD)
**CRITICAL: These tests MUST be written and MUST FAIL before any implementation**
- [ ] T004 [P] [Contract/unit test description] in [exact file path]
- [ ] T005 [P] [Integration test description] in [exact file path]
(one task per contract, one per integration scenario)

## Phase 3: Core Implementation
(ONLY after tests are failing)
- [ ] T006 [P] [Model/entity] in [exact file path]
- [ ] T007 [P] [Service/logic] in [exact file path]
- [ ] T008 [Endpoint/command] in [exact file path]
(one per entity, service, endpoint — parallel only if different files)

## Phase 4: Integration
- [ ] T009 [Database/service connections]
- [ ] T010 [Middleware, logging, auth]

## Phase 5: Polish
- [ ] T011 [P] Additional unit tests in [path]
- [ ] T012 Performance validation
- [ ] T013 [P] Update documentation

## Dependencies
- Tests (Phase 2) before implementation (Phase 3)
- [specific dependency notes: T006 blocks T007, etc.]

## Parallel Execution Guide
Tasks marked [P] within the same phase can run concurrently.
Sequential tasks (no [P]) must complete before the next starts.
Tasks in different phases are NOT parallel — complete each phase first.
```

3. **Task generation rules**:
   - Each contract file → contract test task `[P]`
   - Each entity in data model → model creation task `[P]`
   - Each endpoint → implementation task (not parallel if shared files)
   - Each user story → integration test `[P]`
   - Different files = can be parallel `[P]`
   - Same file = sequential (no `[P]`)

4. **Ordering**:
   - Setup before everything
   - Tests before implementation (TDD)
   - Models before services
   - Services before endpoints
   - Core before integration
   - Everything before polish

5. **Each task must specify**:
   - Exact file path where work happens
   - What to create/modify
   - Enough detail that an LLM can complete it without extra context

6. **Write** to `SPECS_DIR/tasks.md`.

7. **Report** to the user:
   - Path to tasks file
   - Total task count
   - Breakdown by phase
   - Number of parallel-eligible tasks
   - Suggest next step: "Run `/spec-kit:analyze` for consistency check, or `/spec-kit:implement` to start building"
