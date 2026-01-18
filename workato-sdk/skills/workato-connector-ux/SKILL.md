---
name: Workato Connector UX
description: This skill should be used when the user asks to "build a Workato connector", "create a custom connector", "improve connector UX", "add input fields to connector", "make fields sticky", "use extends_schema", "add dynamic fields", or is working with Workato SDK Ruby DSL for custom connectors. Also use proactively when implementing connector actions or configuring input field visibility.
version: 0.1.0
---

# Workato Connector SDK - Recipe Developer UX Patterns

Guide for building Workato custom connectors with excellent recipe developer experience. Focus on field visibility, dynamic schemas, and input patterns that make connectors intuitive to configure.

## Core Principle: Recipe Developer First

Connector inputs must be designed from the recipe developer's perspective. Every field must be:
- **Visible when needed** — Use `sticky: true` for primary inputs
- **Pre-configured when possible** — Use `default:` for common choices
- **Contextually shown** — Use `ngIf` and `extends_schema` for conditional fields

## Field Visibility Patterns

### sticky: true

Mark fields as sticky to keep them visible in the recipe editor. Without sticky, optional fields collapse into "Show optional fields".

**When to use:**
- Primary input fields (the main data users enter)
- Fields users configure in most recipes
- Source type selectors after a parent choice
- Both fields in a paired object (like `type` + `budget_tokens`)

```ruby
{
  name: 'message',
  label: 'Text to send',
  type: 'string',
  control_type: 'text-area',
  sticky: true,              # Always visible
  optional: true,
  hint: 'The message content.'
}
```

### default: value

Pre-populate selectors so users see input fields immediately without making a selection first.

**When to use:**
- Mode selectors where one option is most common
- Configuration fields with sensible defaults
- Version fields with a current stable value

```ruby
{
  name: 'message_type',
  control_type: 'select',
  pick_list: 'message_types',
  optional: false,
  default: 'single_message',  # Most common choice
  hint: 'Choose message type.'
}
```

### Combining sticky + default

For the best UX, combine both patterns:

```ruby
{
  name: 'temperature',
  control_type: 'number',
  convert_input: 'float_conversion',
  sticky: true,           # Always visible
  default: 1.0,           # Sensible starting value
  hint: 'Controls randomness (0.0-2.0).'
}
```

## Dynamic Schema Patterns

### extends_schema

Use `extends_schema: true` when a field selection should reveal additional fields. Workato re-evaluates the schema when this field changes.

```ruby
{
  name: 'source_type',
  control_type: 'select',
  pick_list: 'source_types',
  extends_schema: true,     # Triggers schema refresh
  sticky: true,
  hint: 'How to provide the data.'
}
```

### ngIf Conditionals

Show fields only when relevant using `ngIf` with input path expressions:

```ruby
# Show URL field only when source_type is 'url'
{
  name: 'image_url',
  label: 'Image URL',
  type: 'string',
  ngIf: 'input.source_type == "url"',
  hint: 'Public URL of the image.'
},

# Show base64 fields only when source_type is 'base64'
{
  name: 'image_data',
  label: 'Image data (Base64)',
  type: 'string',
  control_type: 'text-area',
  ngIf: 'input.source_type == "base64"',
  hint: 'Base64-encoded image data.'
}
```

### Nested ngIf Paths

For fields inside objects or arrays, use dot notation:

```ruby
ngIf: 'input.tool_choice.type == "tool"'
ngIf: 'input.block_type == "document" && input.document_source_type == "file"'
```

## toggle_field Pattern

Allow both dropdown selection and custom text input:

```ruby
{
  name: 'model',
  control_type: 'select',
  pick_list: 'model_list',
  toggle_hint: 'Select from list',
  toggle_field: {
    name: 'model',
    label: 'Model ID',
    type: 'string',
    control_type: 'text',
    toggle_hint: 'Enter model ID',
    hint: 'Enter model ID directly, e.g. custom-model-v1'
  }
}
```

## Control Types Reference

