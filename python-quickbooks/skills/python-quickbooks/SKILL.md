---
name: python-quickbooks
description: >
  Python QuickBooks Online API library reference (ej2/python-quickbooks). This skill
  should be used when the user asks to "create a QuickBooks invoice", "query QBO
  customers", "set up QuickBooks authentication", "use python-quickbooks", "filter
  QuickBooks objects", "create a bill", "record a payment", "batch update", or any
  QuickBooks Online API integration in Python. Also covers "QBO", "intuit api python".
user-invocable: false
---

# python-quickbooks Reference

Complete reference for [ej2/python-quickbooks](https://github.com/ej2/python-quickbooks) — Python 3 library for the QuickBooks Online API.

## Installation

```bash
pip install python-quickbooks
pip install intuit-oauth
```

## Quick Start

```python
from intuitlib.client import AuthClient
from quickbooks import QuickBooks

auth_client = AuthClient(
    client_id='CLIENT_ID',
    client_secret='CLIENT_SECRET',
    access_token='ACCESS_TOKEN',
    environment='sandbox',  # or 'production'
    redirect_uri='http://localhost:8000/callback',
)

client = QuickBooks(
    auth_client=auth_client,
    refresh_token='REFRESH_TOKEN',
    company_id='COMPANY_ID',
    minorversion=75,
)
```

## Core Operations

```python
from quickbooks.objects.customer import Customer
from quickbooks.objects.invoice import Invoice

# Get by ID
customer = Customer.get(1, qb=client)

# Save (create or update — determined by presence of Id)
customer = Customer()
customer.DisplayName = "New Customer"
customer.save(qb=client)

# List all (max 100 by default)
customers = Customer.all(qb=client)

# Filter with kwargs
customers = Customer.filter(Active=True, CompanyName="Acme", qb=client)

# Raw WHERE clause
customers = Customer.where("Active = true AND Balance > '100'", qb=client)

# Raw SQL query
customers = Customer.query("SELECT * FROM Customer WHERE Active = true", qb=client)

# Count
count = Customer.count("Active = true", qb=client)

# Choose (IN-style query)
customers = Customer.choose([1, 2, 3], field="Id", qb=client)

# Delete (requires Id + SyncToken — not all objects support delete)
invoice = Invoice.get(42, qb=client)
invoice.delete(qb=client)

# Void (Invoice, Payment, BillPayment, SalesReceipt)
invoice.void(qb=client)

# Send via email
invoice.send(qb=client)
invoice.send(qb=client, send_to="other@example.com")

# Download PDF (Invoice, Estimate, SalesReceipt)
pdf_data = invoice.download_pdf(qb=client)
```

## Object Capabilities Matrix

| Object | get | all/filter | save | delete | void | send | pdf |
|--------|-----|-----------|------|--------|------|------|-----|
| Customer | Y | Y | Y | - | - | - | - |
| Vendor | Y | Y | Y | - | - | - | - |
| Employee | Y | Y | Y | - | - | - | - |
| Invoice | Y | Y | Y | Y | Y | Y | Y |
| Bill | Y | Y | Y | Y | - | - | - |
| BillPayment | Y | Y | Y | Y | Y | - | - |
| Payment | Y | Y | Y | Y | Y | - | - |
| Estimate | Y | Y | Y | Y | - | Y | Y |
| Purchase | Y | Y | Y | Y | - | - | - |
| PurchaseOrder | Y | Y | Y | Y | - | Y | - |
| SalesReceipt | Y | Y | Y | Y | Y | - | Y |
| CreditMemo | Y | Y | Y | Y | - | - | - |
| RefundReceipt | Y | Y | Y | Y | - | - | - |
| VendorCredit | Y | Y | Y | Y | - | - | - |
| Deposit | Y | Y | Y | Y | - | - | - |
| Transfer | Y | Y | Y | Y | - | - | - |
| JournalEntry | Y | Y | Y | Y | - | - | - |
| Item | Y | Y | Y | - | - | - | - |
| Account | Y | Y | Y | - | - | - | - |
| Department | Y | Y | Y | - | - | - | - |
| Term | Y | Y | Y | - | - | - | - |
| Class | Y | Y | Y | - | - | - | - |
| TimeActivity | Y | Y | Y | Y | - | - | - |
| TaxCode | Y | Y | - | - | - | - | - |
| TaxRate | Y | Y | - | - | - | - | - |
| TaxAgency | Y | Y | Y | - | - | - | - |
| TaxService | - | - | Y | - | - | - | - |
| PaymentMethod | Y | Y | Y | - | - | - | - |
| CompanyInfo | Y | - | Y | - | - | - | - |
| Preferences | Y* | - | Y* | - | - | - | - |
| Attachable | Y | Y | Y | Y | - | - | - |
| Budget | Y | Y | - | - | - | - | - |
| CustomerType | Y | Y | - | - | - | - | - |
| CompanyCurrency | Y | Y | Y | - | - | - | - |
| ExchangeRate | - | Y | Y* | - | - | - | - |
| RecurringTxn | Y | Y | Y* | Y* | - | - | - |
| CreditCardPayment | Y | Y | Y | Y | - | - | - |

*Preferences uses PrefMixin.get() (no id param). ExchangeRate uses UpdateNoIdMixin. RecurringTransaction uses UpdateNoIdMixin/DeleteNoIdMixin.

## Critical Notes

- **PascalCase naming**: All object properties use PascalCase (e.g., `DisplayName`, `TotalAmt`), NOT Python snake_case. This matches the QBO API directly.
- **1000 entity max**: QBO API returns max 1000 entities per query. Use `start_position` and `max_results` for pagination.
- **No input sanitization**: The library does not sanitize query inputs. Escape user input in WHERE clauses yourself.
- **Minor version required**: As of v0.9.8+, you must specify `minorversion` explicitly. Default minimum is 75. See [Intuit deprecation notice](https://blogs.intuit.com/2025/01/21/changes-to-our-accounting-api-that-may-impact-your-application/).
- **Singleton behavior**: By default, `QuickBooks()` creates a new instance each call. To enable singleton, use the mangled name: `QuickBooks._QuickBooks__use_global = True` (the `__use_global` attribute is name-mangled; `QuickBooks.__use_global = True` silently creates a new attribute).
- **Sparse updates**: Always set `obj.sparse = True` before `save()` on updates to avoid overwriting unset fields. Full updates (default) replace ALL fields. See [CRUD Operations](references/crud-operations.md#sparse-updates).
- **Rate limits**: QBO enforces 500 requests/min and 10 concurrent per realm. The library does no rate limiting or retry. See [Advanced Features](references/advanced-features.md#rate-limiting).
- **SalesReceipt/RefundReceipt empty detail_dict**: Both have `detail_dict = {}`, so all lines deserialize as generic `DetailLine` — you lose typed detail attributes. Manually check `DetailType` and access raw dicts. See [Financial Objects](references/objects-financial.md#salesreceipt).
- **Single-use refresh tokens**: Each refresh invalidates the previous token. Persist the new refresh token immediately after client init, or risk requiring full re-authorization. See [Authentication](references/authentication.md#token-lifecycle).
- **CreditMemo DetailType key**: CreditMemo uses `"DescriptionLineDetail"` where Invoice/Estimate use `"DescriptionOnly"` for description-only lines. Code that works for invoices silently falls back to generic `DetailLine` on CreditMemos. See [Line Items](references/line-items.md#creditmemo-detail_dict).
- **save() determines create vs update**: If `obj.Id` exists and > 0, it updates; otherwise it creates.
- **delete() needs SyncToken**: Always `get()` the object first before deleting to ensure you have the current SyncToken.

## Reference Index

Detailed documentation is available in the following reference files. Read these on demand for comprehensive coverage:

- [Authentication](references/authentication.md) — AuthClient, OAuth, env vars, sandbox vs production, refresh tokens, minor version
- [Querying](references/querying.md) — all, filter, where, query, count, choose, pagination, ordering
- [CRUD Operations](references/crud-operations.md) — get, save, delete, void, send, download_pdf
- [Object Capabilities](references/object-capabilities.md) — Full capabilities matrix with import paths
- [Entity Objects](references/objects-entities.md) — Customer, Vendor, Employee, Department, CompanyCurrency, CustomerType
- [Financial Objects](references/objects-financial.md) — Invoice, Bill, Payment, Estimate, Purchase, SalesReceipt, etc.
- [Items & Accounting](references/objects-items-accounting.md) — Item, Account, Term, Class, Budget, TimeActivity, ExchangeRate
- [Tax & Settings](references/objects-tax-settings.md) — TaxCode, TaxRate, Preferences, CompanyInfo, Attachable, RecurringTransaction
- [Line Items](references/line-items.md) — DetailLine types, SalesItemLine, AccountBasedExpenseLine, all line detail types
- [Batch Operations](references/batch-operations.md) — batch_create/update/delete, result handling
- [Advanced Features](references/advanced-features.md) — CDC, attachments, reports, recurring transactions, webhooks
- [Helpers & Errors](references/helpers-and-errors.md) — Date formatting, JSON utilities, exception hierarchy
- [Examples](references/examples.md) — Complete working examples end-to-end
