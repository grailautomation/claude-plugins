---
name: Workato SDK Reference
description: This skill should be used when the user asks about "sdk reference", "actions block reference", "triggers block reference", "object_definitions", "methods block", "pick_lists", "schema block", "http methods workato", "ruby methods workato", or needs API reference documentation for Workato SDK blocks and methods.
version: 0.1.0
---

# Workato SDK Reference

Comprehensive reference for all Workato Connector SDK blocks, methods, and configuration options.

## Overview

The Workato SDK consists of these main blocks:

| Block | Purpose |
|-------|---------|
| `connection` | Authentication and base configuration |
| `actions` | Operations users can perform |
| `triggers` | Events that start recipes |
| `methods` | Reusable helper functions |
| `object_definitions` | Reusable schema definitions |
| `pick_lists` | Dropdown options |
| `streams` | Large file handling |

## Connection Block

Defines authentication and connection settings.

```ruby
connection: {
  fields: Array,           # Credential input fields
  authorization: Hash,     # Auth type and configuration
  base_uri: lambda,        # Base URL for requests
  test: lambda            # Connection test
}
```

### Authorization Types

| Type | Use Case |
|------|----------|
| `basic_auth` | Username/password |
| `api_key` | API key in header/query |
| `oauth2` | OAuth 2.0 flows |
| `custom_auth` | Custom auth logic |
| `multi` | Multiple auth options |
| `aws_auth` | AWS Signature v4 |

## Actions Block

Defines connector operations.

```ruby
actions: {
  action_name: {
    title: String,                    # Display name
    subtitle: String,                 # Secondary description
    description: lambda,              # Dynamic description
    help: String | lambda,            # Help text
    config_fields: Array,             # Mode selectors
    input_fields: lambda,             # Input schema
    execute: lambda,                  # Main logic
    output_fields: lambda,            # Output schema
    sample_output: lambda,            # Sample data
    retry_on_response: Array,         # HTTP codes to retry
    retry_on_request: Array,          # Errors to retry
    max_retries: Integer,             # Retry count
    summarize_input: Array,           # Input summary fields
    summarize_output: Array           # Output summary fields
  }
}
```

### Execute Lambda Parameters

```ruby
execute: lambda do |connection, input, extended_input_schema, extended_output_schema, continue|
  # connection - credentials hash
  # input - user inputs
  # extended_input_schema - dynamic schema info
  # extended_output_schema - dynamic output schema
  # continue - multistep continuation data
end
```

## Triggers Block

Defines event triggers.

```ruby
triggers: {
  trigger_name: {
    title: String,
    description: lambda,
    config_fields: Array,
    input_fields: lambda,
    poll: lambda,                     # Polling logic
    webhook_subscribe: lambda,        # Webhook registration
    webhook_unsubscribe: lambda,      # Webhook cleanup
    webhook_notification: lambda,     # Webhook handler
    dedup: lambda,                    # Deduplication
    output_fields: lambda,
    sample_output: lambda
  }
}
```

### Poll Lambda Returns

```ruby
poll: lambda do |connection, input, closure|
  {
    events: Array,          # Records to process
    next_poll: Any,         # Stored in closure
    can_poll_more: Boolean  # Continue polling?
  }
end
```

## Methods Block

Reusable helper functions.

```ruby
methods: {
  method_name: lambda do |arg1, arg2|
    # Logic here
  end
}
```

### Calling Methods

```ruby
result = call('method_name', arg1, arg2)
```

## Object Definitions Block

Reusable field schemas.

```ruby
object_definitions: {
  schema_name: {
    fields: lambda do |connection, config_fields, object_definitions|
      [
        { name: 'field_name', label: 'Label', type: 'string' }
      ]
    end
  }
}
```

### Referencing Object Definitions

```ruby
input_fields: lambda do |object_definitions|
  object_definitions['schema_name']
end
```

## Pick Lists Block

Dropdown options.

```ruby
pick_lists: {
  # Static list
  statuses: lambda do
    [
      ['Active', 'active'],
      ['Inactive', 'inactive']
    ]
  end,

  # Dynamic list
  objects: lambda do |connection|
    get('/api/objects').map { |o| [o['name'], o['id']] }
  end,

  # Dependent list
  fields: lambda do |connection, object_type:|
    get("/api/objects/#{object_type}/fields").map { |f| [f['label'], f['name']] }
  end
}
```

## HTTP Methods

### Request Methods

