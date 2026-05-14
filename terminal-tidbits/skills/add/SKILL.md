---
name: add
description: Add a new terminal tidbit to your personal reference
argument-hint: <tid> <bit>
allowed-tools: Read, Write
disable-model-invocation: true
---

Add a new tidbit to the user's terminal reference collection.

## Arguments
$ARGUMENTS

The user provides:
- **tid**: A short identifier for the command/concept (e.g., `2>&1`, `grep -r`, `chmod 755`)
- **bit**: A detailed explanation in markdown format

Arguments may be provided as:
- Two separate arguments: `/terminal-tidbits:add "2>&1" "explanation here..."`
- A JSON object: `/terminal-tidbits:add {"tid": "2>&1", "bit": "explanation..."}`
- Natural language: "add a tidbit for the `xargs` command..."

## Storage

Resolve paths before reading or writing:
- `PLUGIN_ROOT`: `${CLAUDE_PLUGIN_ROOT}` in Claude Code. If unavailable, use the directory two levels above this `SKILL.md`.
- `TIDBITS_FILE`: `${TERMINAL_TIDBITS_FILE}` if set; otherwise `~/.terminal-tidbits/terminal-tidbits.json`.
- `DEFAULT_TIDBITS_FILE`: `${PLUGIN_ROOT}/data/default-terminal-tidbits.json`.

Tidbits are stored in `TIDBITS_FILE` with this structure:
```json
{
  "tidbits": [
    {"tid": "command", "bit": "explanation..."}
  ]
}
```

## Instructions

### Step 1: Parse the Input

Extract the `tid` and `bit` from $ARGUMENTS. If the user provided natural language, help them formulate both parts:
- Ask clarifying questions if the tid or bit is unclear
- Offer to write the bit if the user just names a command they want to learn about

### Step 2: Read Existing Tidbits

First, try to read the working tidbits file:
```
TIDBITS_FILE
```

If that file doesn't exist, read the defaults and use them as the starting point:
```
DEFAULT_TIDBITS_FILE
```

If neither file exists, start with an empty structure:
```json
{"tidbits": []}
```

### Step 3: Check for Duplicates

Check if a tidbit with the same `tid` already exists (case-sensitive match).

If duplicate found:
- Show the existing bit
- Ask if they want to replace it or keep both (with a modified tid)

### Step 4: Add the Tidbit

Append the new tidbit to the array and write the updated JSON to the working file:
```
TIDBITS_FILE
```
Create the parent directory first if it does not exist.

### Step 5: Confirm

Output a confirmation:

```
Added tidbit: `{tid}`

{bit preview - first 100 chars}...

You now have {N} tidbits. Use `/terminal-tidbits:show` to see all.
```
