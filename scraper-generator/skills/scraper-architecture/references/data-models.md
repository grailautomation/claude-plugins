# Data Models Reference

Complete reference for Pydantic models used in API documentation scrapers.

## Core Model Hierarchy

```
APIDocumentation
├── metadata: Metadata
├── authentication: Authentication
├── rate_limits: dict[str, str]
└── endpoints: list[Endpoint]
    ├── parameters: list[Parameter]
    └── examples: list[Example]
```

## Model Definitions

### Parameter

Represents an API endpoint parameter (path, query, or body).

```python
class Parameter(BaseModel):
    name: str                    # Parameter name
    type: str = "string"         # Data type (string, integer, boolean, array, object)
    required: bool = False       # Whether parameter is required
    description: str = ""        # Human-readable description
    location: str = "query"      # Where param is passed: "query", "path", "body", "header"
```

**Type mappings:**
| Documentation | Python | OpenAPI |
|--------------|--------|---------|
| string | str | string |
| integer, int | int | integer |
| boolean, bool | bool | boolean |
| array | list | array |
| object | dict | object |
| number, float | float | number |

**Location determination:**
1. If param name appears in path template (`:id` or `{id}`), location is "path"
2. For GET/DELETE requests, typically "query"
3. For POST/PUT/PATCH requests, typically "body"
4. Auth params like `api_token` are often "header"

### Example

Represents a code example (request or response).

```python
class Example(BaseModel):
    title: str = ""          # Optional title/label
    code: str                # The code content
    language: str = "json"   # Code language (json, curl, ruby, python)
```

**Language detection:**
- Check `class="language-{lang}"` on code block
- Check `class="highlight-{lang}"` on container
- Infer from content (starts with `{` → json, starts with `curl` → curl)

### Endpoint

Represents a single API endpoint.

```python
class Endpoint(BaseModel):
    method: str                                    # HTTP method (GET, POST, etc.)
    path: str                                      # URL path with params (/api/users/:id)
    description: str = ""                          # What the endpoint does
    parameters: list[Parameter] = []               # All parameters
    request_body: dict[str, Any] | None = None    # Request body schema
    response: dict[str, Any] | None = None        # Response schema
    examples: list[Example] = []                   # Code examples
    rate_limit: str | None = None                 # Endpoint-specific rate limit
    notes: list[str] = []                         # Additional notes/warnings
```

**Method normalization:**
Always store uppercase: GET, POST, PUT, PATCH, DELETE

**Path normalization:**
- Keep parameter placeholders: `/api/users/:id` or `/api/users/{id}`
- Remove example values: `/api/users/123` → skip or infer template
- Ensure leading slash

### Authentication

Represents API authentication requirements.

```python
class Authentication(BaseModel):
    type: str = "Bearer token"           # Auth type
    header: str = "Authorization"        # Header name
    description: str = ""                # How to authenticate
```

**Common types:**
- Bearer token: `Authorization: Bearer <token>`
- API key: `X-API-Key: <key>` or query param
- Basic auth: `Authorization: Basic <base64>`
- OAuth: More complex, may need nested model

### Metadata

Captures scrape context for traceability.

```python
class Metadata(BaseModel):
    source_url: str                              # URL that was scraped
    scraped_at: datetime = datetime.now()        # When scraping occurred
    title: str = ""                              # Page/API title
    section_id: str = ""                         # Machine-readable section ID
    section_name: str = ""                       # Human-readable section name
```

### APIDocumentation

Top-level container for complete documentation.

```python
class APIDocumentation(BaseModel):
    metadata: Metadata
    authentication: Authentication
    rate_limits: dict[str, str] = {}     # name → limit description
    endpoints: list[Endpoint] = []
```

## Serialization

### To JSON

```python
doc.model_dump_json(indent=2)
```

### To Dictionary

```python
doc.model_dump()
```

### From Dictionary

```python
APIDocumentation.model_validate(data)
```

## Validation Patterns

### Required Field Check

```python
def validate_endpoint(ep: Endpoint) -> list[str]:
    issues = []
    if not ep.path.startswith("/"):
        issues.append("Path must start with /")
    if ep.method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
        issues.append(f"Invalid method: {ep.method}")
    return issues
```

### Completeness Check

```python
def check_completeness(doc: APIDocumentation) -> dict:
    stats = {
        "total_endpoints": len(doc.endpoints),
        "with_description": sum(1 for e in doc.endpoints if e.description),
        "with_parameters": sum(1 for e in doc.endpoints if e.parameters),
        "with_examples": sum(1 for e in doc.endpoints if e.examples),
    }
    return stats
```

## Extension Patterns

### Custom Fields

For API-specific data, extend the models:

```python
class WorkatoEndpoint(Endpoint):
    """Workato-specific endpoint with additional fields."""
    workspace_aware: bool = False
    admin_only: bool = False
```

### Nested Schemas

For complex request/response bodies:

```python
class SchemaField(BaseModel):
    name: str
    type: str
    required: bool = False
    description: str = ""
    nested: list["SchemaField"] = []

class RequestBody(BaseModel):
    content_type: str = "application/json"
    fields: list[SchemaField] = []
```
