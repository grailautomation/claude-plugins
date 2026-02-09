---
description: Execute the task plan and build the feature
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

User input:

$ARGUMENTS

Execute the implementation plan by working through all tasks in `tasks.md`.

## Feature Detection

Run from the project root:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```
Parse JSON for `SPECS_DIR`. All paths must be absolute.

## Execution Flow

1. **Load implementation context** from `SPECS_DIR`:
   - **REQUIRED**: `tasks.md` — the complete task list. Abort if missing (suggest `/spec-kit:tasks`).
   - **REQUIRED**: `plan.md` — tech stack, architecture, file structure
   - **IF EXISTS**: `data-model.md` — entities and relationships
   - **IF EXISTS**: `contracts/` — API specifications and test requirements
   - **IF EXISTS**: `research.md` — technical decisions and constraints
   - **IF EXISTS**: `quickstart.md` — integration scenarios

2. **Parse tasks.md** and extract:
   - Task phases (Setup, Tests, Core, Integration, Polish)
   - Task dependencies and ordering
   - Task details: ID, description, file paths, parallel markers `[P]`

3. **Execute tasks phase by phase**:

   **Phase 1 — Setup**: Project structure, dependencies, configuration. Complete fully before moving on.

   **Phase 2 — Tests**: Write tests that fail. Follow TDD — these tests define the contract for implementation. Do not implement yet.

   **Phase 3 — Core**: Implement models, services, commands, endpoints to make tests pass. Respect dependencies (models before services, services before endpoints).

   **Phase 4 — Integration**: Database connections, middleware, logging, external services.

   **Phase 5 — Polish**: Additional unit tests, performance validation, documentation.

4. **Execution rules**:
   - Complete each phase before starting the next
   - Sequential tasks run in order
   - Parallel tasks `[P]` can be done in any order within their phase
   - Tasks affecting the same file must run sequentially regardless of `[P]` marker
   - Follow TDD: write tests first, verify they fail, then implement

5. **Progress tracking**:
   - After completing each task, mark it `[X]` in `tasks.md`:
     ```
     - [X] T001 Create project structure per implementation plan
     ```
   - Report progress after each completed task
   - If a task fails, halt and report the error with context
   - For parallel tasks, continue with successful ones and report failures

6. **Completion validation**:
   - Verify all tasks are marked `[X]`
   - Run tests to confirm they pass
   - Check that implemented features match the spec
   - Report final status with summary of completed work

7. **Report**:
   - Total tasks completed
   - Any tasks that were skipped or failed
   - Test results
   - Suggest running `/spec-kit:analyze` for a final consistency check
