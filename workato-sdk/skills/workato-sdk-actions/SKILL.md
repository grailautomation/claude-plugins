---
name: Workato SDK Actions
description: This skill should be used when the user asks about "build action", "create action", "execute block", "input_fields", "output_fields", "streaming action", "multistep action", "config_fields", "wait for resume", or needs to implement actions for a Workato custom connector.
version: 0.1.0
---

# Workato SDK Actions

Guide for building actions in Workato custom connectors. Actions are operations that send data to or retrieve data from an API.

## Overview

Actions in Workato connectors:
- Receive input from recipe datapills
- Execute API requests
- Return output as datapills for subsequent steps

## Action Structure

```ruby
actions: {
  create_record: {
    title: 'Create record',
    subtitle: 'Create a new record in the system',

    description: lambda do |input, pick_list_label|
      "Create a new <span class='provider'>#{pick_list_label['object_type'] || 'record'}</span>"
    end,

    help: 'Creates a new record with the specified fields.',

    input_fields: lambda do |object_definitions|
      object_definitions['record_input']
    end,

    execute: lambda do |connection, input|
      post('/api/records')
        .payload(input)
        .after_error_response(/.*/) do |_, body, _, message|
          error("#{message}: #{body}")
        end
    end,

    output_fields: lambda do |object_definitions|
      object_definitions['record_output']
    end,

    sample_output: lambda do |connection, input|
      get('/api/records/sample')
    end
  }
}
```

## Key Components

### input_fields

Define what data the action accepts:

```ruby
input_fields: lambda do |object_definitions|
  [
    { name: 'name', label: 'Record Name', optional: false },
    { name: 'email', label: 'Email Address', control_type: 'email' },
    { name: 'amount', type: 'number', control_type: 'number' },
    { name: 'active', type: 'boolean', control_type: 'checkbox' }
  ]
end
```

### execute

The main logic that runs when the action executes:

```ruby
execute: lambda do |connection, input|
  response = post('/api/records')
    .payload(
      name: input['name'],
      email: input['email'],
      metadata: { source: 'workato' }
    )

  { id: response['id'], created_at: response['created_at'] }
end
```

### output_fields

Define the datapills available after execution:

```ruby
output_fields: lambda do |object_definitions|
  [
    { name: 'id', label: 'Record ID' },
    { name: 'created_at', label: 'Created At', type: 'date_time' }
  ]
end
```

## config_fields

Dynamic fields that change the action's behavior:

```ruby
config_fields: [
  {
    name: 'object_type',
    label: 'Object Type',
    control_type: 'select',
    pick_list: 'object_types',
    optional: false,
    extends_schema: true  # Refresh schema when changed
  }
],

input_fields: lambda do |object_definitions, connection, config_fields|
  case config_fields['object_type']
  when 'contact'
    [{ name: 'email', optional: false }, { name: 'phone' }]
  when 'company'
    [{ name: 'company_name', optional: false }, { name: 'industry' }]
  end
end
```

## Common Action Patterns

### Get Record by ID

```ruby
get_record: {
  title: 'Get record',

  input_fields: lambda do
    [{ name: 'id', label: 'Record ID', optional: false }]
  end,

  execute: lambda do |connection, input|
    get("/api/records/#{input['id']}")
  end,

  output_fields: lambda do |object_definitions|
    object_definitions['record']
  end
}
```

### Search Records

```ruby
search_records: {
  title: 'Search records',

  input_fields: lambda do
    [
      { name: 'query', label: 'Search Query' },
      { name: 'limit', type: 'integer', default: 100 }
    ]
  end,

  execute: lambda do |connection, input|
    { records: get('/api/records').params(q: input['query'], limit: input['limit'])['items'] }
  end,

  output_fields: lambda do
    [{ name: 'records', type: 'array', of: 'object', properties: [...] }]
  end
}
```

### Create Record

