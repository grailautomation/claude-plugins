---
name: rm
description: Remove a tidbit from your terminal reference
argument-hint: <tid>
allowed-tools: Read, Write
disable-model-invocation: true
---

Remove a tidbit from the user's terminal reference collection.

## Arguments
$ARGUMENTS

The user provides the `tid` (identifier) of the tidbit to remove.

## Storage

Resolve paths before reading or writing:
- `PLUGIN_ROOT`: `${CLAUDE_PLUGIN_ROOT}` in Claude Code. If unavailable, use the directory two levels above this `SKILL.md`.
- `TIDBITS_FILE`: `${TERMINAL_TIDBITS_FILE}` if set; otherwise `~/.terminal-tidbits/terminal-tidbits.json`.
- `DEFAULT_TIDBITS_FILE`: `${PLUGIN_ROOT}/data/default-terminal-tidbits.json`.

## Instructions

### Step 1: Parse the Input

Extract the `tid` from $ARGUMENTS. The tid is the short identifier (e.g., `2>&1`, `grep -r`).

### Step 2: Read Existing Tidbits

First, try to read the working tidbits file:
```
TIDBITS_FILE
```

If that file doesn't exist, read the defaults:
```
DEFAULT_TIDBITS_FILE
```

If neither file exists, inform the user they have no tidbits yet.

### Step 3: Find the Tidbit

Search for a tidbit with a matching `tid` (case-sensitive).

If not found:
- List similar tids that might be what they meant (fuzzy match on tid or bit content)
- Ask for clarification

### Step 4: Confirm Deletion

Show the tidbit that will be deleted:
```
About to remove:

**`{tid}`**
{first 200 chars of bit}...

Proceed? (y/n)
```

Wait for user confirmation before proceeding.

### Step 5: Remove and Save

Remove the tidbit from the array and write the updated JSON to the working file:
```
TIDBITS_FILE
```
Create the parent directory first if it does not exist.

### Step 6: Confirm

Output a confirmation:
```
Removed tidbit: `{tid}`

You now have {N} tidbits remaining.
```
