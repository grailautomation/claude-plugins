---
description: Cross-artifact consistency check across spec, plan, and tasks
allowed-tools: [Read, Bash, Glob, Grep]
---

User input:

$ARGUMENTS

Perform a **read-only** cross-artifact consistency and quality analysis. Do NOT modify any files.

## Feature Detection

Run from the project root:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```
Parse JSON for `SPECS_DIR`. Derive:
- SPEC = `SPECS_DIR/spec.md`
- PLAN = `SPECS_DIR/plan.md`
- TASKS = `SPECS_DIR/tasks.md`

Abort with an error if any required file is missing, and instruct the user which command to run.

## Execution Flow

1. **Load all artifacts**:
   - `spec.md`: Overview, Functional Requirements, Non-Functional Requirements, User Stories, Edge Cases
   - `plan.md`: Architecture/stack, Data Model references, Phases, Technical constraints
   - `tasks.md`: Task IDs, descriptions, phase grouping, parallel markers `[P]`, file paths
   - `.specify/memory/constitution.md`: Principles and normative rules

2. **Build semantic models**:
   - Requirements inventory: each functional + non-functional requirement with a stable key
   - Task coverage mapping: map each task to one or more requirements
   - Constitution rule set: extract principle names and MUST/SHOULD statements

3. **Detection passes**:

   **A. Duplication**: Near-duplicate requirements across artifacts. Mark lower-quality phrasing for consolidation.

   **B. Ambiguity**: Vague adjectives ("fast", "scalable", "robust") lacking measurable criteria. Unresolved placeholders (TODO, ???, NEEDS CLARIFICATION).

   **C. Underspecification**: Requirements missing measurable outcomes. User stories without acceptance criteria alignment. Tasks referencing undefined components.

   **D. Constitution alignment**: Requirements or plan elements conflicting with MUST principles. Missing mandated quality gates. Constitution conflicts are automatically **CRITICAL**.

   **E. Coverage gaps**: Requirements with zero associated tasks. Tasks with no mapped requirement. Non-functional requirements not reflected in tasks.

   **F. Inconsistency**: Terminology drift (same concept named differently). Data entities in plan but absent in spec. Task ordering contradictions. Conflicting requirements.

4. **Severity assignment**:
   - **CRITICAL**: Constitution violation, missing core artifact, requirement with zero coverage blocking baseline functionality
   - **HIGH**: Duplicate/conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
   - **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
   - **LOW**: Style/wording improvements, minor redundancy

5. **Output the report** (do NOT write to any file):

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | ... | ... | ... | ... | ... |

### Coverage Summary
| Requirement Key | Has Task? | Task IDs | Notes |
|----------------|-----------|----------|-------|

### Constitution Alignment
[Issues or "All principles satisfied"]

### Metrics
- Total Requirements: N
- Total Tasks: N
- Coverage: N%
- Ambiguities: N
- Duplications: N
- Critical Issues: N
```

6. **Next actions**:
   - If CRITICAL issues: recommend resolving before `/spec-kit:implement`
   - If only LOW/MEDIUM: user may proceed with noted improvements
   - Provide specific command suggestions for remediation

7. Ask: "Would you like me to suggest concrete edits for the top issues?" (Do NOT apply them automatically.)

## Rules
- NEVER modify files — this is strictly read-only analysis
- Do not hallucinate missing sections — report them as findings
- Limit findings table to 50 rows; summarize overflow
- If zero issues found, emit a success report with coverage stats
