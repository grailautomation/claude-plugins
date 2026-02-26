# SDK Generation

```bash
# Generate TypeScript client
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated/typescript-client \
  --additional-properties=supportsES6=true,npmName=@myorg/api-client

# Generate Python client
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./generated/python-client \
  --additional-properties=packageName=api_client

# Generate Go client
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g go \
  -o ./generated/go-client
```
