# Complete Working Examples

## Setup (used by all examples)

```python
import os
from intuitlib.client import AuthClient
from quickbooks import QuickBooks

auth_client = AuthClient(
    client_id=os.environ['QBO_CLIENT_ID'],
    client_secret=os.environ['QBO_CLIENT_SECRET'],
    access_token=os.environ.get('QBO_ACCESS_TOKEN'),
    environment=os.environ.get('QBO_ENVIRONMENT', 'sandbox'),
    redirect_uri='http://localhost:8000/callback',
)

client = QuickBooks(
    auth_client=auth_client,
    refresh_token=os.environ['QBO_REFRESH_TOKEN'],
    company_id=os.environ['QBO_COMPANY_ID'],
    minorversion=75,
)
```

---

## Create a Customer

```python
from quickbooks.objects.customer import Customer
from quickbooks.objects.base import Address, PhoneNumber, EmailAddress

customer = Customer()
customer.DisplayName = "Acme Corporation"
customer.CompanyName = "Acme Corporation"
customer.GivenName = "John"
customer.FamilyName = "Doe"

# Set address
address = Address()
address.Line1 = "123 Main Street"
address.City = "San Francisco"
address.CountrySubDivisionCode = "CA"
address.PostalCode = "94105"
customer.BillAddr = address

# Set phone
phone = PhoneNumber()
phone.FreeFormNumber = "(555) 123-4567"
customer.PrimaryPhone = phone

# Set email
email = EmailAddress()
email.Address = "john@example.com"
customer.PrimaryEmailAddr = email

saved_customer = customer.save(qb=client)
print(f"Created customer: {saved_customer.Id} - {saved_customer.DisplayName}")
```

---

## Create an Invoice with Line Items

```python
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.base import Ref, CustomerMemo

# Get customer reference
customer = Customer.get(1, qb=client)

invoice = Invoice()
invoice.CustomerRef = customer.to_ref()
invoice.DueDate = "2024-12-31"
invoice.DocNumber = "INV-001"

# Add line item 1
line1 = SalesItemLine()
line1.Amount = 500.00
line1.Description = "Consulting services - 10 hours"

detail1 = SalesItemLineDetail()
detail1.UnitPrice = 50.00
detail1.Qty = 10

item_ref = Ref()
item_ref.value = "1"  # Item ID
item_ref.name = "Consulting"
detail1.ItemRef = item_ref

line1.SalesItemLineDetail = detail1
invoice.Line.append(line1)

# Add line item 2
line2 = SalesItemLine()
line2.Amount = 200.00
line2.Description = "Software license"

detail2 = SalesItemLineDetail()
detail2.UnitPrice = 200.00
detail2.Qty = 1

item_ref2 = Ref()
item_ref2.value = "2"
item_ref2.name = "Software"
detail2.ItemRef = item_ref2

line2.SalesItemLineDetail = detail2
invoice.Line.append(line2)

# Add memo
memo = CustomerMemo()
memo.value = "Thank you for your business!"
invoice.CustomerMemo = memo

saved_invoice = invoice.save(qb=client)
print(f"Invoice {saved_invoice.DocNumber}: ${saved_invoice.TotalAmt}")
```

---

## Query and Filter Customers

```python
from quickbooks.objects.customer import Customer

# Get all active customers
active = Customer.filter(Active=True, qb=client)

# Search by name
results = Customer.where("DisplayName LIKE 'Acme%'", qb=client)

# Customers with balance
with_balance = Customer.where("Balance > '0'", qb=client)

# Paginated retrieval of all customers
all_customers = []
start = 1
while True:
    batch = Customer.all(
        start_position=start,
        max_results=100,
        order_by="DisplayName",
        qb=client,
    )
    if not batch:
        break
    all_customers.extend(batch)
    if len(batch) < 100:
        break
    start += 100

print(f"Total customers: {len(all_customers)}")

# Count
total = Customer.count(qb=client)
active_count = Customer.count("Active = true", qb=client)
print(f"Total: {total}, Active: {active_count}")
```

---

## Update a Record

