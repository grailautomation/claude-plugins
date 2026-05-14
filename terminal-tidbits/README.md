# Terminal Tidbits

A personal reference system for terminal commands and concepts you're learning. Store explanations for commands, syntax, and shell concepts in a searchable collection.

**Ships with 10 pre-populated tidbits** covering common terminal concepts like `2>&1`, `xargs`, `grep`, `chmod`, and more.

## Commands

| Command | Description |
|---------|-------------|
| `/terminal-tidbits:add` | Add a new tidbit |
| `/terminal-tidbits:rm` | Remove a tidbit |
| `/terminal-tidbits:show` | Display all tidbits |
| `/terminal-tidbits:search` | Search tidbits |
| `/terminal-tidbits:delete-all` | Clear all tidbits (or reset to defaults) |

In Codex, invoke the same workflows as skills, for example
`$terminal-tidbits:add`, `$terminal-tidbits:search`, or
`$terminal-tidbits:show`.

## Usage Examples

### Show all tidbits

```
/terminal-tidbits:show
```

### Search tidbits

```
/terminal-tidbits:search stderr
/terminal-tidbits:search redirect
```

### Add a tidbit

```
/terminal-tidbits:add "2>&1" "Redirects stderr to stdout..."
```

Or use natural language:
```
/terminal-tidbits:add
> What's the tidbit for? xargs
> Claude will help you write the explanation
```

### Remove a tidbit

```
/terminal-tidbits:rm "2>&1"
```

### Reset to defaults

```
/terminal-tidbits:delete-all --reset-to-defaults
```

## Data Storage

Default tidbits are shipped with the plugin, while user-added tidbits are stored
outside the plugin directory so updates do not overwrite personal data:

- **Default tidbits**: `data/default-terminal-tidbits.json` (ships with plugin)
- **Your tidbits**: `~/.terminal-tidbits/terminal-tidbits.json` by default
- **Override path**: set `TERMINAL_TIDBITS_FILE` when you want a different file

The working file lives outside the installed plugin/cache so custom tidbits
survive plugin updates and work in both Claude Code and Codex.

## Pre-populated Tidbits

The plugin ships with explanations for:

- `2>&1` - Redirecting stderr to stdout
- `set -euo pipefail` - Bash strict mode
- `xargs` - Building commands from stdin
- `&&` - Chaining commands
- `chmod` - File permissions
- `$?` - Exit status variable
- `curl` - HTTP requests
- `grep` - Text searching
- `/dev/null` - Discarding output
- `!!` - History expansion

## Installation

Add to your Claude Code plugins or install from the plugin marketplace.
