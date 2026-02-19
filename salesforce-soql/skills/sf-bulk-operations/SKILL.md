---
name: sf-bulk-operations
description: >
  Salesforce Bulk API 2.0 write operations using the sf CLI. Use when
  performing bulk data imports, updates, upserts, or deletes via
  sf data import bulk, sf data update bulk, sf data upsert bulk,
  sf data delete bulk, or sf data resume. Covers CSV preparation,
  line endings, job monitoring, error handling, and result retrieval.
user-invocable: false
---

# Salesforce Bulk Write Operations

Bulk API 2.0 write operations for inserting, updating, upserting, and deleting records via the `sf` CLI.

## Critical: Choose the Right Command

The Bulk API 2.0 does **NOT** auto-detect the operation from your CSV. Each operation has a separate command:

| Command | Operation | Required CSV Column | Use When |
|---------|-----------|-------------------|----------|
| `sf data import bulk` | INSERT | (none — creates new records) | Loading new records |
| `sf data update bulk` | UPDATE | `Id` | Modifying existing records by Salesforce ID |
| `sf data upsert bulk` | UPSERT | External ID field | Insert-or-update by external key |
| `sf data delete bulk` | DELETE | `Id` | Removing records by Salesforce ID |

Common mistake: using `import` (INSERT) when you need `update` (UPDATE). If all
records fail with `INVALID_CROSS_REFERENCE_KEY` or duplicate errors, you likely
used the wrong command.

## CSV Preparation

### Line Endings (macOS Gotcha)

The `--line-ending` flag must match your CSV's actual line endings. On macOS, the default is `LF`.

**Python's `csv` module writes CRLF (`\r\n`) by default.** To produce LF:

```python
with open("upload.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Id", "My_Field__c"], lineterminator="\n")
    writer.writeheader()
    for row in data:
        writer.writerow(row)
```

Then pass `--line-ending LF` explicitly:

```bash
sf data update bulk --file upload.csv --sobject Account --target-org myorg --line-ending LF --wait 10
```

If line endings don't match, you'll get: `ClientInputError: LineEnding is invalid on user data`.

### Header Row

- Use **API field names** (e.g., `Stripe_ATR__c`), not field labels (e.g., "Stripe ATR")
- For update/delete: include an `Id` column with 18-character Salesforce record IDs
- For upsert: include the external ID field specified by `--external-id`

### Column Delimiter

Default is comma. Use `--column-delimiter` for alternatives: `BACKQUOTE`, `CARET`, `COMMA`, `PIPE`, `SEMICOLON`, `TAB`.

## Running Bulk Jobs

### Always Use `--json` Output

The progress spinner produces thousands of ANSI escape characters that overflow terminal buffers. Always capture structured output:

```bash
sf data update bulk \
  --file upload.csv \
  --sobject Account \
  --target-org production \
  --line-ending LF \
  --wait 10 \
  --json 2>&1 | tail -50
```

### Common Flags

| Flag | Description |
|------|-------------|
| `--file` | Path to CSV file (required) |
| `--sobject` | API name of target object (required) |
| `--target-org` | Org alias or username (required) |
| `--line-ending` | `LF` or `CRLF` (default: LF on macOS, CRLF on Windows) |
| `--wait` | Minutes to wait for completion |
| `--external-id` | External ID field name (upsert only) |
| `--column-delimiter` | CSV delimiter |

### Async Jobs

If `--wait` is omitted or the job exceeds the wait time, the CLI returns a job ID. Resume monitoring with:

```bash
sf data import resume --job-id <JOB_ID> --target-org myorg --wait 10 --json
sf data update resume --job-id <JOB_ID> --target-org myorg --wait 10 --json
```

## Inspecting Results

After a job completes (or partially fails):

```bash
sf data bulk results --job-id <JOB_ID> --target-org myorg --json
```

Returns:

```json
{
  "result": {
    "processedRecords": 19852,
    "successfulRecords": 19277,
    "failedRecords": 575,
    "status": "JobComplete",
    "operation": "update",
    "object": "Account",
    "successFilePath": "<JOB_ID>-success-records.csv",
    "failedFilePath": "<JOB_ID>-failed-records.csv"
  }
}
```

The failed records CSV includes the error reason per row:

```
"sf__Id","sf__Error",Id,My_Field__c
"","INVALID_CROSS_REFERENCE_KEY:invalid cross reference id:--","001xxx","value"
```

### Clean Up Result Files

Bulk results write CSV files to the current directory. Clean up after inspection:

```bash
rm -f <JOB_ID>-success-records.csv <JOB_ID>-failed-records.csv
```

## Sandbox Considerations

When running bulk operations against a sandbox:

- **`INVALID_CROSS_REFERENCE_KEY`** errors are expected for record IDs that exist in production but not in the sandbox (accounts created after the last sandbox refresh, or deleted in sandbox). This is normal — compare success count to total to assess coverage.
- Sandbox refresh resets data but not metadata. Custom fields created in production should exist in sandbox after refresh.
- Test with a small subset first (`head -100 upload.csv > test.csv`) before running the full batch.

## Examples

### Update a Custom Field on Accounts

```bash
# Prepare CSV with LF line endings (Python)
python -c "
import csv
with open('update.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, ['Id','My_Field__c'], lineterminator='\n')
    w.writeheader()
    w.writerow({'Id': '001xxx', 'My_Field__c': '42.50'})
"

# Upload
sf data update bulk \
  --file update.csv \
  --sobject Account \
  --target-org production \
  --line-ending LF \
  --wait 10 \
  --json 2>&1 | tail -50
```

### Upsert by External ID

```bash
sf data upsert bulk \
  --file contacts.csv \
  --sobject Contact \
  --external-id External_Id__c \
  --target-org production \
  --line-ending LF \
  --wait 10 \
  --json 2>&1 | tail -50
```

### Delete Records

```bash
# CSV needs only the Id column
echo "Id" > delete.csv
echo "001xxx" >> delete.csv

sf data delete bulk \
  --file delete.csv \
  --sobject Account \
  --target-org sandbox \
  --line-ending LF \
  --wait 10 \
  --json 2>&1 | tail -50
```
