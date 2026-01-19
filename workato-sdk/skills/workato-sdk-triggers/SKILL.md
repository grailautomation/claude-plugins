---
name: Workato SDK Triggers
description: This skill should be used when the user asks about "build trigger", "webhook trigger", "poll trigger", "dynamic webhook", "static webhook", "hybrid trigger", "dedup", "trigger_limit", "closure", or needs to implement triggers for a Workato custom connector.
version: 0.1.0
---

# Workato SDK Triggers

Guide for building triggers in Workato custom connectors. Triggers start recipes when new data is available.

## Overview

Workato supports three trigger types:
1. **Poll triggers** - Periodically check for new records
2. **Webhook triggers** - Receive real-time push notifications
3. **Hybrid triggers** - Combine polling with webhooks

## Trigger Structure

```ruby
triggers: {
  new_record: {
    title: 'New record',
    subtitle: 'Triggers when a new record is created',

    description: lambda do |input, pick_list_label|
      "New <span class='provider'>#{pick_list_label['object_type'] || 'record'}</span>"
    end,

    input_fields: lambda do
      [
        { name: 'object_type', control_type: 'select', pick_list: 'object_types' }
      ]
    end,

    poll: lambda do |connection, input, closure|
      # Polling logic
    end,

    dedup: lambda do |record|
      record['id']
    end,

    output_fields: lambda do |object_definitions|
      object_definitions['record']
    end
  }
}
```

## Poll Triggers

Periodically fetch new records.

### Basic Poll Trigger

```ruby
new_record: {
  title: 'New record',

  input_fields: lambda do
    [{ name: 'since', type: 'date_time', optional: true }]
  end,

  poll: lambda do |connection, input, closure|
    # closure persists between polls
    since = closure || input['since'] || Time.now.iso8601

    records = get('/api/records')
      .params(created_after: since, order: 'created_at')['items']

    next_since = records.last&.[]('created_at') || since

    {
      events: records,
      next_poll: next_since,  # Stored in closure for next poll
      can_poll_more: records.size >= 100
    }
  end,

  dedup: lambda do |record|
    record['id']  # Unique identifier for deduplication
  end,

  output_fields: lambda do
    [
      { name: 'id' },
      { name: 'name' },
      { name: 'created_at', type: 'date_time' }
    ]
  end
}
```

### Closure Usage

The `closure` parameter persists state between polls:

```ruby
poll: lambda do |connection, input, closure|
  closure ||= { page_token: nil, since: input['since'] }

  response = get('/api/records').params(
    since: closure['since'],
    page_token: closure['page_token']
  )

  {
    events: response['items'],
    next_poll: {
      since: response['items'].last&.[]('created_at') || closure['since'],
      page_token: response['next_page_token']
    },
    can_poll_more: response['has_more']
  }
end
```

## Webhook Triggers

Receive real-time notifications from the API.

### Static Webhook

Webhook URL is fixed per connection:

```ruby
new_event_webhook: {
  title: 'New event (webhook)',

  webhook_subscribe: lambda do |connection, input, webhook_url|
    post('/api/webhooks').payload(
      url: webhook_url,
      events: ['record.created']
    )
  end,

  webhook_unsubscribe: lambda do |connection, webhook|
    delete("/api/webhooks/#{webhook['id']}")
  end,

  webhook_notification: lambda do |connection, input, payload|
    payload['data']  # Return the event data
  end,

  dedup: lambda do |event|
    event['id']
  end,

  output_fields: lambda do
    [{ name: 'id' }, { name: 'type' }, { name: 'data', type: 'object' }]
  end
}
```

### Dynamic Webhook

Webhook URL changes per recipe:

```ruby
new_event_dynamic: {
  title: 'New event (real-time)',

  webhook_subscribe: lambda do |connection, input, recipe_id, webhook_url|
    post('/api/webhooks').payload(
      url: webhook_url,
      events: input['event_types'],
      metadata: { recipe_id: recipe_id }
    )
  end,

  webhook_unsubscribe: lambda do |connection, webhook|
    delete("/api/webhooks/#{webhook['id']}")
  end,

  webhook_notification: lambda do |connection, input, payload, headers|
    # Verify webhook signature
    signature = headers['X-Webhook-Signature']
    expected = workato.hmac_sha256(payload.to_json, connection['webhook_secret'])

    error('Invalid signature') unless signature == expected

    payload['events']
  end,

  dedup: lambda do |event|
    event['event_id']
  end
}
```

## Hybrid Triggers

Combine polling for historical data with webhooks for real-time:

```ruby
new_record_hybrid: {
  title: 'New record (real-time)',

  # Poll for historical/missed records
  poll: lambda do |connection, input, closure|
    since = closure || input['since'] || Time.now.iso8601
    records = get('/api/records').params(created_after: since)['items']

    {
      events: records,
      next_poll: records.last&.[]('created_at') || since,
      can_poll_more: records.size >= 100
    }
  end,

  # Subscribe to webhook for real-time
  webhook_subscribe: lambda do |connection, input, recipe_id, webhook_url|
    post('/api/webhooks').payload(url: webhook_url, events: ['record.created'])
  end,

  webhook_unsubscribe: lambda do |connection, webhook|
    delete("/api/webhooks/#{webhook['id']}")
  end,

  webhook_notification: lambda do |connection, input, payload|
    [payload['record']]  # Return as array
  end,

  dedup: lambda do |record|
    record['id']
  end
}
```

## Deduplication

The `dedup` lambda returns a unique identifier to prevent duplicate processing:

```ruby
# Simple ID dedup
dedup: lambda do |record|
  record['id']
end

# Composite dedup
dedup: lambda do |record|
  "#{record['type']}_#{record['id']}_#{record['version']}"
end
```

## Webhook Security

### Signature Verification

```ruby
webhook_notification: lambda do |connection, input, payload, headers|
  # HMAC verification
  signature = headers['X-Signature']
  computed = workato.hmac_sha256(payload.to_json, connection['secret'])

  error('Invalid webhook signature') unless signature == computed

  payload['data']
end
```

### IP Allowlisting

Some APIs require allowlisting Workato's IPs. Refer to Workato documentation for current IP ranges.

## Trigger Limits

For APIs that don't track "since" timestamps:

```ruby
new_record: {
  poll: lambda do |connection, input, closure|
    records = get('/api/records').params(limit: 100)['items']

    {
      events: records.first(workato.trigger_limit || 100),
      can_poll_more: false
    }
  end
}
```

## Sample Output

Provide sample data for recipe building:

```ruby
sample_output: lambda do |connection, input|
  get('/api/records').params(limit: 1)['items'].first || {
    id: 'sample_123',
    name: 'Sample Record',
    created_at: Time.now.iso8601
  }
end
```

## Reference Files

For detailed documentation:

### Trigger Types
- **`references/guides__building-triggers.md`** - Triggers overview
- **`references/guides__building-triggers__poll.md`** - Poll trigger patterns
- **`references/guides__building-triggers__static-webhook.md`** - Static webhooks
- **`references/guides__building-triggers__dynamic-webhook.md`** - Dynamic webhooks
- **`references/guides__building-triggers__hybrid-triggers.md`** - Hybrid triggers

### Webhook Security
- **`references/guides__building-triggers__securing-webhooks.md`** - Webhook security

### Limits
- **`references/guides__trigger-limit.md`** - Trigger limits and quotas
