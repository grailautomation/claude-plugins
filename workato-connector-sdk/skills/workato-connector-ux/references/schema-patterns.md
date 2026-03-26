# Schema Patterns

Patterns for object definitions, methods, config fields, and dynamic schemas.

## Object Definitions

### Basic Structure

Define reusable schemas in `object_definitions:` block:

```ruby
object_definitions: {
  user_output: {
    fields: lambda do |_connection, _config_fields, _object_definitions|
      [
        { name: 'id', type: 'string' },
        { name: 'name', type: 'string' },
        { name: 'email', type: 'string' }
      ]
    end
  }
}
```

### Dynamic Fields Based on Config

Use `config_fields` parameter to vary schema based on action configuration:

```ruby
object_definitions: {
  message_input: {
    fields: lambda do |_connection, config_fields, _object_definitions|
      is_single = config_fields['message_type'] == 'single_message'

      if is_single
        [
          {
            name: 'message',
            type: 'string',
            control_type: 'text-area',
            sticky: true,
            hint: 'Single message to send.'
          }
        ]
      else
        [
          {
            name: 'messages',
            type: 'array',
            of: 'object',
            list_mode: 'dynamic',
            properties: [
              { name: 'role', control_type: 'select', pick_list: 'roles' },
              { name: 'content', control_type: 'text-area', sticky: true }
            ]
          }
        ]
      end
    end
  }
}
```

### Referencing Object Definitions

In action input/output fields:

```ruby
actions: {
  send_message: {
    input_fields: lambda do |object_definitions|
      object_definitions['message_input']
    end,

    output_fields: lambda do |object_definitions|
      object_definitions['message_output']
    end
  }
}
```

### Composing Object Definitions

Combine multiple definitions:

```ruby
input_fields: lambda do |object_definitions|
  [
    { name: 'header', type: 'object', properties: object_definitions['header_fields'] }
  ].concat(object_definitions['body_fields'])
    .concat(object_definitions['config_fields'])
end
```

## Config Fields

### Purpose

`config_fields` appear at the top of action configuration and can trigger schema changes via `extends_schema`.

### Pattern: Mode Selector

```ruby
config_fields: [
  {
    name: 'model',
    optional: false,
    control_type: 'select',
    pick_list: 'model_list',
    hint: 'Select the model to use.'
  },
  {
    name: 'operation_mode',
    control_type: 'select',
    pick_list: 'operation_modes',
    optional: false,
    default: 'simple',
    extends_schema: true,          # Key: triggers input_fields refresh
    hint: 'Choose operation mode.'
  }
]
```

### Accessing Config Fields in Input Fields

```ruby
input_fields: lambda do |object_definitions|
  # config_fields available in object_definitions lambda
  object_definitions['dynamic_input']  # Uses config_fields internally
end

# In object_definitions:
dynamic_input: {
  fields: lambda do |_connection, config_fields, _object_definitions|
    mode = config_fields['operation_mode']
    # Return different fields based on mode
  end
}
```

## Methods Block

### Defining Methods

```ruby
methods: {
  build_request_body: lambda do |input|
    {
      'model' => input['model'],
      'messages' => input['messages'],
      'max_tokens' => input['max_tokens'] || 4096
    }
  end,

  parse_response: lambda do |response|
    {
      'id' => response['id'],
      'content' => response.dig('choices', 0, 'message', 'content')
    }
  end
}
```

### Calling Methods

Use `call('method_name', args)`:

```ruby
execute: lambda do |_connection, input|
  payload = call('build_request_body', input)

  response = post('v1/messages', payload)

  call('parse_response', response)
end
```

### Method for Reusable Field Definitions

```ruby
methods: {
  get_content_block_properties: lambda do
    [
      {
        name: 'block_type',
        label: 'Content type',
        control_type: 'select',
        pick_list: 'content_types',
        optional: false,
        extends_schema: true
      },
      {
        name: 'text',
        type: 'string',
        control_type: 'text-area',
        ngIf: 'input.block_type == "text"'
      },
      {
        name: 'image_url',
        type: 'string',
        ngIf: 'input.block_type == "image"'
      }
    ]
  end
}
```

Use in object definitions:

```ruby
object_definitions: {
  message_with_content: {
    fields: lambda do |_connection, _config_fields, _object_definitions|
      content_props = call('get_content_block_properties')

      [
        {
          name: 'content_blocks',
          type: 'array',
          of: 'object',
          list_mode: 'static',
          properties: content_props
        }
      ]
    end
  }
}
```

## Pick Lists

