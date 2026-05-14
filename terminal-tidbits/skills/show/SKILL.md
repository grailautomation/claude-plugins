---
name: show
description: Display all your terminal tidbits
allowed-tools: Read
disable-model-invocation: true
---

Display all tidbits in the user's terminal reference collection.

## Storage

Resolve paths before reading:
- `PLUGIN_ROOT`: `${CLAUDE_PLUGIN_ROOT}` in Claude Code. If unavailable, use the directory two levels above this `SKILL.md`.
- `TIDBITS_FILE`: `${TERMINAL_TIDBITS_FILE}` if set; otherwise `~/.terminal-tidbits/terminal-tidbits.json`.
- `DEFAULT_TIDBITS_FILE`: `${PLUGIN_ROOT}/data/default-terminal-tidbits.json`.

## Instructions

### Step 1: Read Tidbits

First, try to read the working tidbits file:
```
TIDBITS_FILE
```

If that file doesn't exist, read the defaults:
```
DEFAULT_TIDBITS_FILE
```

If neither file exists, inform the user:
```
No tidbits yet! Use `/terminal-tidbits:add` to start building your reference.
```

### Step 2: Format and Display

Display each tidbit with full detail, using this format:

```markdown
# Terminal Tidbits ({N} total)

---

## `{tid}`

{bit}

---

## `{tid2}`

{bit2}

---

(etc.)
```

### Display Guidelines

- Show the `tid` as a level-2 heading with backticks (code formatting)
- Show the full `bit` content (it may contain markdown formatting - render it properly)
- Separate each tidbit with a horizontal rule (`---`)
- Include a count in the main heading
- Order tidbits alphabetically by `tid` for easy scanning
