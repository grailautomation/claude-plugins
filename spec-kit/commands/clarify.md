---
description: Interactively clarify ambiguities in the current feature spec
allowed-tools: [Read, Write, Bash, Glob]
---

User input:

$ARGUMENTS

Goal: Detect and reduce ambiguity in the active feature specification through up to 5 targeted clarification questions, recording answers directly in the spec.

This clarification workflow should run BEFORE `/spec-kit:plan`. If the user explicitly says they're skipping clarification, warn that downstream rework risk increases but allow it.

## Auto-Bootstrap / Feature Detection

Detect the current feature by running:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```
Parse JSON for `FEATURE_SPEC` and `SPECS_DIR`. If no feature is found, instruct the user to run `/spec-kit:specify` first.

## Execution Flow

1. **Load the spec** from `FEATURE_SPEC`. If it doesn't exist, tell the user to run `/spec-kit:specify` first.

2. **Structured ambiguity scan** — analyze the spec against this taxonomy. For each category, assess: Clear / Partial / Missing.

   - **Functional Scope**: Core user goals, success criteria, explicit out-of-scope declarations
   - **Domain & Data Model**: Entities, attributes, relationships, identity rules, state transitions
   - **Interaction & UX Flow**: Critical user journeys, error/empty/loading states
   - **Non-Functional Attributes**: Performance targets, scalability, reliability, observability
   - **Integration & Dependencies**: External services, data formats, failure modes
   - **Edge Cases & Failure Handling**: Negative scenarios, rate limiting, conflict resolution
   - **Constraints & Tradeoffs**: Technical constraints, explicitly rejected alternatives
   - **Terminology**: Canonical terms, avoided synonyms

3. **Generate up to 5 clarification questions** (internally). Prioritize by `Impact x Uncertainty`. Each question must be:
   - Answerable with a short multiple-choice selection (2-5 options) OR a short phrase (<=5 words)
   - Material to architecture, data modeling, task decomposition, test design, or UX
   - Not already answered in the spec

4. **Ask questions ONE AT A TIME** (interactive loop):
   - Present one question with options as a markdown table:

     | Option | Description |
     |--------|-------------|
     | A | ... |
     | B | ... |
     | Short | Provide a different short answer (<=5 words) |

   - After user answers, validate and record it
   - Move to next question
   - Stop when: all critical ambiguities resolved, user says "done"/"stop"/"proceed", or 5 questions asked
   - Never reveal future questions in advance

5. **After EACH accepted answer**, update the spec file:
   - Ensure a `## Clarifications` section exists (create after the Overview if missing)
   - Under it, add/use a `### Session [today's date]` subheading
   - Append: `- Q: <question> → A: <answer>`
   - Apply the clarification to the most relevant spec section:
     * Functional answers → update Functional Requirements
     * Data answers → update Key Entities
     * Non-functional answers → add measurable criteria
     * Edge cases → add to Edge Cases section
   - If the answer invalidates an earlier vague statement, replace it (don't duplicate)
   - Save the file after each integration

6. **Report completion**:
   - Number of questions asked & answered
   - Path to updated spec
   - Sections modified
   - Coverage summary: which categories are Resolved, Deferred (beyond quota), Clear, or Outstanding
   - If outstanding items remain, recommend whether to proceed to `/spec-kit:plan` or run `/spec-kit:clarify` again
   - Suggest next step

## Rules
- Never exceed 5 questions total
- If no meaningful ambiguities found, say so and suggest proceeding
- If spec is missing, instruct user to run `/spec-kit:specify`
- Respect early termination signals ("stop", "done", "proceed")
