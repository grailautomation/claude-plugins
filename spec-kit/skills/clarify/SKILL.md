---
name: clarify
description: "Use when the user invokes $spec-kit:clarify or /spec-kit:clarify, or asks to clarify only material ambiguities in the active feature spec."
allowed-tools: [Read, Write, Bash, Glob]
disable-model-invocation: true
---

# Spec Kit Clarify

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

User input:

$ARGUMENTS

Goal: reduce ambiguity in the active spec by asking up to five targeted
questions and recording the answers directly in the spec.

## Feature Detection

Run from the project root:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-plan.sh"
```

Parse JSON for `FEATURE_SPEC`, `SPECS_DIR`, `FEATURE_SOURCE`, and
`PROJECT_CONTEXT`. If no feature is found, instruct the user to run
`/spec-kit:specify` or set `SPECIFY_FEATURE`.

## Materiality Rule

Ask a question only if the answer would materially change at least one of:
- Architecture or repo integration approach
- Data model, schema, permissions, or lifecycle rules
- Task decomposition or file ownership
- Test strategy or acceptance criteria
- Safety, privacy, destructive operations, or external service behavior
- UX flow, accessibility, error states, or operational readiness

Do not ask about stylistic preferences, low-impact wording, or plan-level
details that can be documented as assumptions.

## Ambiguity Scan

Assess each category as Clear, Partial, Missing, or Deferred:
- Functional scope and explicit out-of-scope behavior
- Domain/data entities, identity, relationships, lifecycle
- User flows, empty/error/loading states, accessibility/localization
- Performance, reliability, observability, security, privacy, compliance
- External integrations, protocols, imports/exports, failure modes
- Edge cases, conflicts, rate limits, destructive actions
- Existing repo constraints and tradeoffs
- Terminology consistency

Generate at most five candidate questions ordered by impact times uncertainty.

## Interactive Loop

Ask exactly one question at a time.

For multiple choice:

| Option | Description |
|--------|-------------|
| A | ... |
| B | ... |
| Short | Provide a different short answer (<=5 words) |

For short answer:
`Format: Short answer (<=5 words)`

Validate the answer. If ambiguous, ask one quick disambiguation for the same
question. Stop when the user says stop/proceed/done, all material ambiguity is
resolved, or five questions have accepted answers.

## Spec Updates

After each accepted answer:
1. Ensure `## Clarifications` exists after the overview or nearest contextual
   section.
2. Ensure `### Session YYYY-MM-DD` exists for today.
3. Append `- Q: <question> -> A: <answer>`.
4. Apply the clarification to the relevant section:
   - Functional answer -> Functional Requirements
   - Data answer -> Key Entities or data section
   - Non-functional answer -> Non-Functional Requirements
   - Edge case -> Edge Cases
   - Terminology -> normalize terms across touched sections
   - Repo constraint -> Scope or Repo Fit
5. Replace contradictory older text instead of duplicating it.
6. Save the file after each accepted answer.

## Completion Report

Report:
- Number of questions asked and answered
- Path to updated spec
- Sections modified
- Coverage summary with Clear, Resolved, Deferred, and Outstanding categories
- Whether to proceed to `/spec-kit:plan` or run clarification again later
