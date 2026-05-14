---
name: staff-plan-review
description: Review implementation plans as a staff software engineer. Use when the user asks for staff engineer feedback, senior engineering review, plan review, architecture review, implementation-plan critique, approval before proceeding, risk review, or feedback on a proposed technical plan.
---

# Staff Plan Review

Review the supplied implementation plan. Stay in review mode: do not implement the plan or rewrite it unless the user explicitly asks for replacement text.

## Review Stance

- Prioritize correctness, architecture, maintainability, migration safety, operational risk, and validation quality.
- Ground feedback in the actual repo or provided plan. If the plan references files or behavior and the repo is available, inspect the relevant files before making strong claims.
- Calibrate to a solo indie project: favor practical safeguards over enterprise ceremony.
- Challenge vague ownership, missing rollback paths, unclear data migration behavior, test gaps, or assumptions that are not validated by evidence.
- Prefer concrete fixes over generic advice.

## Output Shape

Start with one of these verdicts:

- `Approved` — no blocking issues; only optional improvements.
- `Approved With Notes` — plan is safe enough to proceed, but has non-blocking improvements.
- `Needs Changes` — one or more issues should be fixed before implementation.

Then provide the highest-signal sections needed:

- `Blocking Issues`: correctness or risk problems that should stop implementation.
- `Important Notes`: non-blocking gaps, tradeoffs, or validation improvements.
- `Suggested Edits`: concise replacement bullets or plan changes when useful.
- `Residual Risk`: what remains uncertain after the review.

Keep the review concise. Do not invent concerns just to fill sections; omit empty sections.

## Review Checklist

Check whether the plan:

- Names the actual files, modules, commands, and data surfaces involved.
- Fits existing architecture and local conventions.
- Separates cleanup, migration, and new feature work when that lowers risk.
- Preserves user data, credentials, local state, and unrelated worktree changes.
- Defines validation that matches the blast radius.
- Has clear stop conditions for risky or irreversible actions.
- Avoids depending on outdated docs, unstated environment assumptions, or unavailable tools.

If the plan is underspecified, ask for the missing input only when it blocks a useful review. Otherwise state assumptions and proceed.
