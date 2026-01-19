---
name: Workato SDK Authentication
description: This skill should be used when the user asks about "connector authentication", "oauth workato", "api key auth", "jwt authentication", "aws auth connector", "basic auth connector", "multi_auth", "connection block", or needs to implement authentication for a Workato custom connector.
version: 0.1.0
---

# Workato SDK Authentication

Guide for implementing authentication in Workato custom connectors. Covers all supported auth types and the connection block structure.

## Overview

Authentication in Workato connectors is defined in the `connection:` block. The connector must:
1. Define input fields for credentials
2. Specify the authorization type
3. Implement credential application to requests
4. Optionally test the connection

## Connection Block Structure

```ruby
connection: {
  fields: [
    # Credential input fields
  ],

  authorization: {
    type: 'auth_type',
    # Auth-specific configuration
  },

  base_uri: lambda do |connection|
    "https://#{connection['subdomain']}.api.example.com"
  end,

  test: lambda do |connection|
    get('/me')
  end
}
```

## Authentication Types

### Basic Authentication

Username and password sent as Base64-encoded header.

```ruby
connection: {
  fields: [
    { name: 'username', optional: false },
    { name: 'password', optional: false, control_type: 'password' }
  ],

  authorization: {
    type: 'basic_auth',
    credentials: lambda do |connection|
      user(connection['username'])
      password(connection['password'])
    end
  }
}
```

### API Key Authentication

API key sent as header or query parameter.

```ruby
connection: {
  fields: [
    { name: 'api_key', label: 'API Key', optional: false, control_type: 'password' }
  ],

  authorization: {
    type: 'api_key',
    apply: lambda do |connection|
      headers('Authorization' => "Bearer #{connection['api_key']}")
      # Or as query param:
      # params(api_key: connection['api_key'])
    end
  }
}
```

### Header Authentication

Custom headers for authentication.

```ruby
connection: {
  fields: [
    { name: 'api_key', control_type: 'password' },
    { name: 'api_secret', control_type: 'password' }
  ],

  authorization: {
    type: 'custom_auth',
    apply: lambda do |connection|
      headers(
        'X-API-Key' => connection['api_key'],
        'X-API-Secret' => connection['api_secret']
      )
    end
  }
}
```

### OAuth 2.0 - Authorization Code

Standard OAuth 2.0 flow with user authorization.

```ruby
connection: {
  fields: [
    { name: 'client_id', optional: false },
    { name: 'client_secret', optional: false, control_type: 'password' }
  ],

  authorization: {
    type: 'oauth2',

    authorization_url: lambda do |connection|
      "https://example.com/oauth/authorize?client_id=#{connection['client_id']}&response_type=code"
    end,

    token_url: lambda do
      'https://example.com/oauth/token'
    end,

    client_id: lambda do |connection|
      connection['client_id']
    end,

    client_secret: lambda do |connection|
      connection['client_secret']
    end,

    acquire: lambda do |connection, auth_code, redirect_uri|
      response = post('https://example.com/oauth/token')
        .payload(
          grant_type: 'authorization_code',
          code: auth_code,
          redirect_uri: redirect_uri,
          client_id: connection['client_id'],
          client_secret: connection['client_secret']
        )
        .request_format_www_form_urlencoded

      {
        access_token: response['access_token'],
        refresh_token: response['refresh_token'],
        token_expires_at: Time.now + response['expires_in'].to_i
      }
    end,

    refresh: lambda do |connection, refresh_token|
      response = post('https://example.com/oauth/token')
        .payload(
          grant_type: 'refresh_token',
          refresh_token: refresh_token,
          client_id: connection['client_id'],
          client_secret: connection['client_secret']
        )
        .request_format_www_form_urlencoded

      {
        access_token: response['access_token'],
        refresh_token: response['refresh_token'] || refresh_token
      }
    end,

    apply: lambda do |connection, access_token|
      headers('Authorization' => "Bearer #{access_token}")
    end
  }
}
```

### OAuth 2.0 - Client Credentials

Server-to-server OAuth without user interaction.

```ruby
authorization: {
  type: 'oauth2',

  token_url: lambda do
    'https://example.com/oauth/token'
  end,

  client_id: lambda do |connection|
    connection['client_id']
  end,

  client_secret: lambda do |connection|
    connection['client_secret']
  end,

  acquire: lambda do |connection|
    response = post('https://example.com/oauth/token')
      .payload(
        grant_type: 'client_credentials',
        client_id: connection['client_id'],
        client_secret: connection['client_secret']
      )
      .request_format_www_form_urlencoded

    { access_token: response['access_token'] }
  end,

  apply: lambda do |connection, access_token|
    headers('Authorization' => "Bearer #{access_token}")
  end
}
```

