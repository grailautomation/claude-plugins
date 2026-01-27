# SF CLI Error Handling

## Common Errors and Solutions

### MALFORMED_QUERY

**Error**: `unexpected token: '\'` or similar syntax errors

**Causes**:
1. Shell escaping issues (especially with `!` or special characters)
2. Syntax errors in SOQL
3. Unclosed quotes

**Solutions**:

```bash
# Use <> instead of != (shell escapes !)
# BAD:
sf data query --query "SELECT Id FROM Account WHERE Name != null"

# GOOD:
sf data query --query "SELECT Id FROM Account WHERE Name <> null"

# Use single quotes for the query if it contains special characters
sf data query --query 'SELECT Id FROM Account WHERE Name <> null'
```

---

### INVALID_FIELD

**Error**: `field 'FieldName' can not be filtered in a query call`

**Causes**:
1. Long Text Area fields cannot be filtered
2. Field doesn't exist
3. Wrong API name

**Solutions**:

```bash
# Don't filter on long text fields - query all and filter client-side
# BAD:
sf data query --query "SELECT Id FROM Case WHERE Description LIKE '%error%'"

# GOOD:
sf data query --query "SELECT Id, Description FROM Case" | grep error
```

To verify field exists:
```bash
sf sobject describe --sobject Account --target-org production --json | grep -i "fieldname"
```

---

### NO_AUTHORIZATION_FOUND

**Error**: `No authorization found for alias: xxx`

**Cause**: Org not authenticated or alias doesn't exist

**Solution**:

```bash
# Check authenticated orgs
sf org list

# Re-authenticate
sf org login web --alias <alias>
```

---

### INVALID_SESSION_ID

**Error**: `Session expired or invalid`

**Cause**: OAuth token expired

**Solution**:

```bash
# Re-authenticate
sf org login web --instance-url <your-instance> --alias <alias>
```

---

### QUERY_TIMEOUT

**Error**: Query timed out

**Causes**:
1. Query too complex
2. Too many records
3. Org performance issues

**Solutions**:

```bash
# Add LIMIT
sf data query --query "SELECT Id FROM Account LIMIT 10000"

# Use bulk export for large datasets
sf data export bulk --query "SELECT Id FROM Account" --output-file accounts.csv --wait 20

# Add WHERE clause to reduce scope
sf data query --query "SELECT Id FROM Account WHERE CreatedDate >= LAST_N_DAYS:30"
```

---

### TOO_MANY_QUERY_ROWS

**Error**: Exceeded 50,000 row limit

**Solution**: Use bulk export

```bash
sf data export bulk \
  --query "SELECT Id, Name FROM Account" \
  --output-file accounts.csv \
  --target-org production \
  --wait 30
```

---

### INSUFFICIENT_ACCESS

**Error**: Insufficient access rights on object/field

**Causes**:
1. User profile lacks permission
2. Field-level security restricts access
3. Sharing rules limit visibility

**Solutions**:
- Check user's profile permissions
- Verify field-level security
- Consider using a user with more access

---

### RELATIONSHIP_LIMIT_EXCEEDED

**Error**: Too many relationship queries

**Cause**: Query exceeds relationship limits

**Solutions**:

```bash
# Split into multiple queries
# Instead of:
sf data query --query "SELECT Id, (SELECT Id FROM Contacts), (SELECT Id FROM Opportunities), (SELECT Id FROM Cases), ..."

# Do:
sf data query --query "SELECT Id, (SELECT Id FROM Contacts) FROM Account WHERE Id = 'xxx'"
sf data query --query "SELECT Id, (SELECT Id FROM Opportunities) FROM Account WHERE Id = 'xxx'"
```

---

## Debugging Strategies

### Check Field Names

```bash
sf sobject describe --sobject ObjectName --target-org production --json | grep -E '"name"|"label"'
```

### Check Picklist Values

```bash
sf data query --query "SELECT FieldName, COUNT(Id) FROM Object GROUP BY FieldName" --target-org production --json
```

### Verify Syntax with Smaller Query

```bash
# Start simple
sf data query --query "SELECT Id FROM Account LIMIT 1" --target-org production --json

# Add complexity incrementally
sf data query --query "SELECT Id, Name FROM Account WHERE Type = 'Customer' LIMIT 1" --target-org production --json
```

### Check Org Connection

```bash
sf org display --target-org production
```

### View Full Error Details

```bash
# Errors are in JSON format with --json flag
sf data query --query "BAD QUERY" --target-org production --json 2>&1
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (check message) |
| 68 | Timeout |

## Retry Logic

For transient errors, retry with exponential backoff:

```bash
# Simple retry (in a script)
for i in 1 2 3; do
  sf data query --query "SELECT Id FROM Account LIMIT 1" --target-org production --json && break
  sleep $((i * 5))
done
```
