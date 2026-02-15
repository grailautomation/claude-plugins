# Authentication

## AuthClient Setup

The `intuit-oauth` package provides the `AuthClient` used for OAuth 2.0 authentication with QuickBooks Online.

```python
from intuitlib.client import AuthClient

auth_client = AuthClient(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    access_token='YOUR_ACCESS_TOKEN',    # Optional — if omitted, client auto-refreshes
    environment='sandbox',                # 'sandbox' or 'production'
    redirect_uri='http://localhost:8000/callback',
)
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `client_id` | Yes | OAuth 2.0 client ID from Intuit Developer Portal |
| `client_secret` | Yes | OAuth 2.0 client secret |
| `access_token` | No | If not passed, the QuickBooks client calls refresh automatically |
| `environment` | Yes | `'sandbox'` for testing, `'production'` for live data |
| `redirect_uri` | Yes | Must match the URI registered in your Intuit app |

## QuickBooks Client

```python
from quickbooks import QuickBooks

client = QuickBooks(
    auth_client=auth_client,
    refresh_token='REFRESH_TOKEN',
    company_id='COMPANY_ID',
    minorversion=75,
)
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `auth_client` | Yes | An `AuthClient` instance |
| `refresh_token` | Yes | OAuth 2.0 refresh token for token renewal |
| `company_id` | Yes | The QBO company/realm ID |
| `minorversion` | Recommended | API minor version (default: 75, minimum supported) |
| `invoice_link` | No | Set `True` to get shareable invoice links |
| `verifier_token` | No | For webhook signature validation |
| `use_decimal` | No | Set `True` to parse JSON floats as `decimal.Decimal` |

### Minor Version Deprecation

As of the library's latest release, `minorversion` defaults to 75 (the minimum supported version). If you don't specify it, you'll get a `DeprecationWarning`:

```
No minor version specified. Defaulting to minimum supported version (75).
Please specify minorversion explicitly when initializing QuickBooks.
```

If you specify a version below 75, you'll also get a warning. See: https://blogs.intuit.com/2025/01/21/changes-to-our-accounting-api-that-may-impact-your-application/

## Environment Setup Pattern

Recommended pattern using environment variables:

```python
import os
from intuitlib.client import AuthClient
from quickbooks import QuickBooks

auth_client = AuthClient(
    client_id=os.environ['QBO_CLIENT_ID'],
    client_secret=os.environ['QBO_CLIENT_SECRET'],
    access_token=os.environ.get('QBO_ACCESS_TOKEN'),
    environment=os.environ.get('QBO_ENVIRONMENT', 'sandbox'),
    redirect_uri=os.environ.get('QBO_REDIRECT_URI', 'http://localhost:8000/callback'),
)

client = QuickBooks(
    auth_client=auth_client,
    refresh_token=os.environ['QBO_REFRESH_TOKEN'],
    company_id=os.environ['QBO_COMPANY_ID'],
    minorversion=int(os.environ.get('QBO_MINOR_VERSION', '75')),
)
```

## Sandbox vs Production

The client automatically selects the correct API URL based on the AuthClient environment:

| Environment | API Base URL |
|-------------|-------------|
| `sandbox` | `https://sandbox-quickbooks.api.intuit.com/v3` |
| `production` | `https://quickbooks.api.intuit.com/v3` |

## Token Refresh

If no `access_token` is passed to `AuthClient`, the QuickBooks client automatically calls `auth_client.refresh()` during session initialization. The refreshed token is stored on the client instance:

```python
# After client initialization, the refresh token may have been updated
new_refresh_token = client.refresh_token
# Persist this for next session
```

## Token Lifecycle

**Critical**: You must understand these expiry rules to avoid production outages.

| Token | Lifetime | Notes |
|-------|----------|-------|
| Access token | 60 minutes | Used for API calls |
| Refresh token | 100 days | **Single-use** — each refresh invalidates the old token |

**The library does NOT auto-refresh during a session.** `_start_session()` refreshes once at client init (if `access_token` is None). If the access token expires mid-session, the next API call raises `AuthorizationException` with no retry. Your code must handle this.

**Persistence pattern**: After every client initialization that triggers a refresh, persist the new refresh token immediately. If you lose the new refresh token, the old one is already invalidated and you'll need the user to re-authorize.

```python
client = QuickBooks(
    auth_client=auth_client,
    refresh_token=load_refresh_token(),  # Load from DB/vault
    company_id='COMPANY_ID',
    minorversion=75,
)

# Persist the (possibly updated) refresh token immediately
save_refresh_token(client.refresh_token)
```

## Singleton vs Multi-Instance

By default, each `QuickBooks()` call creates a new instance. For singleton behavior:

```python
# Enable global singleton — must use mangled name
QuickBooks._QuickBooks__use_global = True

# First call creates the instance
client = QuickBooks(auth_client=auth_client, refresh_token='...', company_id='...')

# Subsequent calls return the same instance
same_client = QuickBooks()

# Reset the singleton
client._drop()
```

**Warning**: `__use_global` is a double-underscore attribute, so Python name-mangles it to `_QuickBooks__use_global`. Writing `QuickBooks.__use_global = True` silently creates a new class attribute and the singleton logic never sees it. Always use the mangled form.

**Warning**: Singleton mode shares state across all code using `QuickBooks()`. Avoid in multi-tenant applications.
