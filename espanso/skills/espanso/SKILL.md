---
name: espanso
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
description: >
  Espanso text expander configuration, match authoring, and workflow automation on macOS.
  Use when the user asks to: create or edit espanso matches/triggers, set up text snippets,
  configure dynamic expansions (date, shell, clipboard, forms), manage app-specific config,
  organize matches into packages, debug why a trigger isn't firing, or add new shortcuts to
  their espanso setup. Trigger phrases include "add an espanso snippet", "create a trigger for",
  "configure espanso", "text expander", "espanso match", or any request to expand or automate
  typed text on macOS.
---

# Espanso Skill

Espanso is a cross-platform text expander written in Rust. It intercepts keystrokes and
replaces trigger strings with defined expansions. Config is YAML-based.

## Safety Rules

- Treat Espanso config as user machine state. Read the current config before editing it.
- Resolve the config directory from `ESPANSO_CONFIG_DIR` when set; otherwise use the macOS default path.
- Show the exact YAML change or diff before editing live config.
- Back up the specific file you will edit before making changes.
- Ask for confirmation before any write, package install, restart, existing-trigger replacement, or shell/script expansion.
- Prefer focused edits to one match file instead of rewriting the full config tree.

## Config Locations (macOS)

| File | Purpose |
|------|----------|
| `$CONFIG/config/default.yml` | Global settings |
| `$CONFIG/match/base.yml` | Default matches (always active) |
| `$CONFIG/match/packages/` | Third-party packages |

`$CONFIG` = `${ESPANSO_CONFIG_DIR:-$HOME/Library/Application Support/espanso}`

Back up a match file before editing:

```bash
CONFIG="${ESPANSO_CONFIG_DIR:-$HOME/Library/Application Support/espanso}"
TARGET="$CONFIG/match/base.yml"
mkdir -p "$CONFIG/backups"
cp "$TARGET" "$CONFIG/backups/$(basename "$TARGET").$(date +%Y%m%d%H%M%S).bak"
```

## Core Concepts

- **Match**: a trigger + replacement rule
- **Trigger**: the string the user types (commonly prefixed with `:`)
- **Replace**: the output string
- **Variable**: dynamic value injected via `{{varname}}`
- **Extension**: the source of a variable (`date`, `shell`, `clipboard`, `form`, `random`, `script`)

## Static Matches

```yaml
matches:
  - trigger: ":sig"
    replace: "Best regards,\nYour Name"

  # word: true — only fires when surrounded by word separators
  - trigger: "teh"
    replace: "the"
    word: true

  # propagate_case — alh→although, Alh→Although, ALH→ALTHOUGH
  - trigger: "alh"
    replace: "although"
    propagate_case: true
    word: true

  # $|$ — cursor lands here after expansion
  - trigger: ":div"
    replace: "<div>$|$</div>"

  # Multiple triggers for one replacement
  - triggers: [":hello", ":hi"]
    replace: "Hello, World!"
```

## Dynamic Matches

See [references/extensions.md](references/extensions.md) for full extension reference.

```yaml
matches:
  # Date
  - trigger: ":today"
    replace: "{{date}}"
    vars:
      - name: date
        type: date
        params:
          format: "%Y-%m-%d"

  # Shell command
  - trigger: ":user"
    replace: "{{output}}"
    vars:
      - name: output
        type: shell
        params:
          cmd: "whoami"

  # Clipboard + form combined
  - trigger: ":mdlink"
    replace: "[{{form1.title}}]({{clipboard}})"
    vars:
      - name: clipboard
        type: clipboard
      - name: form1
        type: form
        params:
          layout: "Link title: [[title]]"
```

## Forms

Forms prompt the user with a popup before expanding.

```yaml
  - trigger: ":email"
    replace: "Hi {{form1.name}},\n\n{{form1.body}}\n\nBest,\nYour Name"
    vars:
      - name: form1
        type: form
        params:
          layout: |
            Name: [[name]]
            Body:
            [[body]]
          fields:
            body:
              multiline: true
```

## App-Specific Config

Create `$CONFIG/config/<appname>.yml` to override settings per app.

```yaml
# $CONFIG/config/vscode.yml
filter_title: "Visual Studio Code"
backend: clipboard   # clipboard backend recommended for Electron apps
```

Available filters: `filter_title`, `filter_class`, `filter_exec` (all support regex).

## CLI Commands

```bash
espanso status                   # check if espanso is running
espanso restart                  # restart after config changes
espanso edit                     # open base.yml in default editor
espanso match list               # list all active matches
espanso log                      # tail logs (debug trigger issues)
espanso package install <name>   # install from the Hub
espanso package list             # list installed packages
```

## Organizing Matches

All `.yml` files under `$CONFIG/match/` are loaded automatically — split by topic:

```
match/
  base.yml     # general snippets
  dev.yml      # code/dev snippets
  email.yml    # email templates
  dates.yml    # date/time expansions
```

## Workflow

1. Resolve `$CONFIG` and inspect the target match/config file
2. Back up the target file before editing
3. Edit one focused file under `$CONFIG/match/` when adding snippets
4. Restart Espanso after config changes under `$CONFIG/config/`
5. Use `espanso match list` to verify a trigger is registered
6. Use `espanso log` to debug unexpected behavior
