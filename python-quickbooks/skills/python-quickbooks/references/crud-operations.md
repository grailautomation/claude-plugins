# CRUD Operations

## get(id)

Retrieves a single object by its QBO ID. Provided by `ReadMixin`.

```python
from quickbooks.objects.customer import Customer

customer = Customer.get(42, qb=client)

# With optional params
customer = Customer.get(42, qb=client, params={'minorversion': 75})
```

### Signature

```python
@classmethod
def get(cls, id, qb=None, params=None)
```

### Special case: Preferences

`Preferences` uses `PrefMixin.get()` which takes no `id` parameter (there's only one Preferences object per company):

```python
from quickbooks.objects.preferences import Preferences

prefs = Preferences.get(qb=client)
```

## save()

Creates or updates an object. Provided by `UpdateMixin`.

**Key behavior**: If `obj.Id` exists and is > 0, it performs an **update**. Otherwise it performs a **create**.

```python
# CREATE — no Id set
customer = Customer()
customer.DisplayName = "New Customer"
saved = customer.save(qb=client)
print(saved.Id)  # Now has an Id

# UPDATE — Id already exists
customer = Customer.get(42, qb=client)
customer.DisplayName = "Updated Name"
saved = customer.save(qb=client)
```

### Signature

```python
def save(self, qb=None, request_id=None, params=None)
```

### Sparse Updates

**Warning**: By default, `save()` performs a **full update** — every field on the object is sent to QBO, and any field you didn't explicitly set gets overwritten with its default value (empty string, 0, etc.). This is the most common source of data corruption.

Always set `sparse = True` before updating existing objects:

```python
customer = Customer.get(42, qb=client)
customer.CompanyName = "New Name"
customer.sparse = True  # Only send changed fields
customer.save(qb=client)
```

The `sparse` attribute defaults to `False` on `QuickbooksTransactionEntity`. Without it, a save that only sets `CompanyName` will blank out every other field.

### Optional query params on save

```python
# Include optional parameters in the query string
purchase = Purchase()
# ... set fields ...
purchase.save(qb=client, params={'include': 'allowduplicatedocnum'})
```

### Request ID for idempotency

```python
customer.save(qb=client, request_id='unique-request-id-123')
```

### UpdateNoIdMixin

Some objects (`ExchangeRate`, `Preferences`, `RecurringTransaction`) use `UpdateNoIdMixin` which always performs an update (no create/update branching based on Id):

```python
from quickbooks.objects.exchangerate import ExchangeRate

rate = ExchangeRate()
rate.SourceCurrencyCode = "EUR"
rate.Rate = 1.15
rate.save(qb=client)  # Always calls update_object
```

### TaxService special save

`TaxService` has a custom `save()` that creates via the `TaxService/Taxcode` endpoint:

```python
from quickbooks.objects.taxservice import TaxService, TaxRateDetails

tax_service = TaxService()
tax_service.TaxCode = "MyTaxCode"

detail = TaxRateDetails()
detail.TaxRateName = "Sales Tax"
detail.RateValue = "8.5"
detail.TaxAgencyId = "1"
detail.TaxApplicableOn = "Sales"
tax_service.TaxRateDetails.append(detail)

tax_service.save(qb=client)
```

### Attachable special save

`Attachable` has a custom `save()` that handles file uploads via `_FilePath` or `_FileBytes`.

**Signature**: `def save(self, qb=None)` — note that Attachable's `save()` does NOT accept `request_id` or `params`. Passing those kwargs raises `TypeError`.

```python
from quickbooks.objects.attachable import Attachable

att = Attachable()
att.FileName = "receipt.pdf"
att.ContentType = "application/pdf"
att._FilePath = "/path/to/receipt.pdf"  # OR use _FileBytes
att.save(qb=client)  # Only qb= is accepted
```

**Important**: `_FilePath` and `_FileBytes` are mutually exclusive. Setting both raises `ValueError`.

## delete()

Deletes an object. Provided by `DeleteMixin`. Requires `Id` and `SyncToken`. Not all objects support delete — check the [Object Capabilities Matrix](../SKILL.md).

```python
# Always get() first to ensure current SyncToken
invoice = Invoice.get(42, qb=client)
invoice.delete(qb=client)
```

### Signature

```python
def delete(self, qb=None, request_id=None)
```

**Raises** `QuickbooksException` if `self.Id` is not set.

### What gets sent

Delete sends only `Id` and `SyncToken` to the API:

```json
{"Id": "42", "SyncToken": "3"}
```

### DeleteNoIdMixin

`RecurringTransaction` uses `DeleteNoIdMixin` which sends the full JSON object:

```python
recurring = RecurringTransaction.get(5, qb=client)
recurring.delete(qb=client)  # Sends full object JSON
```

### Soft delete via Active flag

Some objects don't support hard delete. Instead, set `Active = False`:

```python
customer = Customer.get(42, qb=client)
customer.Active = False
customer.save(qb=client)
```

## void()

Voids a transaction. Provided by `VoidMixin`. Available on: **Invoice**, **Payment**, **BillPayment**, **SalesReceipt**.

```python
from quickbooks.objects.invoice import Invoice

invoice = Invoice.get(42, qb=client)
invoice.void(qb=client)
```

### How void works internally

Different objects use different void mechanisms:

| Object | operation param | include param | Data sent |
|--------|----------------|---------------|-----------|
| Invoice | `void` | - | `{Id, SyncToken}` |
| Payment | `update` | `void` | `{Id, SyncToken, sparse: true}` |
| SalesReceipt | `update` | `void` | `{Id, SyncToken, sparse: true}` |
| BillPayment | `update` | `void` | `{Id, SyncToken, sparse: true}` |

**Raises** `QuickbooksException` if `self.Id` is not set.

## send()

Sends a transaction via email. Provided by `SendMixin`. Available on: **Invoice**, **Estimate**, **PurchaseOrder**.

```python
from quickbooks.objects.invoice import Invoice

invoice = Invoice.get(42, qb=client)

# Send to the customer's BillEmail
invoice.send(qb=client)

# Send to a specific email
invoice.send(qb=client, send_to="customer@example.com")
```

### Signature

```python
def send(self, qb=None, send_to=None)
```

The `send_to` parameter is URL-encoded automatically.

## download_pdf()

Downloads a PDF representation. Provided by `QuickbooksPdfDownloadable`. Available on: **Invoice**, **Estimate**, **SalesReceipt**.

```python
from quickbooks.objects.invoice import Invoice

invoice = Invoice.get(42, qb=client)
pdf_bytes = invoice.download_pdf(qb=client)

# Save to file
with open("invoice_42.pdf", "wb") as f:
    f.write(pdf_bytes)
```

### Signature

```python
def download_pdf(self, qb=None)
```

**Raises** `QuickbooksException` if `self.Id` is not set or `qb` is None.

## to_ref()

Many objects support `to_ref()` which creates a `Ref` object for linking:

```python
customer = Customer.get(42, qb=client)
customer_ref = customer.to_ref()
# customer_ref.value = customer.Id
# customer_ref.name = customer.DisplayName
# customer_ref.type = "Customer"

invoice = Invoice()
invoice.CustomerRef = customer_ref
```

## to_linked_txn()

Transaction objects with `LinkedTxnMixin` support creating linked transaction references:

```python
invoice = Invoice.get(42, qb=client)
linked = invoice.to_linked_txn()
# linked.TxnId = invoice.Id
# linked.TxnType = "Invoice"
# linked.TxnLineId = 1
```

This is used when recording payments against invoices.

---

## Production Notes

### Eventual Consistency

After `save()`, subsequent queries may not return the updated data for several seconds. Use the object returned by `save()` instead of immediately re-querying:

```python
# Good — use the returned object
saved = invoice.save(qb=client)
print(saved.TotalAmt)

# Bad — may return stale data
invoice.save(qb=client)
fresh = Invoice.get(invoice.Id, qb=client)  # May not reflect changes yet
```

### SyncToken Conflict Recovery

If another process updated the same object, `save()` raises a `QuickbooksException` with a SyncToken mismatch. Recovery pattern:

```python
try:
    customer.save(qb=client)
except QuickbooksException as e:
    if "stale object" in str(e.detail).lower() or e.error_code == 5010:
        # Re-fetch, re-apply changes, re-save
        customer = Customer.get(customer.Id, qb=client)
        customer.CompanyName = "Desired Name"
        customer.sparse = True
        customer.save(qb=client)
```
