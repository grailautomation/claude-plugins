---
name: init
description: "Use when the user invokes $spec-kit:init or /spec-kit:init, or asks to bootstrap .specify/ for streamlined spec-driven development."
allowed-tools: [Bash, Read, Write]
disable-model-invocation: true
---

# Spec Kit Init

This is a user-invoked Spec Kit workflow. Treat user text after the invocation as the workflow input.

## Plugin Root

Use the spec-kit plugin root when running bundled scripts. In Claude Code, `${CLAUDE_PLUGIN_ROOT}` resolves to this plugin root. If that variable is unavailable, resolve the plugin root as the directory two levels above this `SKILL.md`.

Initialize `.specify/` in the current project for streamlined, brownfield-aware
spec-driven development.

## Steps

1. Inspect the current directory:
   - Is it a git repo?
   - Is the worktree dirty?
   - Which package/tooling files and repo guidance files exist?

2. Create missing directories only:
   ```text
   .specify/
   ├── memory/
   │   ├── constitution.md
   │   └── project-context.md  # local-only, gitignored
   └── specs/
   ```

3. If `.specify/memory/constitution.md` does not exist, create this placeholder:
   ```markdown
   # Project Constitution

   > Run `/spec-kit:constitution` to generate pragmatic project guardrails.

   **Version**: 0.0.0 | **Ratified**: TODO | **Last Amended**: TODO
   ```

4. Create or refresh local-only `.specify/memory/project-context.md` by running
   the bundled detector when available. The detector should also add the path to
   `.gitignore` in git repositories:
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect-project-context.sh" --write
   ```
   If unavailable, write a minimal context file manually from the inspection and
   add `.specify/memory/project-context.md` to `.gitignore`.

5. Do not run `git init` unless the user explicitly asked for it. If this is not
   a git repo, report that branch-based feature detection will require
   `SPECIFY_FEATURE` or explicit feature selection.

6. Report:
   - Files/directories created or already present
   - Detected stack/tooling summary
   - Whether git was left unchanged
   - Next step: `/spec-kit:constitution <project context>`