| control_type | Use For | Notes |
|--------------|---------|-------|
| `text` | Short strings | Default for string type |
| `text-area` | Long text, JSON | Multi-line input |
| `select` | Single choice | Requires `pick_list` or `options` |
| `multiselect` | Multiple choices | Returns array, needs `delimiter` |
| `number` | Decimals | Use with `float_conversion` |
| `integer` | Whole numbers | Use with `integer_conversion` |
| `checkbox` | Boolean | Use with `boolean_conversion` |
| `password` | Secrets | Masked input |
| `schema-designer` | JSON schema | Visual schema builder |

## Type Conversions

Always pair control types with appropriate conversions:

```ruby
{ control_type: 'integer', convert_input: 'integer_conversion' }
{ control_type: 'number', convert_input: 'float_conversion' }
{ control_type: 'checkbox', convert_input: 'boolean_conversion' }
```

## List Mode Patterns

### Static Lists (Fixed Items)

Use for small, bounded collections:

```ruby
{
  name: 'items',
  type: 'array',
  of: 'object',
  list_mode: 'static',
  list_mode_toggle: true,    # Allow switching to dynamic
  properties: [...]
}
```

### Dynamic Lists (From Datapills)

Use when items come from upstream data:

```ruby
{
  name: 'messages',
  type: 'array',
  of: 'object',
  list_mode: 'dynamic',
  list_mode_toggle: true,
  properties: [...]
}
```

## Object Definitions Pattern

Define reusable schemas in `object_definitions:` block:

```ruby
object_definitions: {
  message_input: {
    fields: lambda do |_connection, config_fields, _object_definitions|
      # Dynamic field generation based on config_fields
      is_single = config_fields['mode'] == 'single'

      if is_single
        [{ name: 'text', type: 'string', sticky: true }]
      else
        [{ name: 'messages', type: 'array', of: 'object', properties: [...] }]
      end
    end
  }
}
```

Reference in actions:

```ruby
input_fields: lambda do |object_definitions|
  object_definitions['message_input']
end
```

## Pick Lists

### Static Pick Lists

Define in `pick_lists:` block:

```ruby
pick_lists: {
  source_types: lambda do
    [['Base64 encoded', 'base64'], ['URL', 'url']]
  end
}
```

### Dynamic Pick Lists (API-driven)

Fetch options from API:

```ruby
pick_lists: {
  model_list: lambda do
    get('v1/models')&.[]('data')&.map do |model|
      [model['display_name'], model['id']]
    end
  end
}
```

### Connection Fields Limitation

Connection fields cannot reference `pick_lists:` (authentication not yet available). Use inline `options:` instead:

```ruby
# In connection: fields:
{
  name: 'version',
  control_type: 'select',
  options: [['2023-06-01', '2023-06-01']],  # Inline, not pick_list
  default: '2023-06-01'
}
```

## Helper Methods Pattern

Define reusable logic in `methods:` block:

```ruby
methods: {
  get_content_block_properties: lambda do
    [
      { name: 'block_type', control_type: 'select', ... },
      { name: 'url', ngIf: 'input.block_type == "url"', ... }
    ]
  end
}
```

Call methods with `call('method_name', args)`:

```ruby
content_props = call('get_content_block_properties')
```

## Hints Best Practices

Hints must be crafted from the recipe developer's perspective:

- **Explain what, not how** — "The maximum tokens to generate" not "Set this to control output length"
- **Mention defaults** — "Defaults to 4096 if left blank"
- **Link to docs** — Use `<a href="..." target="_blank">docs</a>` for complex topics
- **Be concise** — One sentence when possible

```ruby
hint: 'Maximum tokens to generate. See <a href="https://docs.example.com/models" ' \
      'target="_blank">models</a> for limits. Defaults to 4096.'
```

## Additional Resources

### Reference Files

For detailed patterns and complete examples, consult:
- **`references/field-patterns.md`** — Complete sticky, default, optional patterns with examples
- **`references/control-types.md`** — All control types with conversion requirements
- **`references/schema-patterns.md`** — Object definitions, methods, config_fields patterns