```python
from quickbooks.objects.customer import Customer

# Get the customer
customer = Customer.get(42, qb=client)

# Modify fields
customer.CompanyName = "Acme Corp (Updated)"
customer.Notes = "Key account - handle with care"

# Save (Id exists, so this updates)
updated = customer.save(qb=client)
print(f"Updated: {updated.DisplayName}, SyncToken: {updated.SyncToken}")
```

---

## Create a Bill with Expense Lines

```python
from quickbooks.objects.bill import Bill
from quickbooks.objects.vendor import Vendor
from quickbooks.objects.detailline import (
    AccountBasedExpenseLine, AccountBasedExpenseLineDetail,
    ItemBasedExpenseLine, ItemBasedExpenseLineDetail,
)
from quickbooks.objects.base import Ref

# Get vendor reference
vendor = Vendor.get(1, qb=client)

bill = Bill()
bill.VendorRef = vendor.to_ref()
bill.DueDate = "2024-12-15"
bill.DocNumber = "BILL-001"

# Account-based expense line
line1 = AccountBasedExpenseLine()
line1.Amount = 150.00
line1.Description = "Office supplies"

detail1 = AccountBasedExpenseLineDetail()
account_ref = Ref()
account_ref.value = "7"  # Account ID for Office Expenses
account_ref.name = "Office Expenses"
detail1.AccountRef = account_ref
line1.AccountBasedExpenseLineDetail = detail1

bill.Line.append(line1)

# Item-based expense line
line2 = ItemBasedExpenseLine()
line2.Amount = 300.00

detail2 = ItemBasedExpenseLineDetail()
detail2.UnitPrice = 30.00
detail2.Qty = 10

item_ref = Ref()
item_ref.value = "5"
item_ref.name = "Printer Paper"
detail2.ItemRef = item_ref
line2.ItemBasedExpenseLineDetail = detail2

bill.Line.append(line2)

saved_bill = bill.save(qb=client)
print(f"Bill {saved_bill.DocNumber}: ${saved_bill.TotalAmt}")
```

---

## Record a Payment Against an Invoice

```python
from decimal import Decimal
from quickbooks.objects.payment import Payment, PaymentLine
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.customer import Customer
from quickbooks.objects.base import Ref, LinkedTxn

# Get the invoice
invoice = Invoice.get(42, qb=client)

# Create payment
payment = Payment()
payment.TotalAmt = Decimal(invoice.TotalAmt)

# Set customer
customer_ref = Ref()
customer_ref.value = invoice.CustomerRef.value
payment.CustomerRef = customer_ref

# Link to invoice
payment_line = PaymentLine()
payment_line.Amount = Decimal(invoice.TotalAmt)

linked_txn = invoice.to_linked_txn()
payment_line.LinkedTxn.append(linked_txn)

payment.Line.append(payment_line)

saved_payment = payment.save(qb=client)
print(f"Payment recorded: ${saved_payment.TotalAmt}")
```

**Gotchas**:
- **Undeposited Funds**: Without setting `DepositToAccountRef`, payments go to the Undeposited Funds account by default. Set `payment.DepositToAccountRef` to deposit directly to a bank account.
- **DocNumber may be ignored**: If `SalesFormsPrefs.CustomTxnNumbers` is off in QBO company settings, QBO auto-generates the DocNumber and silently ignores any value you set.

---

## Batch Create Customers

```python
from quickbooks.objects.customer import Customer
from quickbooks.batch import batch_create

customers = []
for name in ["Alpha Inc", "Beta LLC", "Gamma Corp", "Delta Ltd"]:
    c = Customer()
    c.DisplayName = name
    c.CompanyName = name
    customers.append(c)

results = batch_create(customers, qb=client)

print(f"Created: {len(results.successes)}")
for obj in results.successes:
    print(f"  {obj.DisplayName} (Id: {obj.Id})")

if results.faults:
    print(f"Failed: {len(results.faults)}")
    for fault in results.faults:
        print(f"  {fault.original_object.DisplayName}")
        for error in fault.Error:
            print(f"    {error.code}: {error.Message}")
```

---

## Attach a File to an Invoice