### Static Pick Lists

```ruby
pick_lists: {
  roles: lambda do
    [
      ['User', 'user'],
      ['Assistant', 'assistant'],
      ['System', 'system']
    ]
  end,

  content_types: lambda do
    [
      ['Text', 'text'],
      ['Image', 'image'],
      ['Document', 'document']
    ]
  end
}
```

### Dynamic Pick Lists (API-Driven)

```ruby
pick_lists: {
  model_list: lambda do
    response = get('v1/models')

    response['data']&.map do |model|
      [model['display_name'], model['id']]
    end || []
  end,

  workspace_list: lambda do |connection|
    get('v1/workspaces').map do |ws|
      [ws['name'], ws['id']]
    end
  end
}
```

### Pick List with Connection Parameter

```ruby
pick_lists: {
  projects: lambda do |connection|
    # connection hash available for API calls
    get('v1/projects',
      headers: { 'X-Workspace' => connection['workspace_id'] }
    ).map { |p| [p['name'], p['id']] }
  end
}
```

## ngIf Expressions

### Basic Syntax

```ruby
ngIf: 'input.field_name == "value"'
```

### Nested Fields

```ruby
ngIf: 'input.parent.child == "value"'
ngIf: 'input.settings.advanced_mode == true'
```

### Compound Conditions

```ruby
ngIf: 'input.type == "custom" && input.format == "json"'
ngIf: 'input.source == "url" || input.source == "file"'
```

### With Arrays (Item Context)

Inside array item properties, `input` refers to the item:

```ruby
{
  name: 'messages',
  type: 'array',
  of: 'object',
  properties: [
    { name: 'type', control_type: 'select', pick_list: 'message_types' },
    {
      name: 'text',
      ngIf: 'input.type == "text"'  # input = current array item
    }
  ]
}
```

## extends_schema Pattern

### How It Works

1. User changes field with `extends_schema: true`
2. Workato re-evaluates `input_fields` lambda
3. `config_fields` contains new value
4. Schema updates to show/hide relevant fields

### Example Flow

```ruby
config_fields: [
  {
    name: 'auth_type',
    control_type: 'select',
    options: [['API Key', 'api_key'], ['OAuth', 'oauth']],
    extends_schema: true,
    default: 'api_key'
  }
],

input_fields: lambda do |object_definitions|
  object_definitions['auth_fields']
end

# In object_definitions:
auth_fields: {
  fields: lambda do |_connection, config_fields, _object_definitions|
    case config_fields['auth_type']
    when 'api_key'
      [{ name: 'api_key', control_type: 'password', sticky: true }]
    when 'oauth'
      [
        { name: 'client_id', sticky: true },
        { name: 'client_secret', control_type: 'password', sticky: true }
      ]
    else
      []
    end
  end
}
```

## Output Fields Pattern

### Static Output

```ruby
output_fields: lambda do |_object_definitions|
  [
    { name: 'id', label: 'Record ID' },
    { name: 'status', label: 'Status' },
    { name: 'created_at', label: 'Created at', type: 'timestamp' }
  ]
end
```

### Dynamic Output Based on Config

```ruby
output_fields: lambda do |object_definitions|
  object_definitions['dynamic_output']
end

# In object_definitions:
dynamic_output: {
  fields: lambda do |_connection, config_fields, _object_definitions|
    base_fields = [
      { name: 'id' },
      { name: 'status' }
    ]

    if config_fields['include_metadata'] == true
      base_fields + [
        { name: 'metadata', type: 'object' },
        { name: 'timestamps', type: 'object' }
      ]
    else
      base_fields
    end
  end
}
```

### Nested Object Output

```ruby
output_fields: lambda do |_object_definitions|
  [
    { name: 'id' },
    { name: 'user', type: 'object', properties: [
      { name: 'id' },
      { name: 'name' },
      { name: 'email' }
    ]},
    { name: 'items', type: 'array', of: 'object', properties: [
      { name: 'product_id' },
      { name: 'quantity', type: 'integer' }
    ]}
  ]
end
```

## Sample Output

Provide example output for Workato's datapill display:

```ruby
sample_output: lambda do |_connection, _input|
  {
    id: 'rec_123abc',
    status: 'success',
    user: {
      id: 'usr_456def',
      name: 'John Doe',
      email: 'john@example.com'
    },
    items: [
      { product_id: 'prod_1', quantity: 2 },
      { product_id: 'prod_2', quantity: 1 }
    ]
  }
end
```

**Purpose:** Workato uses this to show datapill names and structure before the action runs.