```ruby
create_record: {
  title: 'Create record',

  input_fields: lambda do |object_definitions|
    object_definitions['record_input']
  end,

  execute: lambda do |connection, input|
    post('/api/records').payload(input)
  end,

  output_fields: lambda do |object_definitions|
    object_definitions['record']
  end
}
```

### Update Record

```ruby
update_record: {
  title: 'Update record',

  input_fields: lambda do |object_definitions|
    [{ name: 'id', optional: false }] + object_definitions['record_input']
  end,

  execute: lambda do |connection, input|
    id = input.delete('id')
    patch("/api/records/#{id}").payload(input)
  end,

  output_fields: lambda do |object_definitions|
    object_definitions['record']
  end
}
```

## Multistep Actions

Actions that require multiple API calls:

```ruby
execute: lambda do |connection, input, eis, eos, continue|
  if continue.blank?
    # First step: initiate
    job = post('/api/jobs').payload(input)
    { job_id: job['id'] }
  elsif continue['status'] == 'pending'
    # Poll for completion
    job = get("/api/jobs/#{continue['job_id']}")
    if job['status'] == 'complete'
      { result: job['result'] }
    else
      { reinvoke_after: 30, continue: { job_id: continue['job_id'], status: 'pending' } }
    end
  end
end
```

## Streaming Actions

### Download Streaming

For downloading large files:

```ruby
execute: lambda do |connection, input|
  workato.stream.out('download_stream', { file_id: input['file_id'] })
end,

streams: {
  download_stream: {
    input_fields: lambda { [{ name: 'file_id' }] },

    read: lambda do |connection, input, byte_offset|
      get("/api/files/#{input['file_id']}/content")
        .headers('Range' => "bytes=#{byte_offset}-")
        .response_format_raw
    end
  }
}
```

### Upload Streaming

For uploading large files:

```ruby
execute: lambda do |connection, input|
  workato.stream.in(input['file_content']) do |chunk, byte_offset, eof|
    if byte_offset == 0
      # Initialize upload
      session = post('/api/uploads/init').payload(filename: input['filename'])
      { upload_id: session['id'], byte_offset: 0 }
    else
      # Upload chunk
      put("/api/uploads/#{chunk['upload_id']}/chunks")
        .payload(chunk)
        .headers('Content-Range' => "bytes #{byte_offset}-#{byte_offset + chunk.size - 1}/*")
    end
  end
end
```

## Wait for Resume Actions

Actions that pause and wait for external callback:

```ruby
execute: lambda do |connection, input, eis, eos, continue, resume_data|
  if continue.blank?
    # Start process and return resume URL
    { wait_for_resume: { resume_url: workato.resume_url } }
  elsif resume_data.present?
    # Resume after callback received
    { result: resume_data }
  end
end
```

## Error Handling

```ruby
execute: lambda do |connection, input|
  post('/api/records')
    .payload(input)
    .after_error_response(/4\d{2}/) do |code, body, headers, message|
      error("API Error (#{code}): #{body['error']}")
    end
end
```

## Reference Files

For detailed documentation:

### Building Actions
- **`references/guides__building-actions.md`** - Actions overview
- **`references/guides__building-actions__create-objects.md`** - Create patterns
- **`references/guides__building-actions__get-objects.md`** - Get/search patterns
- **`references/guides__building-actions__update-objects.md`** - Update patterns
- **`references/guides__building-actions__custom-action.md`** - Custom action support
- **`references/guides__building-actions__multistep-actions.md`** - Multistep actions
- **`references/guides__building-actions__multi-threaded-actions.md`** - Multi-threaded
- **`references/guides__building-actions__wait-for-resume-actions.md`** - Wait for resume

### Streaming
- **`references/guides__building-actions__streaming.md`** - Streaming overview
- **`references/guides__building-actions__streaming__download-stream.md`** - Download streaming
- **`references/guides__building-actions__streaming__upload-stream-chunk-id.md`** - Upload with chunk ID
- **`references/guides__building-actions__streaming__upload-stream-content-range.md`** - Upload with content range

### Input Fields
- **`references/guides__config_fields.md`** - Config fields and dynamic schemas
