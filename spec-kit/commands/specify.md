---
description: Create a feature specification from a natural language description
argument-hint: "<feature description>"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

The text after `/spec-kit:specify` IS the feature description. Do not ask the user to repeat it.

User input:

$ARGUMENTS

If the user input is empty, respond with an error: "Please provide a feature description. Example: `/spec-kit:specify build a REST API for managing photo albums`"

## Auto-Bootstrap

Ensure `.specify/specs/` and `.specify/memory/` directories exist. Create them if missing.

## Execution Flow

1. **Create feature branch and directory** by running this script from the project root:
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/create-feature.sh" $ARGUMENTS
   ```
   Parse the JSON output for `BRANCH_NAME`, `SPEC_FILE`, `FEATURE_NUM`, and `FEATURE_DIR`. All subsequent file paths must be absolute.

   **IMPORTANT**: Run this script exactly once. Parse the JSON from its output.

2. **Load the constitution** at `.specify/memory/constitution.md` if it exists. Note any principles that constrain the spec (architecture rules, testing requirements, tech constraints).

3. **Analyze the feature description** and extract:
   - Actors (who uses this)
   - Actions (what they do)
   - Data (what's involved)
   - Constraints (any mentioned limits)

4. **Write the specification** to `SPEC_FILE` using this structure:

```markdown
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[BRANCH_NAME from script]`
**Created**: [today's date]
**Status**: Draft

## Overview
[1-2 paragraph summary of what this feature does and why it matters, derived from the user's description]

## User Scenarios & Acceptance Criteria

### Primary User Story
[Main user journey in plain language]

### Acceptance Scenarios
1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]
(add more as appropriate)

### Edge Cases
- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Functional Requirements
- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
(continue as needed — each requirement must be testable)

Mark anything unclear with `[NEEDS CLARIFICATION: specific question]`

### Key Entities
(include if the feature involves data)
- **[Entity]**: [What it represents, key attributes, relationships]

## Review Checklist
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
```

5. **Spec quality rules**:
   - Focus on WHAT and WHY, never HOW (no tech stack, no code structure)
   - Every requirement must be testable — if you can't write a test for it, rewrite it
   - Mark ALL assumptions with `[NEEDS CLARIFICATION: specific question]` — don't guess
   - Common underspecified areas to flag: user permissions, data retention, performance targets, error handling, integrations

6. **Report** to the user:
   - Branch name and spec file path
   - Count of requirements generated
   - Count of `[NEEDS CLARIFICATION]` markers (if any)
   - Suggest next step: "Run `/spec-kit:clarify` to resolve ambiguities" (if markers exist) or "Run `/spec-kit:plan` to create the implementation plan"
