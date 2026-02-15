# Advanced Features

## Change Data Capture (CDC)

Returns objects that have changed since a given timestamp. Useful for incremental syncing.

```python
from quickbooks.cdc import change_data_capture
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.customer import Customer
from datetime import datetime
```

### Single entity type

```python
cdc_response = change_data_capture(
    [Invoice],
    "2024-01-01T00:00:00",
    qb=client,
)

for invoice in cdc_response.Invoice:
    print(f"Changed: Invoice {invoice.Id} - {invoice.TotalAmt}")
```

### Multiple entity types

```python
cdc_response = change_data_capture(
    [Invoice, Customer],
    "2024-01-01T00:00:00",
    qb=client,
)

for invoice in cdc_response.Invoice:
    print(f"Invoice {invoice.Id}")

for customer in cdc_response.Customer:
    print(f"Customer {customer.DisplayName}")
```

### Using datetime objects

```python
from datetime import datetime

# Datetime objects are automatically converted to string format
cdc_response = change_data_capture(
    [Invoice, Customer],
    datetime(2024, 1, 1, 0, 0, 0),
    qb=client,
)
```

### How CDC works internally

1. Takes a list of QBO classes and a timestamp
2. Builds a comma-separated entity list string (e.g., "Invoice,Customer")
3. Calls the `/cdc` endpoint with `entities` and `changedSince` params
4. Parses the response and sets each entity type as an attribute on `CDCResponse`
5. Each attribute is a `QueryResponse` (iterable list of objects)

### CDCResponse

The response object has dynamic attributes based on the entity types requested:

```python
cdc_response = change_data_capture([Invoice, Customer], timestamp, qb=client)

# Access via attribute matching the class name
cdc_response.Invoice   # QueryResponse (iterable) of Invoice objects
cdc_response.Customer  # QueryResponse (iterable) of Customer objects
```

`QueryResponse` implements `ObjectListMixin` — supports iteration, len, contains, indexing.

---

## Attachments

### Create a note attachment

```python
from quickbooks.objects.attachable import Attachable
from quickbooks.objects.base import AttachableRef, Ref

attachment = Attachable()
attachment.Note = "Important note about this invoice"

# Link to an entity
att_ref = AttachableRef()
entity_ref = Ref()
entity_ref.value = "42"
entity_ref.type = "Invoice"
att_ref.EntityRef = entity_ref
att_ref.IncludeOnSend = True
attachment.AttachableRef.append(att_ref)

attachment.save(qb=client)
```

### Upload a file via path

```python
attachment = Attachable()
attachment.FileName = "receipt.pdf"
attachment.ContentType = "application/pdf"
attachment._FilePath = "/path/to/receipt.pdf"

# Optionally link to a transaction
att_ref = AttachableRef()
entity_ref = Ref()
entity_ref.value = "42"
entity_ref.type = "Invoice"
att_ref.EntityRef = entity_ref
attachment.AttachableRef.append(att_ref)

attachment.save(qb=client)
```

### Upload a file via bytes

```python
attachment = Attachable()
attachment.FileName = "receipt.pdf"
attachment.ContentType = "application/pdf"

with open("/path/to/receipt.pdf", "rb") as f:
    attachment._FileBytes = f.read()

attachment.save(qb=client)
```

### Important notes

- `_FilePath` and `_FileBytes` are **mutually exclusive** — setting both raises `ValueError`
- File uploads use multipart form data with base64 encoding internally
- First save (create with file) returns response in `AttachableResponse[0].Attachable`
- Subsequent saves (update) return response in `Attachable`
- Properties starting with `_` are filtered from JSON serialization

---

## Reports

Access QBO reports via the client directly:

```python
# Get a report
report = client.get_report("ProfitAndLoss", qs={
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
})

# Other report types
report = client.get_report("BalanceSheet")
report = client.get_report("CashFlow")
report = client.get_report("GeneralLedger")
report = client.get_report("TrialBalance")
report = client.get_report("AgedReceivables")
report = client.get_report("AgedPayables")
```

### Signature

```python
def get_report(self, report_type, qs=None)
```

- `report_type`: The QBO report name (e.g., "ProfitAndLoss")
- `qs`: Dict of query string parameters for the report

The return value is the raw JSON response from the QBO reporting API.

---

## Recurring Transactions

```python
from quickbooks.objects.recurringtransaction import (
    RecurringTransaction,
    RecurringInvoice,
    RecurringBill,
    RecurringInfo,
    ScheduleInfo,
)
```

### List recurring transactions

```python
recurring = RecurringTransaction.all(qb=client)
```

### Get a recurring transaction

```python
recurring = RecurringTransaction.get(5, qb=client)
```

### 12 Recurring Variants

Each recurring type extends its base transaction with `RecurringInfo` and `RecurDataRef`:

