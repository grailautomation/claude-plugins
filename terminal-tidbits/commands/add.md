---
description: Add a new terminal tidbit to your personal reference
argument-hint: <tid> <bit>
allowed-tools: Read, Write
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

Tidbits are stored in `${CLAUDE_PLUGIN_ROOT}/data/terminal-tidbits.json` with this structure:
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
${CLAUDE_PLUGIN_ROOT}/data/terminal-tidbits.json
```

If that file doesn't exist, read the defaults and use them as the starting point:
```
${CLAUDE_PLUGIN_ROOT}/data/default-terminal-tidbits.json
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
${CLAUDE_PLUGIN_ROOT}/data/terminal-tidbits.json
```

### Step 5: Confirm

Output a confirmation:

```
Added tidbit: `{tid}`

{bit preview - first 100 chars}...

You now have {N} tidbits. Use `/terminal-tidbits:show` to see all.
```
