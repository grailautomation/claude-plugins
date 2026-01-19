---
name: Workato SDK Data Formats
description: This skill should be used when the user asks about "request_format", "response_format", "xml format workato", "json format workato", "multipart form", "form-url-encoded", "parse xml", "build xml", or needs to handle different data formats in a Workato connector.
version: 0.1.0
---

# Workato SDK Data Formats

Guide for handling different request and response formats in Workato custom connectors.

## Overview

Workato connectors support multiple data formats:
- **JSON** (default) - Most common API format
- **XML** - SOAP and legacy APIs
- **Form URL-encoded** - OAuth and simple forms
- **Multipart form** - File uploads

## Request Formats

### JSON (Default)

JSON is the default format. No special configuration needed:

```ruby
execute: lambda do |connection, input|
  post('/api/records')
    .payload(
      name: input['name'],
      email: input['email']
    )
  # Automatically sends Content-Type: application/json
end
```

### Form URL-Encoded

For OAuth token exchanges and simple form submissions:

```ruby
execute: lambda do |connection, input|
  post('/oauth/token')
    .payload(
      grant_type: 'authorization_code',
      code: input['code'],
      redirect_uri: input['redirect_uri']
    )
    .request_format_www_form_urlencoded
  # Sends Content-Type: application/x-www-form-urlencoded
end
```

### Multipart Form

For file uploads:

```ruby
execute: lambda do |connection, input|
  post('/api/files')
    .payload(
      file: input['file_content'],
      filename: input['filename'],
      description: input['description']
    )
    .request_format_multipart_form
  # Sends Content-Type: multipart/form-data
end
```

### XML

For SOAP and XML-based APIs:

```ruby
execute: lambda do |connection, input|
  post('/api/records')
    .payload(
      'Record' => {
        '@xmlns' => 'http://example.com/schema',
        'Name' => input['name'],
        'Email' => input['email']
      }
    )
    .request_format_xml
  # Sends Content-Type: application/xml
end
```

## Response Formats

### JSON Response (Default)

Responses are automatically parsed as JSON:

```ruby
execute: lambda do |connection, input|
  response = get('/api/records/123')
  # response is already a Hash
  { id: response['id'], name: response['name'] }
end
```

### XML Response

Parse XML responses:

```ruby
execute: lambda do |connection, input|
  response = get('/api/records/123')
    .response_format_xml

  # Access XML elements
  {
    id: response.dig('Record', 'Id'),
    name: response.dig('Record', 'Name')
  }
end
```

### Raw Response

For binary data or custom parsing:

```ruby
execute: lambda do |connection, input|
  content = get("/api/files/#{input['id']}/download")
    .response_format_raw

  { file_content: content }
end
```

## XML Specifics

### Building XML Payloads

Use hashes with special keys:

```ruby
payload = {
  'Envelope' => {
    '@xmlns:soap' => 'http://schemas.xmlsoap.org/soap/envelope/',
    'Body' => {
      'CreateRecord' => {
        '@xmlns' => 'http://example.com/api',
        'Name' => 'Test',
        'Items' => {
          'Item' => [
            { 'Value' => 'A' },
            { 'Value' => 'B' }
          ]
        }
      }
    }
  }
}
```

Produces:
```xml
<Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <CreateRecord xmlns="http://example.com/api">
      <Name>Test</Name>
      <Items>
        <Item><Value>A</Value></Item>
        <Item><Value>B</Value></Item>
      </Items>
    </CreateRecord>
  </Body>
</Envelope>
```

### XML Attributes

Prefix attribute keys with `@`:

```ruby
{
  'Record' => {
    '@id' => '123',           # Attribute
    '@type' => 'contact',     # Attribute
    'Name' => 'John'          # Element
  }
}
```

Produces:
```xml
<Record id="123" type="contact">
  <Name>John</Name>
</Record>
```

### XML Namespaces

Define namespaces with `@xmlns`:

```ruby
{
  'soap:Envelope' => {
    '@xmlns:soap' => 'http://schemas.xmlsoap.org/soap/envelope/',
    '@xmlns:api' => 'http://example.com/api',
    'soap:Body' => {
      'api:GetRecord' => {
        'api:Id' => '123'
      }
    }
  }
}
```

### Parsing XML Responses

Navigate with `dig`:

```ruby
response = get('/api/record')
  .response_format_xml

# Access nested elements
name = response.dig('Envelope', 'Body', 'GetRecordResponse', 'Record', 'Name')

# Access attributes
id = response.dig('Envelope', 'Body', 'GetRecordResponse', 'Record', '@id')

# Handle arrays
items = response.dig('Envelope', 'Body', 'GetRecordResponse', 'Items', 'Item')
items = [items] unless items.is_a?(Array)  # Ensure array
```

## Multipart Form Details

### File Upload with Metadata

```ruby
execute: lambda do |connection, input|
  post('/api/upload')
    .payload(
      file: [
        input['file_content'],
        'application/octet-stream',     # Content type
        input['filename']               # Filename
      ],
      metadata: input['metadata'].to_json
    )
    .request_format_multipart_form
end
```

### Multiple Files

```ruby
execute: lambda do |connection, input|
  files = input['files'].map do |file|
    ['files[]', [file['content'], file['content_type'], file['name']]]
  end

  post('/api/upload')
    .payload(Hash[files])
    .request_format_multipart_form
end
```

## Content Type Headers

Override content type when needed:

```ruby
execute: lambda do |connection, input|
  post('/api/data')
    .payload(input['raw_data'])
    .headers('Content-Type' => 'text/plain')
end
```

## Combining Formats

Different request and response formats:

```ruby
execute: lambda do |connection, input|
  # Send form-encoded, receive JSON
  response = post('/oauth/token')
    .payload(grant_type: 'client_credentials')
    .request_format_www_form_urlencoded
    # Response is JSON by default

  { access_token: response['access_token'] }
end
```

## Reference Files

For detailed documentation:

- **`references/guides__data-formats.md`** - Data formats overview
- **`references/guides__data-formats__json-format.md`** - JSON format details
- **`references/guides__data-formats__xml-format.md`** - XML format details
- **`references/guides__data-formats__form-url-encoded.md`** - Form URL-encoded
- **`references/guides__data-formats__request_format_multipart_form.md`** - Multipart form uploads
