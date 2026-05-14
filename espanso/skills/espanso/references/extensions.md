# Espanso Extensions Reference

## date

Inserts dynamic date/time values.

```yaml
vars:
  - name: mydate
    type: date
    params:
      format: "%Y-%m-%d"       # strftime format string
      locale: "en-US"          # optional: locale for day/month names
      offset: 86400            # optional: seconds offset (86400 = tomorrow, -86400 = yesterday)
      tz: "America/New_York"   # optional: timezone (v2.3.0+)
```

Common format strings:
- `%Y-%m-%d` → `2025-03-18`
- `%m/%d/%Y` → `03/18/2025`
- `%A, %B %d, %Y` → `Tuesday, March 18, 2025`
- `%H:%M` → `14:30`
- `%I:%M %p` → `02:30 PM`

## shell

Runs a shell command and inserts stdout.

```yaml
vars:
  - name: output
    type: shell
    params:
      cmd: "date +%s"           # shell command (macOS: zsh/bash)
      shell: bash               # optional: bash, zsh, sh, powershell
      trim: true                # optional: trim trailing newline (default: true)
```

## clipboard

Inserts current clipboard content.

```yaml
vars:
  - name: clip
    type: clipboard
```

No params required. Access via `{{clip}}` in replace string.

## form

Shows a popup dialog before expanding. Use `[[fieldname]]` in layout to define fields.

```yaml
vars:
  - name: form1
    type: form
    params:
      layout: |
        Title: [[title]]
        Body:
        [[body]]
      fields:
        title:
          default: "Untitled"    # optional default value
        body:
          multiline: true        # multiline text area
          default: ""
```

Access field values with `{{form1.fieldname}}`.

## random

Picks a random item from a list.

```yaml
vars:
  - name: greet
    type: random
    params:
      choices:
        - "Hey!"
        - "Hi there!"
        - "Hello!"
```

## script

Runs an external script file and inserts stdout.

```yaml
vars:
  - name: result
    type: script
    params:
      args:
        - python3
        - /path/to/script.py
```

## Nested Variables

Variables can reference other variables in their params:

```yaml
- trigger: ":now"
  replace: "It's {{mytime}}"
  vars:
    - name: fmt
      type: shell
      params:
        cmd: echo "%H:%M"
    - name: mytime
      type: date
      params:
        format: "{{fmt}}"
```
