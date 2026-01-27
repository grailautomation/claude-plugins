---
description: Search your terminal tidbits
argument-hint: [search-term]
allowed-tools: Read
---

Search through tidbits and display matching results.

## Arguments
$ARGUMENTS

The user optionally provides a search term. If no search term is provided, display all tidbits (same as `/terminal-tidbits:show`).

## Storage

Tidbits are stored in `${CLAUDE_PLUGIN_ROOT}/data/terminal-tidbits.json`.

## Instructions

### Step 1: Parse Search Term

Extract the search term from $ARGUMENTS.

If $ARGUMENTS is empty or not provided, display all tidbits using the same format as the show command.

### Step 2: Read Tidbits

First, try to read the working tidbits file:
```
${CLAUDE_PLUGIN_ROOT}/data/terminal-tidbits.json
```

If that file doesn't exist, read the defaults:
```
${CLAUDE_PLUGIN_ROOT}/data/default-terminal-tidbits.json
```

If neither file exists, inform the user:
```
No tidbits yet! Use `/terminal-tidbits:add` to start building your reference.
```

### Step 3: Search

Perform a case-insensitive search across both `tid` and `bit` fields. A tidbit matches if the search term appears anywhere in either field.

This is a simple substring match (like Ctrl+F / Cmd+F in a browser).

### Step 4: Display Results

If matches found, display using full detail format:

```markdown
# Search Results for "{search-term}" ({N} matches)

---

## `{tid}`

{bit}

---

(etc.)
```

If no matches found:
```
No tidbits matching "{search-term}".

You have {N} total tidbits. Try `/terminal-tidbits:show` to see all, or try a different search term.
```

### Display Guidelines

- Show the `tid` as a level-2 heading with backticks
- Show the full `bit` content
- Separate each tidbit with a horizontal rule
- Order matches alphabetically by `tid`
- Highlight or emphasize where the search term appears (if practical)
