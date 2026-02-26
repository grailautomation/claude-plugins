---
name: openapi-spec-generation
version: 0.1.0
user-invocable: true
description: >-
  This skill should be used when the user asks to "generate an OpenAPI spec",
  "create API documentation", "generate an SDK from a spec", "validate an API
  spec", "lint an OpenAPI file", "design an API contract", or when building,
  maintaining, or validating RESTful API specifications using OpenAPI 3.1.
---

# OpenAPI Spec Generation

Patterns for creating, maintaining, and validating OpenAPI 3.1 specifications for RESTful APIs.

## When to Activate

- Creating API documentation from scratch
- Generating OpenAPI specs from existing code
- Designing API contracts (design-first approach)
- Validating API implementations against specs
- Generating client SDKs from specs
- Setting up API documentation portals

## Core Concepts

### OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### Design Approaches

| Approach | Description | Best For |
|----------|-------------|----------|
| **Design-First** | Write spec before code | New APIs, contracts |
| **Code-First** | Generate spec from code | Existing APIs |
| **Hybrid** | Annotate code, generate spec | Evolving APIs |

## Templates

Available in `references/`:

- **Complete Spec** — [references/template-complete-spec.md](references/template-complete-spec.md) — Full OpenAPI 3.1 spec with all components (schemas, parameters, responses, security, examples)
- **FastAPI/Python** — [references/template-fastapi-python.md](references/template-fastapi-python.md) — Code-first with Pydantic models and automatic OpenAPI generation
- **tsoa/TypeScript** — [references/template-tsoa-typescript.md](references/template-tsoa-typescript.md) — Decorator-based spec generation for Express
- **Validation** — [references/template-validation-linting.md](references/template-validation-linting.md) — Spectral & Redocly configs for linting and bundling
- **SDK Generation** — [references/sdk-generation.md](references/sdk-generation.md) — OpenAPI Generator commands for TypeScript, Python, Go clients

## Best Practices

### Do's

- **Use $ref** — Reuse schemas, parameters, responses
- **Add examples** — Real-world values help consumers
- **Document errors** — All possible error codes
- **Version the API** — In URL or header
- **Use semantic versioning** — For spec changes

### Don'ts

- **Don't use generic descriptions** — Be specific
- **Don't skip security** — Define all schemes
- **Don't forget nullable** — Be explicit about null
- **Don't mix styles** — Consistent naming throughout
- **Don't hardcode URLs** — Use server variables

## Resources

- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0)
- [Spectral](https://stoplight.io/open-source/spectral)
