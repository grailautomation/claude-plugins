# SF CLI Output Formats

## JSON Output (Recommended)

Best for parsing results programmatically.

```bash
sf data query --query "SELECT Id, Name FROM Account LIMIT 5" --target-org production --json
```

### JSON Structure

```json
{
  "status": 0,
  "result": {
    "records": [
      {
        "attributes": {
          "type": "Account",
          "url": "/services/data/v65.0/sobjects/Account/001xxx"
        },
        "Id": "001xxx",
        "Name": "Acme Corporation"
      }
    ],
    "totalSize": 1,
    "done": true
  },
  "warnings": []
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `status` | 0 = success, 1 = error |
| `result.records` | Array of record objects |
| `result.totalSize` | Number of records returned |
| `result.done` | Query completed (for paging) |

### Handling Large Output

```bash
# Limit output lines
sf data query --query "SELECT Id, Name FROM Account" --target-org production --json 2>&1 | head -100

# Save to file
sf data query --query "SELECT Id, Name FROM Account" --target-org production --json > results.json

# Extract records only (jq)
sf data query --query "SELECT Id, Name FROM Account" --target-org production --json | jq '.result.records'
```

## Human-Readable Table

Default format when `--json` not specified:

```bash
sf data query --query "SELECT Id, Name FROM Account LIMIT 5" --target-org production
```

Output:
```
 Id                 Name
 ────────────────── ─────────────────
 001xxx             Acme Corporation
 001yyy             Globex Inc
```

## CSV Output

For spreadsheet compatibility:

```bash
sf data query --query "SELECT Id, Name FROM Account LIMIT 5" --target-org production --result-format csv
```

## Bulk Export (Large Datasets)

For queries returning > 10,000 records:

```bash
# Export to CSV
sf data export bulk \
  --query "SELECT Id, Name FROM Account" \
  --output-file accounts.csv \
  --target-org production \
  --wait 10

# Export to JSON
sf data export bulk \
  --query "SELECT Id, Name FROM Account" \
  --output-file accounts.json \
  --result-format json \
  --target-org production \
  --wait 10

# Include deleted records
sf data export bulk \
  --query "SELECT Id, Name FROM Account" \
  --output-file accounts.csv \
  --target-org production \
  --all-rows \
  --wait 10
```

### Bulk Export Options

| Flag | Description |
|------|-------------|
| `--output-file` | Path for output file |
| `--result-format` | `csv` or `json` |
| `--wait` | Minutes to wait for completion |
| `--all-rows` | Include soft-deleted records |
| `--column-delimiter` | CSV delimiter (COMMA, TAB, etc.) |

## Query from File

For complex queries:

```bash
# Create query file
echo "SELECT Id, Name, Account.Name FROM Contact WHERE AccountId <> null" > query.soql

# Run from file
sf data query --file query.soql --target-org production --json
```

## Error Output

Errors return JSON with error details:

```json
{
  "status": 1,
  "name": "MALFORMED_QUERY",
  "message": "unexpected token: '\\'",
  "exitCode": 1
}
```

### Common Error Patterns

| Error | Meaning |
|-------|---------|
| `MALFORMED_QUERY` | Syntax error in SOQL |
| `INVALID_FIELD` | Field doesn't exist or can't be queried |
| `NO_AUTHORIZATION_FOUND` | Not authenticated |
| `INVALID_SESSION_ID` | Token expired |

## Suppress Warnings

```bash
sf data query --query "SELECT Id FROM Account" --target-org production --json 2>/dev/null
```

## Parse with jq

```bash
# Get just record count
sf data query --query "SELECT Id FROM Account" --target-org prod --json | jq '.result.totalSize'

# Get first record
sf data query --query "SELECT Id, Name FROM Account LIMIT 1" --target-org prod --json | jq '.result.records[0]'

# Get specific field values
sf data query --query "SELECT Id, Name FROM Account LIMIT 5" --target-org prod --json | jq '.result.records[].Name'
```