### JWT Authentication

JSON Web Token for service accounts.

```ruby
connection: {
  fields: [
    { name: 'private_key', control_type: 'text-area', optional: false },
    { name: 'service_account_email', optional: false }
  ],

  authorization: {
    type: 'custom_auth',

    acquire: lambda do |connection|
      jwt_header = { alg: 'RS256', typ: 'JWT' }
      jwt_payload = {
        iss: connection['service_account_email'],
        scope: 'https://example.com/api',
        aud: 'https://example.com/oauth/token',
        iat: Time.now.to_i,
        exp: Time.now.to_i + 3600
      }

      jwt = workato.jwt_encode(jwt_payload, connection['private_key'], 'RS256')

      response = post('https://example.com/oauth/token')
        .payload(grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: jwt)
        .request_format_www_form_urlencoded

      { access_token: response['access_token'] }
    end,

    apply: lambda do |connection, access_token|
      headers('Authorization' => "Bearer #{access_token}")
    end
  }
}
```

### AWS Signature Authentication

For AWS services using Signature Version 4.

```ruby
connection: {
  fields: [
    { name: 'access_key_id', optional: false },
    { name: 'secret_access_key', optional: false, control_type: 'password' },
    { name: 'region', optional: false, default: 'us-east-1' }
  ],

  authorization: {
    type: 'aws_auth',
    credentials: lambda do |connection|
      access_key_id(connection['access_key_id'])
      secret_access_key(connection['secret_access_key'])
      region(connection['region'])
      service('execute-api')  # or 's3', 'dynamodb', etc.
    end
  }
}
```

### Multi-Auth (Multiple Auth Options)

Allow users to choose between auth methods.

```ruby
connection: {
  fields: [
    {
      name: 'auth_type',
      control_type: 'select',
      options: [['API Key', 'api_key'], ['OAuth 2.0', 'oauth2']],
      optional: false
    },
    { name: 'api_key', ngIf: 'input.auth_type == "api_key"', control_type: 'password' },
    { name: 'client_id', ngIf: 'input.auth_type == "oauth2"' },
    { name: 'client_secret', ngIf: 'input.auth_type == "oauth2"', control_type: 'password' }
  ],

  authorization: {
    type: 'multi',

    selected: lambda do |connection|
      connection['auth_type']
    end,

    options: {
      api_key: {
        type: 'api_key',
        apply: lambda do |connection|
          headers('Authorization' => "Bearer #{connection['api_key']}")
        end
      },
      oauth2: {
        type: 'oauth2',
        # ... OAuth configuration
      }
    }
  }
}
```

## Connection Testing

Always implement a test to validate credentials:

```ruby
connection: {
  # ... fields and authorization ...

  test: lambda do |connection|
    get('/api/v1/me')  # Lightweight endpoint to verify auth
  end
}
```

## Common Patterns

### Dynamic Base URI

```ruby
base_uri: lambda do |connection|
  if connection['environment'] == 'sandbox'
    'https://sandbox.api.example.com'
  else
    'https://api.example.com'
  end
end
```

### Token Refresh Detection

```ruby
detect_on: [401, /token.*expired/i],

refresh_on: [401, /token.*expired/i]
```

## Reference Files

For detailed documentation on each auth type:

### Auth Type Guides
- **`references/guides__authentication.md`** - Authentication overview
- **`references/guides__authentication__basic-authentication.md`** - Basic auth
- **`references/guides__authentication__api-key.md`** - API key auth
- **`references/guides__authentication__header-auth.md`** - Header auth
- **`references/guides__authentication__jwt.md`** - JWT authentication
- **`references/guides__authentication__aws_auth.md`** - AWS Signature auth
- **`references/guides__authentication__on-prem.md`** - On-premise agents
- **`references/guides__authentication__multi_auth.md`** - Multiple auth options

### OAuth 2.0 Guides
- **`references/guides__authentication__oauth__auth-code.md`** - Authorization code flow
- **`references/guides__authentication__oauth__auth-code-pkce.md`** - Auth code with PKCE
- **`references/guides__authentication__oauth__client-credentials.md`** - Client credentials
- **`references/guides__authentication__oauth__ropc.md`** - Resource owner password
