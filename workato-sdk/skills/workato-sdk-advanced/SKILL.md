---
name: Workato SDK Advanced
description: This skill should be used when the user asks about "connector planning", "code patterns", "defining schema", "best practices workato", "error handling workato", "connector architecture", "object_definitions patterns", "reusable methods", or needs advanced guidance for building production-quality Workato connectors.
version: 0.1.0
---

# Workato SDK Advanced Patterns

Guide for advanced connector development patterns, architecture planning, and best practices.

## Overview

Building production-quality connectors requires:
- Thoughtful planning and API analysis
- Reusable code patterns
- Proper schema design
- Robust error handling
- Performance optimization

## Connector Planning

### API Analysis Checklist

Before building a connector, analyze:

1. **Authentication**
   - What auth method does the API use?
   - Are there multiple auth options?
   - How are tokens refreshed?

2. **Data Model**
   - What are the primary objects/resources?
   - How do objects relate to each other?
   - What fields are required vs optional?

3. **Operations**
   - What CRUD operations are available?
   - Are there batch operations?
   - What search/filter capabilities exist?

4. **Webhooks/Events**
   - Does the API support webhooks?
   - What events are available?
   - How is webhook security handled?

5. **Rate Limits**
   - What are the rate limits?
   - How should the connector handle throttling?

### Connector Structure

Organize connector code logically:

```ruby
{
  title: 'My Connector',

  # 1. Connection & Auth
  connection: { ... },

  # 2. Reusable Methods
  methods: { ... },

  # 3. Object Definitions (Schemas)
  object_definitions: { ... },

  # 4. Pick Lists
  pick_lists: { ... },

  # 5. Actions
  actions: { ... },

  # 6. Triggers
  triggers: { ... },

  # 7. Streams (if needed)
  streams: { ... }
}
```

## Code Patterns

### Reusable Methods

Extract common logic into methods:

```ruby
methods: {
  # Pagination helper
  paginate: lambda do |endpoint, params = {}|
    results = []
    page = 1

    loop do
      response = get(endpoint).params(params.merge(page: page, per_page: 100))
      results.concat(response['items'])
      break unless response['has_more']
      page += 1
    end

    results
  end,

  # Error handling wrapper
  safe_request: lambda do |&block|
    block.call
      .after_error_response(/4\d{2}/) do |code, body, headers, message|
        error("API Error (#{code}): #{body['error'] || message}")
      end
      .after_error_response(/5\d{2}/) do |code, body, headers, message|
        error("Server Error (#{code}): Please try again later")
      end
  end,

  # Field mapping
  map_fields: lambda do |record, field_map|
    field_map.each_with_object({}) do |(api_field, workato_field), result|
      result[workato_field] = record[api_field] if record[api_field]
    end
  end
}
```

### Using Methods

```ruby
execute: lambda do |connection, input|
  records = call('paginate', '/api/records', { status: 'active' })
  records.map { |r| call('map_fields', r, { 'id' => 'record_id', 'name' => 'title' }) }
end
```

## Schema Design

### Object Definitions

Define reusable schemas:

```ruby
object_definitions: {
  # Base record schema
  record: {
    fields: lambda do |connection, config_fields|
      [
        { name: 'id', label: 'Record ID' },
        { name: 'name', label: 'Name' },
        { name: 'created_at', label: 'Created At', type: 'date_time' },
        { name: 'updated_at', label: 'Updated At', type: 'date_time' }
      ]
    end
  },

  # Input-specific schema (writable fields only)
  record_input: {
    fields: lambda do |connection, config_fields|
      [
        { name: 'name', label: 'Name', optional: false },
        { name: 'email', label: 'Email', control_type: 'email' },
        { name: 'status', control_type: 'select', pick_list: 'statuses' }
      ]
    end
  },

  # Dynamic schema based on config
  dynamic_record: {
    fields: lambda do |connection, config_fields|
      object_type = config_fields['object_type']
      get("/api/schemas/#{object_type}")['fields'].map do |field|
        {
          name: field['name'],
          label: field['label'],
          type: field['type'],
          optional: !field['required']
        }
      end
    end
  }
}
```

### Schema Composition

Combine schemas:

```ruby
input_fields: lambda do |object_definitions|
  [
    { name: 'id', optional: false }
  ].concat(object_definitions['record_input'])
end
```

## Error Handling

### Comprehensive Error Handling

```ruby
execute: lambda do |connection, input|
  post('/api/records')
    .payload(input)
    .after_error_response(400) do |code, body, headers, message|
      # Validation errors
      errors = body['errors']&.map { |e| e['message'] }&.join(', ')
      error("Validation failed: #{errors || body['message']}")
    end
    .after_error_response(401) do |code, body, headers, message|
      error("Authentication failed. Please reconnect.")
    end
    .after_error_response(403) do |code, body, headers, message|
      error("Permission denied: #{body['message']}")
    end
    .after_error_response(404) do |code, body, headers, message|
      error("Resource not found")
    end
    .after_error_response(429) do |code, body, headers, message|
      retry_after = headers['Retry-After']
      error("Rate limited. Retry after #{retry_after} seconds")
    end
    .after_error_response(/5\d{2}/) do |code, body, headers, message|
      error("Server error (#{code}). Please try again later.")
    end
end
```

### Retry Logic

```ruby
actions: {
  create_with_retry: {
    execute: lambda do |connection, input|
      post('/api/records').payload(input)
    end,

    retry_on_response: [429, 503],
    max_retries: 3
  }
}
```

## Best Practices

### Naming Conventions

- **Actions**: Verb + noun (`create_record`, `search_contacts`)
- **Triggers**: `new_` prefix (`new_record`, `new_event`)
- **Fields**: snake_case matching API where possible

### Performance

1. **Minimize API calls** - Batch requests when possible
2. **Use pagination** - Don't fetch all records at once
3. **Cache static data** - Store picklist values
4. **Optimize webhooks** - Use webhooks over polling when available

### Security

1. **Never log credentials** - Use `control_type: 'password'`
2. **Validate webhooks** - Always verify signatures
3. **Sanitize inputs** - Escape user data in URLs
4. **Use HTTPS** - Never allow HTTP connections

### User Experience

1. **Clear labels** - Use descriptive field names
2. **Helpful hints** - Explain what fields do
3. **Smart defaults** - Pre-populate common values
4. **Validation** - Catch errors before API calls

## Debugging

### Local Testing

```ruby
# Add debug output
execute: lambda do |connection, input|
  workato.log("Input: #{input.inspect}")

  response = get('/api/records')
  workato.log("Response: #{response.inspect}")

  response
end
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "undefined method" | Method not defined | Check method name spelling |
| Empty response | Wrong endpoint/params | Log request, check API docs |
| Auth fails | Token expired | Implement token refresh |
| Missing fields | Schema mismatch | Update object_definitions |

## Reference Files

For detailed documentation:

### Connector Guide
- **`references/guides__advanced-connector-guide__introduction.md`** - Guide overview
- **`references/guides__advanced-connector-guide__connector-planning.md`** - Planning checklist
- **`references/guides__advanced-connector-guide__connector-building-defining-schema.md`** - Schema design
- **`references/guides__advanced-connector-guide__connector-building-building-actions.md`** - Action patterns
- **`references/guides__advanced-connector-guide__connector-building-building-triggers.md`** - Trigger patterns
- **`references/guides__advanced-connector-guide__connector-building-code-patterns.md`** - Code patterns

### Best Practices
- **`references/guides__best-practices.md`** - General best practices
- **`references/guides__error-handling.md`** - Error handling patterns
- **`references/guides__debugging.md`** - Debugging techniques
