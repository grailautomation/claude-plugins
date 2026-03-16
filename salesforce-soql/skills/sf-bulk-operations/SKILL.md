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

## JSON Response Shapes (Critical for Programmatic Use)

`sf data update bulk --json` returns **two completely different JSON shapes** depending on whether all records succeeded or some failed. Code that parses bulk operation results must handle both.

### Full Success (status: 0)

All records processed without error:

```json
{
  "status": 0,
  "result": {
    "id": "750TN00000iZJOGYA4",
    "processedRecords": 17956,
    "failedRecords": 0,
    "status": "JobComplete",
    "operation": "update",
    "object": "Account"
  }
}
```

Record counts and job state are directly in `result`.

### Partial Failure (status: 1, FailedRecordDetailsError)

Some records failed — the CLI wraps the response in an **error envelope** with a different shape:

```json
{
  "name": "FailedRecordDetailsError",
  "message": "Job finished being processed but failed to process 200 records.",
  "exitCode": 1,
  "status": 1,
  "data": {
    "jobId": "750TN00000iZk9tYAC",
    "state": "JobComplete"
  },
  "actions": [
    "Get the job results by running: \"sf data bulk results -o myorg --job-id 750TN...\"."
  ],
  "context": "DataUpdateBulk",
  "commandName": "DataUpdateBulk"
}
```

**The error envelope does NOT contain record counts.** Only `data.jobId` and `data.state`. To get `processedRecords`/`failedRecords`, you must follow up with `sf data bulk results`.

### Parsing Strategy for Scripts

```python
payload = json.loads(stdout)

if payload.get("status") == 0:
    # Success — counts in result
    result = payload["result"]
    processed = result["processedRecords"]
    failed = result["failedRecords"]
else:
    # Error envelope — check if job completed with failures
    err_data = payload.get("data", {})
    job_id = err_data.get("jobId")
    job_state = err_data.get("state")

    if job_state == "JobComplete" and job_id:
        # Job completed but had failures — fetch counts separately
        # Run: sf data bulk results --job-id <job_id> --target-org <org> --json
        pass
    else:
        # Real failure — job didn't complete
        raise RuntimeError(payload.get("message", "Unknown error"))
```

## Inspecting Results

After a job completes (or partially fails), fetch detailed results:

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

**Side effect:** This command writes `<JOB_ID>-success-records.csv` and `<JOB_ID>-failed-records.csv` to the **current working directory**. These can be large (3+ MB for 18K rows).

The failed records CSV includes the error reason per row:

```
"sf__Id","sf__Error",Id,My_Field__c
"","UNABLE_TO_LOCK_ROW:unable to obtain exclusive access to this record or 200 records: 001xxx,001yyy,...:--","001xxx","value"
"","INVALID_CROSS_REFERENCE_KEY:invalid cross reference id:--","001zzz","value"
```

### Clean Up Result Files

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
