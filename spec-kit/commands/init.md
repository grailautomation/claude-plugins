---
description: Bootstrap .specify/ directory structure for spec-driven development
allowed-tools: [Bash, Read, Write]
---

Initialize the `.specify/` directory structure in the current project for spec-driven development.

## Steps

1. Check if `.specify/` already exists in the current working directory. If it does, report what's already there and skip creation of existing items.

2. Create the following directory structure:
   ```
   .specify/
   ├── memory/
   │   └── constitution.md    (empty placeholder)
   └── specs/                 (empty, features go here)
   ```

3. If `.specify/memory/constitution.md` does not exist, create it with this placeholder content:

   ```markdown
   # Project Constitution

   > Run `/spec-kit:constitution` to generate your project's development principles.

   **Version**: 0.0.0 | **Ratified**: — | **Last Amended**: —
   ```

4. If the current directory is not a git repository, initialize one with `git init`.

5. Report what was created:
   - List each directory/file created (or note if already existed)
   - Suggest next step: "Run `/spec-kit:constitution <context>` to establish your project's development principles."