- RecurringBill, RecurringPurchase, RecurringCreditMemo
- RecurringDeposit, RecurringEstimate, RecurringInvoice
- RecurringJournalEntry, RecurringRefundReceipt, RecurringSalesReceipt
- RecurringTransfer, RecurringVendorCredit, RecurringPurchaseOrder

### ScheduleInfo fields

| Field | Description |
|-------|-------------|
| StartDate | When the schedule begins |
| EndDate | When the schedule ends |
| DaysBefore | Days before due date to create |
| MaxOccurrences | Maximum number of occurrences |
| RemindDays | Days before to send reminder |
| IntervalType | Frequency type |
| NumInterval | Number of intervals |
| DayOfMonth | Day of month (1-31) |
| DayOfWeek | Day of week |
| MonthOfYear | Month name |
| WeekOfMonth | Week of month (1-5) |
| NextDate | Next scheduled date (read-only) |
| PreviousDate | Previous occurrence date (read-only) |

### RecurringInfo

| Field | Default | Description |
|-------|---------|-------------|
| RecurType | "Automated" | "Automated", "Reminder", or "Unscheduled" |
| Name | "" | Display name for the template |
| Active | False | Whether the schedule is active |

---

## Webhook Validation

Validate incoming webhook signatures:

```python
# Set verifier token on client
client = QuickBooks(
    auth_client=auth_client,
    refresh_token='...',
    company_id='...',
    verifier_token='YOUR_WEBHOOK_VERIFIER_TOKEN',
)

# Validate webhook signature
is_valid = client.validate_webhook_signature(
    request_body=request.body.decode('utf-8'),  # Must be str, not bytes
    signature=request.headers['intuit-signature'],
)

# Or pass verifier token directly
is_valid = client.validate_webhook_signature(
    request_body=request.body.decode('utf-8'),
    signature=request.headers['intuit-signature'],
    verifier_token='YOUR_TOKEN',
)
```

**Type requirements**: Both `request_body` and `verifier_token` must be **strings** (not bytes). Internally, `request_body.encode('utf-8')` is called — passing bytes raises `AttributeError`. The `verifier_token` is passed through `bytes(value, 'utf-8')` which also requires a string.

The validation uses HMAC-SHA256: `hmac.new(verifier_token, body, sha256)` compared against the base64-decoded signature.

---

## Shareable Invoice Links

Enable shareable invoice links by setting `invoice_link=True` on the client:

```python
client = QuickBooks(
    auth_client=auth_client,
    refresh_token='...',
    company_id='...',
    invoice_link=True,
)

invoice = Invoice.get(42, qb=client)
print(invoice.InvoiceLink)  # Shareable URL
```

---

## LinkedTxn / LinkedTxnMixin

Most transaction objects support `to_linked_txn()` for creating references between transactions:

```python
# Link a payment to an invoice
invoice = Invoice.get(42, qb=client)
linked_txn = invoice.to_linked_txn()
# linked_txn.TxnId = invoice.Id
# linked_txn.TxnType = "Invoice"
# linked_txn.TxnLineId = 1
```

This is how you record payments against specific invoices or link bills to purchase orders.

---

## Current User

Get information about the authenticated user:

```python
user_info = client.get_current_user()
```

Uses the endpoint: `https://appcenter.intuit.com/api/v1/user/current`

---

## Rate Limiting

QBO enforces these limits per realm (company):

| Limit | Value |
|-------|-------|
| Requests per minute | 500 |
| Concurrent requests | 10 |

**The library does zero rate limiting, queueing, or retry.** HTTP 429 responses are not handled — they raise a generic exception. You must implement backoff and retry yourself.

Recommended pattern:

```python
import time
from quickbooks.exceptions import QuickbooksException

def qbo_request_with_retry(fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return fn()
        except QuickbooksException as e:
            if "throttl" in str(e.detail).lower() or e.error_code == 429:
                time.sleep(2 ** attempt)
                continue
            raise
    raise QuickbooksException("Max retries exceeded", error_code=429)
```

---

## Thread Safety

`OAuth2Session` (used internally by the client) is **not thread-safe**. If you're making concurrent API calls, create one `QuickBooks` client per thread. Do not share a single client instance across threads.

---

## query() Uses POST

The `query()` method sends SELECT statements as a POST body (not GET with query params). The content type is `application/text`. This is a QBO API requirement, not a library choice.

---

## Decimal Mode

For financial precision, enable decimal parsing:

```python
client = QuickBooks(
    auth_client=auth_client,
    refresh_token='...',
    company_id='...',
    use_decimal=True,
)

# Now all numeric values from the API are parsed as decimal.Decimal
invoice = Invoice.get(42, qb=client)
print(type(invoice.TotalAmt))  # <class 'decimal.Decimal'>
```