```python
from quickbooks.objects.attachable import Attachable
from quickbooks.objects.base import AttachableRef, Ref

# Create attachment with file
attachment = Attachable()
attachment.FileName = "receipt.pdf"
attachment.ContentType = "application/pdf"
attachment._FilePath = "/path/to/receipt.pdf"

# Link to an invoice
att_ref = AttachableRef()
entity_ref = Ref()
entity_ref.value = "42"
entity_ref.type = "Invoice"
att_ref.EntityRef = entity_ref
att_ref.IncludeOnSend = True
attachment.AttachableRef.append(att_ref)

saved = attachment.save(qb=client)
print(f"Attachment created: {saved.Id} - {saved.FileName}")
```

---

## Change Data Capture

```python
from quickbooks.cdc import change_data_capture
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.customer import Customer
from datetime import datetime, timedelta

# Get changes from the last 24 hours
yesterday = datetime.now() - timedelta(days=1)

cdc_response = change_data_capture(
    [Invoice, Customer],
    yesterday,
    qb=client,
)

# Process changed invoices
if hasattr(cdc_response, 'Invoice'):
    for invoice in cdc_response.Invoice:
        print(f"Invoice {invoice.Id} changed: ${invoice.TotalAmt}")

# Process changed customers
if hasattr(cdc_response, 'Customer'):
    for customer in cdc_response.Customer:
        print(f"Customer {customer.Id} changed: {customer.DisplayName}")
```

---

## Void an Invoice

```python
from quickbooks.objects.invoice import Invoice

# Get the invoice first (need current SyncToken)
invoice = Invoice.get(42, qb=client)
print(f"Voiding invoice {invoice.DocNumber}...")

invoice.void(qb=client)
print("Invoice voided successfully")
```

---

## Send Invoice via Email

```python
from quickbooks.objects.invoice import Invoice

invoice = Invoice.get(42, qb=client)

# Send to the customer's BillEmail on file
invoice.send(qb=client)

# Or send to a specific email address
invoice.send(qb=client, send_to="billing@example.com")
```

---

## Download Invoice PDF

```python
from quickbooks.objects.invoice import Invoice

invoice = Invoice.get(42, qb=client)
pdf_bytes = invoice.download_pdf(qb=client)

with open(f"invoice_{invoice.DocNumber}.pdf", "wb") as f:
    f.write(pdf_bytes)
print(f"Saved invoice PDF ({len(pdf_bytes)} bytes)")
```

---

## Create a Journal Entry

```python
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref

je = JournalEntry()
je.DocNumber = "JE-001"
je.TxnDate = "2024-06-15"

# Debit line
debit_line = JournalEntryLine()
debit_line.Amount = 1000.00
debit_line.Description = "Transfer to operating account"

debit_detail = JournalEntryLineDetail()
debit_detail.PostingType = "Debit"
debit_account = Ref()
debit_account.value = "1"  # Account ID
debit_detail.AccountRef = debit_account
debit_line.JournalEntryLineDetail = debit_detail

je.Line.append(debit_line)

# Credit line
credit_line = JournalEntryLine()
credit_line.Amount = 1000.00
credit_line.Description = "Transfer from savings"

credit_detail = JournalEntryLineDetail()
credit_detail.PostingType = "Credit"
credit_account = Ref()
credit_account.value = "2"  # Account ID
credit_detail.AccountRef = credit_account
credit_line.JournalEntryLineDetail = credit_detail

je.Line.append(credit_line)

saved_je = je.save(qb=client)
print(f"Journal Entry {saved_je.DocNumber}: ${saved_je.TotalAmt}")
```

---

## Error Handling

```python
from quickbooks.exceptions import (
    AuthorizationException,
    ObjectNotFoundException,
    ValidationException,
    QuickbooksException,
)

try:
    # Attempt an operation
    customer = Customer.get(99999, qb=client)
except ObjectNotFoundException as e:
    print(f"Customer not found: {e.detail}")
except AuthorizationException as e:
    print(f"Auth failed (code {e.error_code}): {e.message}")
    # Refresh token and retry
except ValidationException as e:
    print(f"Validation error: {e.message}")
    print(f"Detail: {e.detail}")
except QuickbooksException as e:
    print(f"Unexpected QBO error {e.error_code}: {e.message}")
```
