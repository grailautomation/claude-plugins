# Object Capabilities

## Import Paths & Capabilities

### Entities

| Object | Import Path | get | all | save | delete | void | send | pdf | to_ref |
|--------|------------|-----|-----|------|--------|------|------|-----|--------|
| Customer | `quickbooks.objects.customer.Customer` | Y | Y | Y | - | - | - | - | Y |
| Vendor | `quickbooks.objects.vendor.Vendor` | Y | Y | Y | - | - | - | - | Y |
| Employee | `quickbooks.objects.employee.Employee` | Y | Y | Y | - | - | - | - | Y |
| Department | `quickbooks.objects.department.Department` | Y | Y | Y | - | - | - | - | Y |
| CompanyCurrency | `quickbooks.objects.companycurrency.CompanyCurrency` | Y | Y | Y | - | - | - | - | Y |
| CustomerType | `quickbooks.objects.customertype.CustomerType` | Y | Y | - | - | - | - | - | - |

### Financial Documents

| Object | Import Path | get | all | save | delete | void | send | pdf | to_ref |
|--------|------------|-----|-----|------|--------|------|------|-----|--------|
| Invoice | `quickbooks.objects.invoice.Invoice` | Y | Y | Y | Y | Y | Y | Y | Y |
| Bill | `quickbooks.objects.bill.Bill` | Y | Y | Y | Y | - | - | - | Y |
| BillPayment | `quickbooks.objects.billpayment.BillPayment` | Y | Y | Y | Y | Y | - | - | - |
| Payment | `quickbooks.objects.payment.Payment` | Y | Y | Y | Y | Y | - | - | - |
| Estimate | `quickbooks.objects.estimate.Estimate` | Y | Y | Y | Y | - | Y | Y | - |
| Purchase | `quickbooks.objects.purchase.Purchase` | Y | Y | Y | Y | - | - | - | - |
| PurchaseOrder | `quickbooks.objects.purchaseorder.PurchaseOrder` | Y | Y | Y | Y | - | Y | - | - |
| SalesReceipt | `quickbooks.objects.salesreceipt.SalesReceipt` | Y | Y | Y | Y | Y | - | Y | - |
| CreditMemo | `quickbooks.objects.creditmemo.CreditMemo` | Y | Y | Y | Y | - | - | - | Y |
| RefundReceipt | `quickbooks.objects.refundreceipt.RefundReceipt` | Y | Y | Y | Y | - | - | - | - |
| VendorCredit | `quickbooks.objects.vendorcredit.VendorCredit` | Y | Y | Y | Y | - | - | - | - |
| Deposit | `quickbooks.objects.deposit.Deposit` | Y | Y | Y | Y | - | - | - | - |
| Transfer | `quickbooks.objects.transfer.Transfer` | Y | Y | Y | Y | - | - | - | - |
| JournalEntry | `quickbooks.objects.journalentry.JournalEntry` | Y | Y | Y | Y | - | - | - | - |
| CreditCardPayment | `quickbooks.objects.creditcardpayment_entity.CreditCardPayment` | Y | Y | Y | Y | - | - | - | - |

### Items & Accounting

| Object | Import Path | get | all | save | delete | void | send | pdf | to_ref |
|--------|------------|-----|-----|------|--------|------|------|-----|--------|
| Item | `quickbooks.objects.item.Item` | Y | Y | Y | - | - | - | - | Y |
| Account | `quickbooks.objects.account.Account` | Y | Y | Y | - | - | - | - | Y |
| Term | `quickbooks.objects.term.Term` | Y | Y | Y | - | - | - | - | Y |
| Class | `quickbooks.objects.trackingclass.Class` | Y | Y | Y | - | - | - | - | Y |
| Budget | `quickbooks.objects.budget.Budget` | Y | Y | - | - | - | - | - | - |
| TimeActivity | `quickbooks.objects.timeactivity.TimeActivity` | Y | Y | Y | Y | - | - | - | - |
| ExchangeRate | `quickbooks.objects.exchangerate.ExchangeRate` | - | Y | Y* | - | - | - | - | - |

*ExchangeRate uses `UpdateNoIdMixin` — `save()` always updates, never creates.

### Tax & Settings

| Object | Import Path | get | all | save | delete | void | send | pdf | to_ref |
|--------|------------|-----|-----|------|--------|------|------|-----|--------|
| TaxCode | `quickbooks.objects.taxcode.TaxCode` | Y | Y | - | - | - | - | - | Y |
| TaxRate | `quickbooks.objects.taxrate.TaxRate` | Y | Y | - | - | - | - | - | - |
| TaxAgency | `quickbooks.objects.taxagency.TaxAgency` | Y | Y | Y | - | - | - | - | - |
| TaxService | `quickbooks.objects.taxservice.TaxService` | - | - | Y* | - | - | - | - | - |
| PaymentMethod | `quickbooks.objects.paymentmethod.PaymentMethod` | Y | Y | Y | - | - | - | - | Y |
| CompanyInfo | `quickbooks.objects.company_info.CompanyInfo` | Y | - | Y | - | - | - | - | Y |
| Preferences | `quickbooks.objects.preferences.Preferences` | Y** | - | Y*** | - | - | - | - | - |
| Attachable | `quickbooks.objects.attachable.Attachable` | Y | Y | Y* | Y | - | - | - | Y |
| RecurringTransaction | `quickbooks.objects.recurringtransaction.RecurringTransaction` | Y | Y | Y*** | Y*** | - | - | - | - |

*TaxService has custom save(). Attachable has custom save() with file upload.
**Preferences.get() takes no id parameter.
***Uses UpdateNoIdMixin/DeleteNoIdMixin.

## Mixin Inheritance Summary

| Mixin | Provides | Objects Using It |
|-------|----------|-----------------|
| `ReadMixin` | `get(id)` | All readable objects |
| `ListMixin` | `all()`, `filter()`, `where()`, `query()`, `count()`, `choose()` | All listable objects |
| `UpdateMixin` | `save()` (create if no Id, update if Id) | Most writable objects |
| `UpdateNoIdMixin` | `save()` (always updates) | ExchangeRate, Preferences, RecurringTransaction |
| `DeleteMixin` | `delete()` (sends Id+SyncToken) | Most deletable objects |
| `DeleteNoIdMixin` | `delete()` (sends full JSON) | RecurringTransaction |
| `VoidMixin` | `void()` | Invoice, Payment, BillPayment, SalesReceipt |
| `SendMixin` | `send()` | Invoice, Estimate, PurchaseOrder |
| `QuickbooksPdfDownloadable` | `download_pdf()` | Invoice, Estimate, SalesReceipt |
| `LinkedTxnMixin` | `to_linked_txn()` | Most transaction objects |
| `PrefMixin` | `get()` (no id) | Preferences |
| `ToJsonMixin` | `to_json()` | All objects (via QuickbooksBaseObject) |
| `FromJsonMixin` | `from_json()` | All objects (via QuickbooksBaseObject) |
| `ToDictMixin` | `to_dict()` | All objects (via QuickbooksBaseObject) |

## Base Classes

| Base Class | Inherits | Description |
|-----------|----------|-------------|
| `QuickbooksBaseObject` | ToJsonMixin, FromJsonMixin, ToDictMixin | Base for all objects |
| `QuickbooksTransactionEntity` | QuickbooksBaseObject | Adds Id, SyncToken, sparse, domain |
| `QuickbooksManagedObject` | QuickbooksBaseObject, ReadMixin, ListMixin, UpdateMixin | Full CRUD |
| `QuickbooksReadOnlyObject` | QuickbooksBaseObject, ReadMixin, ListMixin | Read-only |