| Method | Usage |
|--------|-------|
| `get(url)` | GET request |
| `post(url)` | POST request |
| `put(url)` | PUT request |
| `patch(url)` | PATCH request |
| `delete(url)` | DELETE request |

### Request Modifiers

```ruby
get('/api/records')
  .params(key: 'value')              # Query parameters
  .payload(data)                     # Request body
  .headers('X-Custom' => 'value')    # Custom headers
  .request_format_json               # JSON body (default)
  .request_format_xml                # XML body
  .request_format_www_form_urlencoded # Form body
  .request_format_multipart_form     # Multipart body
  .response_format_json              # Parse JSON (default)
  .response_format_xml               # Parse XML
  .response_format_raw               # Raw response
```

### Error Handling

```ruby
get('/api/records')
  .after_response do |code, body, headers|
    # Handle any response
  end
  .after_error_response(400) do |code, body, headers, message|
    # Handle specific error
  end
  .after_error_response(/4\d{2}/) do |code, body, headers, message|
    # Handle error pattern
  end
```

## Field Schema

### Field Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | String | Internal field name |
| `label` | String | Display label |
| `type` | String | Data type |
| `control_type` | String | UI control |
| `optional` | Boolean | Required field? |
| `default` | Any | Default value |
| `hint` | String | Help text |
| `sticky` | Boolean | Always visible |
| `extends_schema` | Boolean | Triggers schema refresh |
| `ngIf` | String | Conditional visibility |
| `pick_list` | String | Dropdown source |
| `toggle_field` | Hash | Toggle input |

### Data Types

| Type | Description |
|------|-------------|
| `string` | Text (default) |
| `integer` | Whole numbers |
| `number` | Decimal numbers |
| `boolean` | True/false |
| `date` | Date only |
| `date_time` | Date and time |
| `timestamp` | Unix timestamp |
| `object` | Nested object |
| `array` | List of items |

### Control Types

| Control | Use Case |
|---------|----------|
| `text` | Single line text |
| `text-area` | Multi-line text |
| `select` | Dropdown |
| `multiselect` | Multiple selection |
| `number` | Number input |
| `integer` | Integer input |
| `checkbox` | Boolean toggle |
| `password` | Masked input |
| `date` | Date picker |
| `date_time` | DateTime picker |
| `email` | Email input |
| `url` | URL input |
| `phone` | Phone input |

## Ruby Methods

### Workato-Specific Methods

```ruby
workato.log(message)                    # Debug logging
workato.parse_json(string)              # Parse JSON
workato.parse_xml(string)               # Parse XML
workato.hmac_sha256(data, key)          # HMAC SHA256
workato.jwt_encode(payload, key, alg)   # JWT encoding
workato.uuid                            # Generate UUID
workato.trigger_limit                   # Current trigger limit
workato.resume_url                      # Wait-for-resume URL
workato.stream.in(data)                 # Stream input
workato.stream.out(name, input)         # Stream output
```

### Allowed Ruby Methods

Common Ruby methods available in SDK:
- String: `split`, `gsub`, `match`, `strip`, `upcase`, `downcase`
- Array: `map`, `select`, `reject`, `find`, `first`, `last`, `flatten`
- Hash: `dig`, `merge`, `slice`, `except`, `each`, `keys`, `values`
- Time: `now`, `parse`, `iso8601`, `strftime`
- Integer: `to_s`, `to_i`, `abs`, `times`

## Reference Files

For complete documentation:

### Core References
- **`references/sdk-reference.md`** - SDK overview
- **`references/sdk-reference__actions.md`** - Actions reference
- **`references/sdk-reference__triggers.md`** - Triggers reference
- **`references/sdk-reference__connection.md`** - Connection reference
- **`references/sdk-reference__connection__authorization.md`** - Authorization details

### Schema & Methods
- **`references/sdk-reference__schema.md`** - Field schema reference
- **`references/sdk-reference__object_definitions.md`** - Object definitions
- **`references/sdk-reference__methods.md`** - Methods block
- **`references/sdk-reference__picklists.md`** - Pick lists

### HTTP & Utilities
- **`references/sdk-reference__http.md`** - HTTP methods
- **`references/sdk-reference__ruby_methods.md`** - Allowed Ruby methods
- **`references/sdk-reference__streams.md`** - Streaming reference
- **`references/sdk-reference__test.md`** - Testing reference

### Other
- **`references/sdk-reference__custom-action.md`** - Custom action support
- **`references/sdk-reference__whitelist-removal.md`** - Deprecated methods
- **`references/guides.md`** - Guides index
