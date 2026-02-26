# Common Modification Patterns

### Pattern 1: Simple Key Remap
Remap Caps Lock to Escape:
```json
{
    "description": "Caps Lock to Escape",
    "manipulators": [{
        "type": "basic",
        "from": { "key_code": "caps_lock", "modifiers": { "optional": ["any"] } },
        "to": [{ "key_code": "escape" }]
    }]
}
```


### Pattern 2: Dual-Function Key (Tap vs Hold)
Control when held, Escape when tapped:
```json
{
    "description": "Control/Escape on Left Control",
    "manipulators": [{
        "type": "basic",
        "from": { "key_code": "left_control", "modifiers": { "optional": ["any"] } },
        "to": [{ "key_code": "left_control" }],
        "to_if_alone": [{ "key_code": "escape" }]
    }]
}
```

### Pattern 3: App-Specific Remap
Disable Cmd+L in Finder:
```json
{
    "description": "Disable Cmd+L in Finder",
    "manipulators": [{
        "type": "basic",
        "from": {
            "key_code": "l",
            "modifiers": { "mandatory": ["command"], "optional": ["caps_lock"] }
        },
        "conditions": [{
            "type": "frontmost_application_if",
            "bundle_identifiers": ["^com\\.apple\\.finder$"]
        }]
    }]
}
```

### Pattern 4: Double-Tap Action
Double-tap Right Shift for Mission Control:
```json
{
    "description": "Double Right Shift to Mission Control",
    "manipulators": [
        {
            "type": "basic",
            "from": { "key_code": "right_shift", "modifiers": { "optional": ["any"] } },
            "to": [
                { "apple_vendor_keyboard_key_code": "mission_control" },
                { "key_code": "vk_none" }
            ],
            "conditions": [{
                "type": "variable_if",
                "name": "right_shift_pressed",
                "value": 1
            }]
        },
        {
            "type": "basic",
            "from": { "key_code": "right_shift", "modifiers": { "optional": ["any"] } },
            "to": [
                { "set_variable": { "name": "right_shift_pressed", "value": 1 } },
                { "key_code": "right_shift" }
            ],
            "to_delayed_action": {
                "to_if_invoked": [{ "set_variable": { "name": "right_shift_pressed", "value": 0 } }],
                "to_if_canceled": [{ "set_variable": { "name": "right_shift_pressed", "value": 0 } }]
            }
        }
    ]
}
```


### Pattern 5: Shell Command Execution
```json
{
    "description": "Open Safari with Cmd+Shift+S",
    "manipulators": [{
        "type": "basic",
        "from": {
            "key_code": "s",
            "modifiers": { "mandatory": ["command", "shift"], "optional": ["caps_lock"] }
        },
        "to": [{ "shell_command": "open -a 'Safari.app'" }]
    }]
}
```

### Pattern 6: Mouse Control
```json
{
    "description": "Arrow keys as mouse movement with Right Shift",
    "manipulators": [
        {
            "type": "basic",
            "from": {
                "key_code": "up_arrow",
                "modifiers": { "mandatory": "right_shift", "optional": ["any"] }
            },
            "to": [{ "mouse_key": { "y": -1536 } }]
        }
    ]
}
```

### Pattern 7: Virtual Modifier (Hyper Key)
```json
{
    "description": "Caps Lock as Hyper Key",
    "manipulators": [{
        "type": "basic",
        "from": { "key_code": "caps_lock", "modifiers": { "optional": ["any"] } },
        "to": [{
            "set_variable": { "name": "hyper_active", "value": 1 }
        }],
        "to_after_key_up": [{
            "set_variable": { "name": "hyper_active", "value": 0 }
        }],
        "to_if_alone": [{ "key_code": "escape" }]
    }]
}
```
