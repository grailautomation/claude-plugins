---
name: Workato SDK Quickstart
description: This skill should be used when the user asks about "getting started workato sdk", "first connector", "connector quickstart", "share connector", "version control connector", "workato walkthrough", "connector examples", or is new to building Workato custom connectors.
version: 0.1.0
---

# Workato SDK Quickstart

Guide for getting started with Workato custom connector development.

## Overview

Workato custom connectors allow you to connect to any API not covered by built-in connectors. This guide covers:
- Setting up your first connector
- Basic connector structure
- Testing and debugging
- Sharing and version control

## Prerequisites

- Workato account with SDK access
- Basic Ruby knowledge
- API documentation for your target service

## Your First Connector

### Minimal Connector

Start with the simplest possible connector:

```ruby
{
  title: 'My First Connector',

  connection: {
    fields: [
      { name: 'api_key', label: 'API Key', control_type: 'password' }
    ],

    authorization: {
      type: 'api_key',
      apply: lambda do |connection|
        headers('Authorization' => "Bearer #{connection['api_key']}")
      end
    },

    base_uri: lambda do |connection|
      'https://api.example.com'
    end,

    test: lambda do |connection|
      get('/me')
    end
  },

  actions: {
    test_action: {
      title: 'Test action',

      input_fields: lambda do
        [{ name: 'message', label: 'Message' }]
      end,

      execute: lambda do |connection, input|
        { echo: input['message'] }
      end,

      output_fields: lambda do
        [{ name: 'echo', label: 'Echo' }]
      end
    }
  }
}
```

### Building Blocks

#### Connection Block

Handles authentication:

```ruby
connection: {
  fields: [
    # Credential inputs shown to users
  ],
  authorization: {
    # How to apply credentials to requests
  },
  base_uri: lambda do |connection|
    # Base URL for all API calls
  end,
  test: lambda do |connection|
    # Lightweight call to verify credentials work
  end
}
```

#### Actions Block

Operations users can perform:

```ruby
actions: {
  action_name: {
    title: 'Human readable title',

    input_fields: lambda do
      # Fields users fill in
    end,

    execute: lambda do |connection, input|
      # API call logic
    end,

    output_fields: lambda do
      # Fields available as datapills
    end
  }
}
```

#### Triggers Block

Events that start recipes:

```ruby
triggers: {
  trigger_name: {
    title: 'New something',

    poll: lambda do |connection, input, closure|
      # Check for new records
    end,

    dedup: lambda do |record|
      # Unique identifier for deduplication
    end,

    output_fields: lambda do
      # Fields available as datapills
    end
  }
}
```

## Testing Your Connector

### In Workato UI

1. Go to **Tools > Connector SDK**
2. Paste your connector code
3. Click **Test** to verify connection
4. Use **Debugger** tab to test actions/triggers

### Local Development (CLI)

```bash
# Install SDK gem
gem install workato-connector-sdk

# Create project
workato new my_connector
cd my_connector

# Test connection
workato exec connection.authorization --settings=settings.yaml

# Test action
workato exec actions.test_action --input='{"message": "hello"}'
```

## Common Patterns

### Making API Calls

```ruby
# GET request
get('/api/records')

# GET with params
get('/api/records').params(status: 'active', limit: 10)

# POST with payload
post('/api/records').payload(name: 'Test', email: 'test@example.com')

# PUT/PATCH
put("/api/records/#{id}").payload(input)
patch("/api/records/#{id}").payload(input)

# DELETE
delete("/api/records/#{id}")
```

### Handling Responses

```ruby
execute: lambda do |connection, input|
  response = get('/api/records')

  # Response is automatically parsed JSON
  {
    total: response['total'],
    records: response['items']
  }
end
```

### Error Handling

```ruby
execute: lambda do |connection, input|
  post('/api/records')
    .payload(input)
    .after_error_response(/4\d{2}/) do |code, body, headers, message|
      error("API Error: #{body['message']}")
    end
end
```

## Debugging Tips

### Use Logging

```ruby
execute: lambda do |connection, input|
  workato.log("Input received: #{input.inspect}")

  response = get('/api/records')
  workato.log("API response: #{response.inspect}")

  response
end
```

### Check Common Issues

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Connection fails | Wrong credentials | Verify API key/secret |
| Empty response | Wrong endpoint | Check API docs for URL |
| Missing fields | Schema mismatch | Update output_fields |
| Action errors | Bad input | Add input validation |

## Sharing Connectors

### Export/Import

1. **Export**: Copy connector code from SDK editor
2. **Import**: Paste into another workspace's SDK editor

### Workato Community

Share connectors via Workato Community Library:
1. Test thoroughly
2. Document usage
3. Submit for review

### Version Control

Use Git to track connector changes:

```bash
# Initialize repo
git init

# Track connector file
git add connector.rb
git commit -m "Initial connector"

# Create branch for new feature
git checkout -b add-search-action
```

## Platform Limits

Be aware of Workato platform limits:

| Limit | Value |
|-------|-------|
| Max connector size | 1 MB |
| Action timeout | 120 seconds |
| Trigger poll interval | 5 minutes minimum |
| Webhook payload | 10 MB |

## Next Steps

After your first connector:

1. **Add more actions** - CRUD operations for main objects
2. **Add triggers** - Real-time events via webhooks
3. **Improve UX** - Dynamic fields, helpful hints
4. **Add tests** - RSpec tests for reliability

## Reference Files

For detailed documentation:

### Getting Started
- **`references/quickstart.md`** - Quickstart overview
- **`references/guides__walkthrough.md`** - Step-by-step walkthrough
- **`references/guides__examples.md`** - Example connectors

### Debugging & Testing
- **`references/quickstart__debugging.md`** - Debugging guide
- **`references/quickstart__FAQ.md`** - Frequently asked questions

### Sharing & Deployment
- **`references/quickstart__sharing.md`** - Sharing connectors
- **`references/quickstart__version-control.md`** - Version control practices

### Platform
- **`references/limits.md`** - Platform limits and quotas
