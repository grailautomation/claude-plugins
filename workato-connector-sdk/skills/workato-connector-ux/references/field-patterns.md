# Field Visibility Patterns

Detailed patterns for controlling field visibility and defaults in Workato connectors.

## The Visibility Problem

By default, Workato hides optional fields behind "Show optional fields" expansion. This creates friction for recipe developers who must click to reveal commonly-used inputs.

**Solution hierarchy:**
1. `sticky: true` — Field always visible
2. `optional: false` — Field always visible (required)
3. `default: value` — Pre-selects value, triggers schema with `extends_schema`

## sticky: true Deep Dive

### When to Use sticky

| Scenario | Use sticky? | Reason |
|----------|-------------|--------|
| Primary text input | Yes | Users need to see where to enter data |
| Mode/type selector | Yes | Users must choose before seeing dependent fields |
| Configuration with default | Yes | Users may want to adjust common settings |
| Rarely-used option | No | Keep UI clean, let users expand if needed |
| Advanced configuration | No | Power users know to expand optional fields |

### sticky with Objects

When a field is an object, inner fields can also be sticky:

```ruby
{
  name: 'thinking',
  type: 'object',
  hint: 'Enable extended thinking for complex reasoning.',
  properties: [
    { name: 'type',
      control_type: 'select',
      pick_list: [['Enabled', 'enabled']],
      sticky: true,              # Visible when object expanded
      hint: 'Set to enabled to turn on thinking.' },
    { name: 'budget_tokens',
      control_type: 'integer',
      convert_input: 'integer_conversion',
      sticky: true,              # Both fields visible together
      hint: 'Token budget for thinking (min 1024).' }
  ]
}
```

### sticky with Arrays

For array item properties, sticky controls visibility within each item:

```ruby
{
  name: 'tools',
  type: 'array',
  of: 'object',
  list_mode: 'static',
  properties: [
    { name: 'name', sticky: true },       # Always visible in each item
    { name: 'description', sticky: true }, # Always visible in each item
    { name: 'cache_control' }              # Hidden under optional fields
  ]
}
```

## default: value Deep Dive

### Interaction with extends_schema

When a field has both `default` and `extends_schema`, Workato:
1. Sets the default value immediately
2. Triggers schema extension with that value
3. Shows dependent fields without user action

```ruby
{
  name: 'message_type',
  control_type: 'select',
  pick_list: 'message_types',
  default: 'single_message',    # Pre-selected
  extends_schema: true,         # Triggers schema refresh
  hint: 'Choose message type.'
}
```

This means dependent fields (via `ngIf: 'input.message_type == "single_message"'`) appear immediately.

### Default Value Types

| Field Type | Default Example | Notes |
|------------|-----------------|-------|
| String select | `default: 'option_value'` | Use internal value, not display label |
| Integer | `default: 4096` | No quotes needed |
| Number | `default: 1.0` | Include decimal for floats |
| Boolean | `default: true` | Use Ruby boolean |
| Multiselect | `default: ['a', 'b']` | Array of selected values |

### Don't Use default For

- Required fields without sensible defaults
- Fields where any assumption could be wrong
- Security-sensitive settings (tokens, limits)

## Combining Patterns

### Pattern: Config Field with Default

For configuration selectors that control action behavior:

```ruby
# In config_fields:
{
  name: 'output_format',
  control_type: 'select',
  pick_list: 'output_formats',
  default: 'json',           # Most common choice
  optional: false,           # Must be set (default handles it)
  extends_schema: true,      # May affect available fields
  hint: 'Response format.'
}
```

### Pattern: Primary Input Field

For the main data entry field in an action:

```ruby
{
  name: 'message',
  label: 'Message text',
  type: 'string',
  control_type: 'text-area',
  sticky: true,              # Always visible
  optional: true,            # Not required if alternatives exist
  hint: 'Enter the message content.'
}
```

### Pattern: Source Type Selector

For choosing how to provide data (URL vs base64, file vs inline):

```ruby
{
  name: 'image_source',
  label: 'Image source',
  control_type: 'select',
  pick_list: [['URL', 'url'], ['Base64', 'base64']],
  sticky: true,              # Visible after parent selection
  optional: true,
  extends_schema: true,      # Shows URL or base64 fields
  ngIf: 'input.content_type == "image"',
  hint: 'How to provide the image.'
}
```

### Pattern: Conditional Required Fields

Fields that are required only in certain modes:

```ruby
# URL field - required when source is URL
{
  name: 'image_url',
  type: 'string',
  optional: true,            # Optional overall
  ngIf: 'input.image_source == "url"',
  hint: 'Required when source is URL.'
}

# Validate in execute:
execute: lambda do |_connection, input|
  if input['image_source'] == 'url' && input['image_url'].blank?
    error('Image URL is required when source is URL')
  end
  # ...
end
```

## Anti-Patterns to Avoid

### Anti-Pattern: All Fields Optional, None Sticky

```ruby
# BAD: User sees empty form, must expand optional fields
{
  name: 'query',
  type: 'string',
  optional: true
  # Missing: sticky: true
}
```

### Anti-Pattern: Default Without extends_schema

```ruby
# BAD: Default set but dependent fields don't appear
{
  name: 'mode',
  control_type: 'select',
  default: 'advanced'
  # Missing: extends_schema: true
}
```

### Anti-Pattern: Sticky on Rarely-Used Fields

```ruby
# BAD: Clutters UI with fields most users ignore
{
  name: 'log_level',
  control_type: 'select',
  sticky: true,        # Don't make debug options sticky
  optional: true
}
```

## Field Ordering Strategy

Order fields for optimal UX:

1. **Config fields first** — Mode selectors that affect available fields
2. **Primary inputs** — Main data entry (sticky: true)
3. **Secondary inputs** — Common optional configuration (sticky: true)
4. **Advanced options** — Rarely-changed settings (no sticky)
5. **System fields** — Metadata, identifiers (no sticky)

Example action structure:

```ruby
config_fields: [
  { name: 'model', ... },           # 1. Model selection
  { name: 'message_type', ... }     # 1. Mode selector
],

input_fields: lambda do |object_definitions|
  [
    { name: 'message', sticky: true },      # 2. Primary input
    { name: 'system', sticky: true },       # 3. Common config
    { name: 'temperature', sticky: true },  # 3. Common config
    { name: 'max_tokens', sticky: true },   # 3. Common config
    { name: 'top_p' },                      # 4. Advanced
    { name: 'top_k' },                      # 4. Advanced
    { name: 'metadata' }                    # 5. System
  ]
end
```
