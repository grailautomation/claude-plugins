# Formatter Patterns Reference

Output format conventions and implementation patterns.

## Formatter Architecture

Each formatter is a pure function that takes an `APIDocumentation` model and returns a formatted string.

```python
def format_as_X(doc: APIDocumentation) -> str:
    """Convert documentation to X format."""
    # Transform model to output
    return output_string
```

## JSON Formatter

The simplest formatter - just serialize the Pydantic model.

```python
def format_as_json(doc: APIDocumentation) -> str:
    """Convert to JSON with nice formatting."""
    return doc.model_dump_json(indent=2)
```

### Output Structure

```json
{
  "metadata": {
    "source_url": "https://example.com/api/users",
    "scraped_at": "2024-01-15T10:30:00",
    "title": "Users API",
    "section_id": "users",
    "section_name": "Users"
  },
  "authentication": {
    "type": "Bearer token",
    "header": "Authorization",
    "description": "All requests require Bearer token"
  },
  "rate_limits": {
    "default": "1000 requests per minute"
  },
  "endpoints": [
    {
      "method": "GET",
      "path": "/api/users",
      "description": "List all users",
      "parameters": [...],
      "examples": [...]
    }
  ]
}
```

## Markdown Formatter

Generate human-readable documentation.

### Template Structure

```python
def format_as_markdown(doc: APIDocumentation) -> str:
    lines = []

    # Title
    lines.append(f"# {doc.metadata.title}")
    lines.append("")

    # Authentication
    lines.append("## Authentication")
    lines.append(f"**Type:** {doc.authentication.type}")
    lines.append(f"**Header:** `{doc.authentication.header}`")
    lines.append("")

    # Endpoints
    lines.append("## Endpoints")
    lines.append("")

    for ep in doc.endpoints:
        lines.extend(_format_endpoint(ep))

    return "\n".join(lines)

def _format_endpoint(ep: Endpoint) -> list[str]:
    lines = []

    # Heading
    lines.append(f"### {ep.method} {ep.path}")
    lines.append("")

    # Description
    if ep.description:
        lines.append(ep.description)
        lines.append("")

    # Parameters
    if ep.parameters:
        lines.append("**Parameters:**")
        lines.append("")
        lines.append("| Name | Type | Required | Description |")
        lines.append("|------|------|----------|-------------|")
        for p in ep.parameters:
            req = "Yes" if p.required else "No"
            lines.append(f"| `{p.name}` | {p.type} | {req} | {p.description} |")
        lines.append("")

    # Examples
    for ex in ep.examples:
        if ex.title:
            lines.append(f"**{ex.title}:**")
        lines.append(f"```{ex.language}")
        lines.append(ex.code)
        lines.append("```")
        lines.append("")

    return lines
```

### Markdown Conventions

- Use fenced code blocks with language hints
- Use tables for parameters
- Use inline code for parameter names
- Include blank lines for readability
- Keep headings hierarchical (h1 → h2 → h3)

## OpenAPI Formatter

Generate valid OpenAPI 3.0.3 YAML specifications.

### Spec Structure

```python
def format_as_openapi(doc: APIDocumentation) -> str:
    spec = {
        "openapi": "3.0.3",
        "info": _build_info(doc),
        "servers": _build_servers(doc),
        "security": [{"bearerAuth": []}],
        "paths": _build_paths(doc),
        "components": _build_components(doc),
    }
    return yaml.dump(spec, sort_keys=False, allow_unicode=True)
```

### Info Section

```python
def _build_info(doc: APIDocumentation) -> dict:
    return {
        "title": doc.metadata.title,
        "description": f"Scraped from {doc.metadata.source_url}",
        "version": "1.0.0",
    }
```

### Servers Section

```python
def _build_servers(doc: APIDocumentation) -> list:
    # Example: Multiple data centers
    return [
        {"url": "https://www.workato.com", "description": "US Data Center"},
        {"url": "https://app.eu.workato.com", "description": "EU Data Center"},
    ]
```

### Paths Section

```python
def _build_paths(doc: APIDocumentation) -> dict:
    paths = {}

    for ep in doc.endpoints:
        # Convert path params from :id to {id}
        openapi_path = re.sub(r":(\w+)", r"{\1}", ep.path)

        if openapi_path not in paths:
            paths[openapi_path] = {}

        paths[openapi_path][ep.method.lower()] = _build_operation(ep)

    return paths

def _build_operation(ep: Endpoint) -> dict:
    op = {
        "summary": ep.description,
        "operationId": _generate_operation_id(ep),
        "responses": {"200": {"description": "Successful response"}},
    }

    # Add parameters
    if ep.parameters:
        op["parameters"] = [_build_parameter(p) for p in ep.parameters]

    # Add request body for POST/PUT/PATCH
    if ep.method in ["POST", "PUT", "PATCH"] and ep.request_body:
        op["requestBody"] = _build_request_body(ep.request_body)

    return op
```

### Operation ID Generation

```python
def _generate_operation_id(ep: Endpoint) -> str:
    """Generate clean operationId from method and path."""
    # /api/users/:id → users_id
    path_part = ep.path.replace("/api/", "").replace("/", "_")
    path_part = re.sub(r"[:{}\-]", "", path_part)

    # GET → get, POST → create
    method_map = {"GET": "get", "POST": "create", "PUT": "update",
                  "DELETE": "delete", "PATCH": "patch"}
    method = method_map.get(ep.method, ep.method.lower())

    # Combine: getUsers, createUser
    words = path_part.split("_")
    return method + "".join(w.title() for w in words if w)
```

### Parameter Conversion

```python
def _build_parameter(p: Parameter) -> dict:
    return {
        "name": p.name,
        "in": p.location,  # "query", "path", "header"
        "required": p.required or p.location == "path",
        "schema": {"type": _openapi_type(p.type)},
        "description": p.description,
    }

def _openapi_type(type_str: str) -> str:
    """Map documentation types to OpenAPI types."""
    mapping = {
        "string": "string",
        "integer": "integer",
        "int": "integer",
        "boolean": "boolean",
        "bool": "boolean",
        "array": "array",
        "object": "object",
        "number": "number",
        "float": "number",
    }
    return mapping.get(type_str.lower(), "string")
```

### Components Section

```python
def _build_components(doc: APIDocumentation) -> dict:
    return {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "description": doc.authentication.description,
            }
        }
    }
```

## YAML Best Practices

When generating YAML:

```python
import yaml

# Use safe_dump for security
yaml.safe_dump(data)

# Preserve order (Python 3.7+)
yaml.dump(data, sort_keys=False)

# Handle unicode properly
yaml.dump(data, allow_unicode=True)

# Use block style for readability
yaml.dump(data, default_flow_style=False)
```

## Validation

### OpenAPI Validation

Test generated specs with:

```bash
# Using openapi-generator-cli
npx @openapitools/openapi-generator-cli validate -i spec.yaml

# Using swagger-cli
npx swagger-cli validate spec.yaml
```

### Common Validation Errors

1. **Missing operationId** - Every operation needs unique ID
2. **Invalid path param** - Path params must be in path template
3. **Missing required fields** - Check info.title, info.version
4. **Invalid $ref** - Ensure all references resolve
