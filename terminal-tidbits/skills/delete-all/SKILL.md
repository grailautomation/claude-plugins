---
name: delete-all
description: Delete tidbits (defaults, custom, or all)
allowed-tools: Read, Write, Bash, AskUserQuestion
disable-model-invocation: true
---

Delete tidbits from the user's collection with options for what to delete.

## Storage

Resolve paths before reading or writing:
- `PLUGIN_ROOT`: `${CLAUDE_PLUGIN_ROOT}` in Claude Code. If unavailable, use the directory two levels above this `SKILL.md`.
- `TIDBITS_FILE`: `${TERMINAL_TIDBITS_FILE}` if set; otherwise `~/.terminal-tidbits/terminal-tidbits.json`.
- `DEFAULT_TIDBITS_FILE`: `${PLUGIN_ROOT}/data/default-terminal-tidbits.json`.

## Instructions

### Step 1: Read Current State

Read both files to understand what exists:

1. Read the defaults file:
   ```
   DEFAULT_TIDBITS_FILE
   ```

2. Read the working file (if it exists):
   ```
   TIDBITS_FILE
   ```

Determine:
- How many default tidbits exist (from default-terminal-tidbits.json)
- How many total tidbits the user currently has
- Which tidbits are "user-added" (in working file but not in defaults, matched by `tid`)

### Step 2: Show Current State

Before asking, display a summary so the user understands what they have:

```
You currently have {TOTAL} tidbits:
- {D} from the default set
- {C} that you added
```

If the user has modified or deleted some defaults, note that too.

### Step 3: Ask What to Delete

Use the **AskUserQuestion** tool to present deletion options. Use clear action verbs that explicitly state what will be REMOVED:

```json
{
  "questions": [{
    "question": "Which tidbits do you want to remove?",
    "header": "Remove",
    "options": [
      {
        "label": "My additions only",
        "description": "Removes the {C} tidbits you added; keeps the {D} defaults"
      },
      {
        "label": "Defaults only",
        "description": "Removes the {D} default tidbits; keeps your {C} additions"
      },
      {
        "label": "Everything",
        "description": "Removes all {TOTAL} tidbits; collection will be empty"
      },
      {
        "label": "Reset to original",
        "description": "Discards all changes; restores the {ORIG} original default tidbits"
      }
    ],
    "multiSelect": false
  }]
}
```

Replace placeholders with actual counts:
- `{TOTAL}` = total tidbits user currently has
- `{D}` = count of default tidbits still present
- `{C}` = count of user-added tidbits
- `{ORIG}` = count of tidbits in default-terminal-tidbits.json (always the same)

### Step 4: Execute Based on Choice

Before writing `TIDBITS_FILE`, create its parent directory if it does not exist.

**If "My additions only":**
- Filter the working file to keep only tidbits whose `tid` matches a default tidbit
- Write the filtered list to the working file
- Or simply delete the working file if all custom tidbits were removed

**If "Defaults only":**
- Filter the working file to keep only tidbits whose `tid` does NOT match any default tidbit
- Write the filtered list to the working file

**If "Everything":**
- Write an empty tidbits structure to the working file:
  ```json
  {"tidbits": []}
  ```

**If "Reset to original":**
- Delete the working file entirely (so commands will read from defaults)
- Use Bash to remove: `rm "$TIDBITS_FILE"`
- Or write the defaults content to the working file

### Step 5: Confirm

Report what was done:

```
Deleted {X} tidbits.

You now have {Y} tidbits. Use `/terminal-tidbits:show` to see them.
```

Or if everything was deleted:
```
All tidbits deleted. Your collection is now empty.

Use `/terminal-tidbits:add` to start fresh, or run `/terminal-tidbits:delete-all` and choose "Reset to original" to restore the defaults.
```
