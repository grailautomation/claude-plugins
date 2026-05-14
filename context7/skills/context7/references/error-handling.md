# Context7 Error Handling & Troubleshooting

## Common Errors

### "Documentation not found or not finalized"

**Causes:**
- Library not indexed in Context7's database
- Version-specific docs unavailable (common even when base library exists)
- Typo in library ID

**Solutions:**
1. Always call `resolve-library-id` first — don't guess IDs
2. Try the base `/org/project` format without version specifier
3. Check if library exists at context7.com
4. For missing libraries, user can submit at context7.com/add-library

### Empty or Irrelevant Results

**Causes:**
- Topic parameter too narrow
- Low token limit
- Library has sparse documentation

**Solutions:**
1. Use a fuller task-oriented `query` with the library area included
2. Try a general setup or usage query first, then refine
3. If the library has few docs, retry with the base `/org/project` ID

### Rate Limit Exceeded (HTTP 429)

**Causes:**
- Free tier allows ~60 requests/hour
- Heavy usage without API key

**Solutions:**
1. Implement exponential backoff
2. Cache results for repeated queries
3. Obtain API key from context7.com/dashboard

### Connection/Server Errors

**Causes:**
- MCP server not running
- Network issues
- npx resolution failures (especially Windows)

**Solutions:**
1. Verify MCP is configured: `claude mcp list`
2. Test the package directly: `npx -y @upstash/context7-mcp`
3. Try remote server instead of local: `https://mcp.context7.com/mcp`
4. Replace `npx` with `bunx -y @upstash/context7-mcp`

## Fallback Strategies

When Context7 fails, use these fallbacks in order:

1. **Retry with base ID**: Remove version specifier, try `/org/project`
2. **Broaden query**: Use a fuller task-oriented query
3. **Check availability**: Verify at context7.com before more attempts
4. **Use training knowledge**: Fall back to built-in knowledge with caveat about potential staleness
5. **Web search**: Fetch official docs directly as last resort

## Error Response Examples

**Successful resolution:**
```json
{
  "libraries": [
    {
      "id": "/vercel/next.js",
      "name": "Next.js",
      "trust_score": 0.95,
      "snippet_count": 1250,
      "versions": ["v15.1.0", "v14.2.0"]
    }
  ]
}
```

**Failed resolution:**
```json
{
  "libraries": []
}
```
Library name not recognized. Try alternative names or check context7.com.

**Documentation not found:**
```json
{
  "error": "Documentation not found or not finalized"
}
```
ID invalid or library not indexed. Verify with `resolve-library-id` first.
