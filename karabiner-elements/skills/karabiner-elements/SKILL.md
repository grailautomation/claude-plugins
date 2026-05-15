---
name: karabiner-elements
version: 0.1.0
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
description: >-
  This skill should be used when the user asks to "remap keys", "set up a
  hyper key", "create Karabiner rules", "configure keyboard shortcuts",
  "create complex modifications", "set up dual-function keys", "configure
  app-specific shortcuts", or any Karabiner-Elements setup and troubleshooting
  on macOS.
---

# Karabiner-Elements Configuration Agent

Configure, customize, and troubleshoot Karabiner-Elements on macOS — including key remapping, complex modifications, profiles, and device-specific rules.

## Safety Rules

- Treat Karabiner configuration as user machine state. Read the current config before editing it.
- Resolve paths from environment variables when set; otherwise use Karabiner's macOS defaults.
- Show the exact JSON change or diff before editing live config.
- Back up `karabiner.json` before any write.
- Ask for confirmation before any write, profile selection, variable change, service restart, or other live behavior change.
- Prefer adding focused complex modification files over rewriting unrelated profile data.
- Lint complex modifications with `karabiner_cli` when the CLI is available.
- Do not run uninstall, root-owned environment-file edits, or other destructive maintenance commands unless the user explicitly asks for that action.

## Important Paths

```
CONFIG_FILE: ${KARABINER_CONFIG_FILE:-$HOME/.config/karabiner/karabiner.json}
COMPLEX_MODS_DIR: ${KARABINER_COMPLEX_MODS_DIR:-$HOME/.config/karabiner/assets/complex_modifications}
CLI_PATH: ${KARABINER_CLI_PATH:-/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli}
DEVICES_FILE: ${KARABINER_DEVICES_FILE:-$HOME/.local/share/karabiner/karabiner_grabber_devices.json}
LOG_DIR: /var/log/karabiner/
```

## Configuration Structure

The main `karabiner.json` structure:

```json
{
    "global": { "check_for_updates_on_startup": true, "show_in_menu_bar": true },
    "profiles": [
        {
            "name": "Default",
            "selected": true,
            "simple_modifications": [],
            "fn_function_keys": [],
            "complex_modifications": { "parameters": {}, "rules": [] },
            "virtual_hid_keyboard": { "keyboard_type": "ansi" },
            "devices": [],
            "parameters": {}
        }
    ]
}
```

## CLI Commands Reference

```bash
# Profile management
"$CLI_PATH" --list-profile-names
"$CLI_PATH" --show-current-profile-name
"$CLI_PATH" --select-profile 'Profile Name'  # confirm before running

# Variable management
"$CLI_PATH" --set-variables '{"my_var":1, "another_var":true}'  # confirm before running

# Configuration validation
"$CLI_PATH" --lint-complex-modifications "$COMPLEX_MODS_DIR"/*.json

# Version and help
"$CLI_PATH" --version
"$CLI_PATH" --help
```

## Environment Inspection

Before making changes, gather context about the installation, current config, connected devices, and active profile. Use the inspection script at [scripts/inspect_environment.sh](scripts/inspect_environment.sh) to automate this.

## Complex Modifications Structure

Each complex modification rule follows this pattern:

```json
{
    "description": "Human-readable description",
    "manipulators": [
        {
            "type": "basic",
            "from": {
                "key_code": "source_key",
                "modifiers": { "mandatory": ["modifier1"], "optional": ["any"] }
            },
            "to": [{ "key_code": "target_key", "modifiers": ["modifier"] }],
            "to_if_alone": [],
            "to_if_held_down": [],
            "to_after_key_up": [],
            "to_delayed_action": {
                "to_if_invoked": [],
                "to_if_canceled": []
            },
            "conditions": [],
            "parameters": {}
        }
    ]
}
```

## Reference Documentation

- **Key Codes** — [references/key-codes.md](references/key-codes.md) — Letters, numbers, F-keys, modifiers, navigation, media, Apple vendor keys
- **Condition Types** — [references/conditions.md](references/conditions.md) — Application, device, keyboard type, variable, input source conditions
- **Modification Patterns** — [references/patterns.md](references/patterns.md) — 7 patterns: simple remap, dual-function, app-specific, double-tap, shell command, mouse control, hyper key
- **Software Functions** — [references/software-functions.md](references/software-functions.md) — Open app, set mouse position, sleep, double-click
- **Parameters** — [references/parameters.md](references/parameters.md) — Timing parameters and mouse key configuration
- **Maintenance & Troubleshooting** — [references/maintenance.md](references/maintenance.md) — Service restart, uninstall, device info, logs, environment variables

## Scripts & Templates

- **Environment Inspector** — [scripts/inspect_environment.sh](scripts/inspect_environment.sh) — Gather installation status, profiles, devices, and rules
- **Configuration Manager** — [scripts/config_manager.py](scripts/config_manager.py) — Safe JSON manipulation utilities for backups, rule management, and profile editing
- **Common Rules** — [assets/common_rules.json](assets/common_rules.json) — Caps Lock remap, dual-function, Vim arrows, double-tap quit templates
- **Key Codes Reference** — [assets/key_codes_reference.json](assets/key_codes_reference.json) — Complete machine-readable key code listing

## Agent Workflow

When a user requests a new mapping:

1. **Understand the request** — Clarify key(s), modifier(s), and action(s)
2. **Check current config** — Read existing karabiner.json
3. **Validate** — Ensure no conflicts with existing rules
4. **Generate JSON** — Create the proper rule structure
5. **Preview changes** — Show the generated JSON or diff and ask for confirmation
6. **Apply changes** — Add to complex_modifications in karabiner.json or create a separate file in assets/complex_modifications/
7. **Test** — Verify the change took effect
8. **Document** — Explain what was changed and how to roll back

Always back up before modifying:
```bash
cp ~/.config/karabiner/karabiner.json ~/.config/karabiner/karabiner.json.backup.$(date +%Y%m%d%H%M%S)
```

Use the configuration manager at [scripts/config_manager.py](scripts/config_manager.py) for safe JSON manipulation.
Its write commands preview by default; pass `--yes` only after the user approves
the shown diff.

## Important Notes

1. **JSON Comments** — Karabiner.json supports comments, but they may be lost if edited via the GUI
2. **Profile Selection** — Only one profile is active at a time (`"selected": true`)
3. **Rule Order** — Rules are evaluated in order; first match wins
4. **Device Specificity** — Use `device_if` conditions to target specific keyboards
5. **Virtual Keyboard Type** — Set to "ansi", "iso", or "jis" based on layout
6. **Modifier Consumption** — Mandatory modifiers are removed from output; optional are preserved
