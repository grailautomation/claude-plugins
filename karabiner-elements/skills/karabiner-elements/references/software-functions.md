# Software Functions

### Open Application
```json
{ "software_function": { "open_application": { "bundle_identifier": "com.apple.Safari" } } }
{ "software_function": { "open_application": { "file_path": "/Applications/Safari.app" } } }
```

### Set Mouse Position
```json
{ "software_function": { "set_mouse_cursor_position": { "x": "50%", "y": "50%", "screen": 0 } } }
```

### System Sleep
```json
{ "software_function": { "iokit_power_management_sleep_system": { "delay_milliseconds": 500 } } }
```

### Double Click
```json
{ "software_function": { "cg_event_double_click": { "button": 0 } } }
```
