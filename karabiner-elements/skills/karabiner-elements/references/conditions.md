# Condition Types

### Application-Based Conditions
```json
{
    "type": "frontmost_application_if",
    "bundle_identifiers": ["^com\\.apple\\.Terminal$"]
}
```

### Device-Based Conditions
```json
{
    "type": "device_if",
    "identifiers": [
        { "vendor_id": 1452 },
        { "is_built_in_keyboard": true }
    ]
}
```

### Keyboard Type Conditions
```json
{
    "type": "keyboard_type_if",
    "keyboard_types": ["ansi", "iso"]
}
```

### Variable Conditions
```json
{
    "type": "variable_if",
    "name": "my_variable",
    "value": 1
}
```

### Input Source Conditions
```json
{
    "type": "input_source_if",
    "input_sources": [{ "language": "en" }]
}
```
