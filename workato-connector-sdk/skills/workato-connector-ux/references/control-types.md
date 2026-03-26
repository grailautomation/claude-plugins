# Control Types Reference

Complete reference for Workato SDK control types and their proper usage.

## Text Input Controls

### text (default)

Single-line text input. Default for `type: 'string'`.

```ruby
{
  name: 'title',
  type: 'string',
  control_type: 'text',  # Optional, this is default
  hint: 'Enter a title.'
}
```

### text-area

Multi-line text input for longer content.

```ruby
{
  name: 'message',
  type: 'string',
  control_type: 'text-area',
  hint: 'Enter the message content.'
}
```

**Use for:**
- Messages, descriptions, body content
- JSON input (with instructions to format)
- Code snippets, templates
- Any multi-line text

### password

Masked input for sensitive data.

```ruby
{
  name: 'api_key',
  type: 'string',
  control_type: 'password',
  hint: 'Your API key (will be masked).'
}
```

**Use in:**
- Connection fields for API keys, tokens
- Action fields for secrets that vary per recipe

## Selection Controls

### select

Single-choice dropdown.

```ruby
{
  name: 'format',
  control_type: 'select',
  pick_list: 'format_options',      # Reference to pick_lists
  hint: 'Choose output format.'
}
```

Or with inline options:

```ruby
{
  name: 'format',
  control_type: 'select',
  options: [
    ['JSON', 'json'],
    ['XML', 'xml'],
    ['CSV', 'csv']
  ],
  hint: 'Choose output format.'
}
```

**Array format:** `[['Display Label', 'value'], ...]`

### multiselect

Multiple-choice selection, returns array.

```ruby
{
  name: 'features',
  control_type: 'multiselect',
  pick_list: 'feature_options',
  delimiter: ',',                   # Required for proper handling
  hint: 'Select features to enable.'
}
```

**Result handling:**
```ruby
execute: lambda do |_connection, input|
  features = input['features']  # Array: ['feature1', 'feature2']
  # Or if delimiter specified, may be comma-separated string
  features_array = features.is_a?(Array) ? features : features.split(',')
end
```

## Numeric Controls

### integer

Whole number input.

```ruby
{
  name: 'max_tokens',
  control_type: 'integer',
  convert_input: 'integer_conversion',  # Required!
  hint: 'Maximum tokens (whole number).'
}
```

### number

Decimal number input.

```ruby
{
  name: 'temperature',
  control_type: 'number',
  convert_input: 'float_conversion',    # Required!
  hint: 'Temperature (0.0 to 2.0).'
}
```

**Always use convert_input** to ensure proper type handling.

## Boolean Control

### checkbox

Boolean toggle.

```ruby
{
  name: 'stream',
  type: 'boolean',
  control_type: 'checkbox',
  convert_input: 'boolean_conversion',  # Required!
  hint: 'Enable streaming response.'
}
```

**With toggle_field for datapill support:**

```ruby
{
  name: 'enabled',
  type: 'boolean',
  control_type: 'checkbox',
  convert_input: 'boolean_conversion',
  toggle_hint: 'Select from list',
  toggle_field: {
    name: 'enabled',
    type: 'string',
    control_type: 'text',
    convert_input: 'boolean_conversion',
    toggle_hint: 'Use custom value',
    hint: 'Enter true or false.'
  }
}
```

## Special Controls

### schema-designer

Visual JSON schema builder for complex inputs.

```ruby
{
  name: 'input_schema',
  type: 'object',
  properties: [
    {
      name: 'schema_builder',
      control_type: 'schema-designer',
      label: 'Schema',
      extends_schema: true,
      sticky: true,
      empty_schema_title: 'Define your schema fields.',
      sample_data_type: 'json',
      hint: 'Design the input schema visually.'
    }
  ]
}
```

**Use for:**
- Tool input schemas
- Dynamic object definitions
- User-defined data structures

### url

URL input with validation.

```ruby
{
  name: 'webhook_url',
  type: 'string',
  control_type: 'url',
  hint: 'Enter the webhook URL.'
}
```

### email

Email input with validation.

```ruby
{
  name: 'notification_email',
  type: 'string',
  control_type: 'email',
  hint: 'Email for notifications.'
}
```

## Type Conversions

### Required Conversions

| control_type | convert_input | Purpose |
|--------------|---------------|---------|
| integer | `integer_conversion` | String to Integer |
| number | `float_conversion` | String to Float |
| checkbox | `boolean_conversion` | String to Boolean |

### Why Conversions Matter

Without conversion, numeric inputs arrive as strings:

```ruby
# Without conversion
input['max_tokens']  # => "4096" (string!)

# With integer_conversion
input['max_tokens']  # => 4096 (integer)
```

**Always add conversion** for numeric and boolean fields.

## toggle_field Pattern

Allow both selection and custom input:

```ruby
{
  name: 'model',
  control_type: 'select',
  pick_list: 'model_list',
  optional: false,
  toggle_hint: 'Select from list',
  toggle_field: {
    name: 'model',
    label: 'Model ID',
    type: 'string',
    control_type: 'text',
    optional: false,
    toggle_hint: 'Enter model ID',
    hint: 'Enter custom model identifier.'
  }
}
```

**Key points:**
- Both fields must have same `name`
- Both should have matching `optional` status
- Set appropriate `toggle_hint` for each mode

## Control Type Selection Guide

### For Text Data

| Scenario | Control Type |
|----------|--------------|
| Short string (name, title) | `text` |
| Long text (message, body) | `text-area` |
| Sensitive data (API key) | `password` |
| URL | `url` |
| Email | `email` |

### For Numeric Data

| Scenario | Control Type + Conversion |
|----------|---------------------------|
| Count, ID, limit | `integer` + `integer_conversion` |
| Percentage, ratio | `number` + `float_conversion` |
| Currency (if decimal) | `number` + `float_conversion` |

### For Selection

| Scenario | Control Type |
|----------|--------------|
| Single choice | `select` |
| Multiple choices | `multiselect` |
| Choice with custom option | `select` + `toggle_field` |

### For Boolean

| Scenario | Control Type + Conversion |
|----------|---------------------------|
| Simple yes/no | `checkbox` + `boolean_conversion` |
| Boolean from datapill | `checkbox` + `toggle_field` |

### For Complex Data

| Scenario | Control Type |
|----------|--------------|
| JSON schema | `schema-designer` |
| File content | `text-area` (base64) |
| Structured object | `type: 'object'` with properties |
| List of items | `type: 'array'` with of + properties |
