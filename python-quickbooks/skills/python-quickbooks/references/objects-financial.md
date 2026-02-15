# Financial Document Objects

## Invoice

```python
from quickbooks.objects.invoice import Invoice
```

Mixins: DeleteMixin, QuickbooksPdfDownloadable, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, SendMixin, VoidMixin

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| Deposit | decimal | 0 | |
| Balance | decimal | 0 | Read-only |
| AllowIPNPayment | bool | True | |
| AllowOnlineCreditCardPayment | bool | False | |
| AllowOnlineACHPayment | bool | False | |
| DocNumber | str | None | |
| PrivateNote | str | "" | |
| DueDate | str | "" | |
| ShipDate | str | "" | |
| TrackingNum | str | "" | |
| TotalAmt | str | "" | Read-only |
| TxnDate | str | "" | |
| ApplyTaxAfterDiscount | bool | False | |
| PrintStatus | str | "NotSet" | |
| EmailStatus | str | "NotSet" | |
| ExchangeRate | decimal | 1 | |
| GlobalTaxCalculation | str | "TaxExcluded" | |
| InvoiceLink | str | "" | |
| HomeBalance | decimal | 0 | |
| HomeTotalAmt | decimal | 0 | |
| FreeFormAddress | bool | False | |
| EInvoiceStatus | str | None | |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| DepartmentRef | Ref |
| CurrencyRef | Ref |
| CustomerRef | Ref |
| ClassRef | Ref |
| SalesTermRef | Ref |
| ShipMethodRef | Ref |
| DepositToAccountRef | Ref |
| BillAddr | Address |
| ShipAddr | Address |
| TxnTaxDetail | TxnTaxDetail |
| BillEmail | EmailAddress |
| BillEmailCc | EmailAddress |
| BillEmailBcc | EmailAddress |
| CustomerMemo | CustomerMemo |
| DeliveryInfo | DeliveryInfo |
| RecurDataRef | Ref |
| TaxExemptionRef | Ref |
| MetaData | MetaData |

### List Fields (list_dict)

| Field | Type |
|-------|------|
| CustomField | CustomField |
| Line | DetailLine |
| LinkedTxn | LinkedTxn |

### Detail Types (detail_dict)

| DetailType Value | Python Class |
|------------------|-------------|
| SalesItemLineDetail | SalesItemLine |
| SubTotalLineDetail | SubtotalLine |
| DiscountLineDetail | DiscountLine |
| DescriptionOnly | DescriptionOnlyLine |
| GroupLineDetail | GroupLine |

### Special Methods

- `to_ref()` — name=DocNumber
- `to_linked_txn()` — TxnType="Invoice"
- `email_sent` (property) — True if EmailStatus == "EmailSent"

---

## Bill

```python
from quickbooks.objects.bill import Bill
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| DueDate | str | "" |
| Balance | decimal | 0 |
| TotalAmt | str | "" |
| TxnDate | str | "" |
| DocNumber | str | "" |
| PrivateNote | str | "" |
| ExchangeRate | decimal | 0 |
| GlobalTaxCalculation | str | None |

### Nested Objects

| Field | Type |
|-------|------|
| SalesTermRef | Ref |
| CurrencyRef | Ref |
| APAccountRef | Ref |
| VendorRef | Ref |
| AttachableRef | Ref |
| DepartmentRef | Ref |
| TxnTaxDetail | TxnTaxDetail |
| VendorAddr | Address |

### Detail Types: ItemBasedExpenseLine, AccountBasedExpenseLine, TDSLine

---

## BillPayment

```python
from quickbooks.objects.billpayment import BillPayment
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, VoidMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| PayType | str | "" |
| TotalAmt | decimal | 0 |
| PrivateNote | str | "" |
| DocNumber | str | "" |

### Nested Objects

| Field | Type |
|-------|------|
| VendorRef | Ref |
| CheckPayment | CheckPayment |
| CreditCardPayment | BillPaymentCreditCard |
| APAccountRef | Ref |
| DepartmentRef | Ref |
| CurrencyRef | Ref |

### List Fields

| Field | Type |
|-------|------|
| Line | BillPaymentLine |

### BillPaymentLine

| Field | Type |
|-------|------|
| Amount | decimal |
| LinkedTxn | list[LinkedTxn] |

### CheckPayment

| Field | Type |
|-------|------|
| PrintStatus | str ("NotSet") |
| BankAccountRef | Ref |

---

## Payment

```python
from quickbooks.objects.payment import Payment
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, VoidMixin

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| PaymentRefNum | str | None | |
| TotalAmt | decimal | None | |
| UnappliedAmt | decimal | None | Read-only |
| ExchangeRate | decimal | None | |
| TxnDate | str | None | |
| TxnSource | str | None | |
| PrivateNote | str | None | |
| TxnStatus | str | None | |
| TransactionLocationType | str | None | Minor version 4+ |

### Nested Objects

| Field | Type |
|-------|------|
| ARAccountRef | Ref |
| CustomerRef | Ref |
| PaymentMethodRef | Ref |
| DepositToAccountRef | Ref |
| CurrencyRef | Ref |
| CreditCardPayment | CreditCardPayment |
| TaxExemptionRef | Ref |
| MetaData | MetaData |

### List Fields

| Field | Type |
|-------|------|
| Line | PaymentLine |

### PaymentLine

| Field | Type |
|-------|------|
| Amount | decimal |
| LinkedTxn | list[LinkedTxn] |

---

## Estimate

```python
from quickbooks.objects.estimate import Estimate
```

Mixins: DeleteMixin, QuickbooksPdfDownloadable, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, SendMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| DocNumber | str | None |
| TxnDate | str | None |
| TxnStatus | str | None |
| PrivateNote | str | None |
| TotalAmt | decimal | 0 |
| ExchangeRate | decimal | 1 |
| ApplyTaxAfterDiscount | bool | False |
| PrintStatus | str | "NotSet" |
| EmailStatus | str | "NotSet" |
| DueDate | str | None |
| ShipDate | str | None |
| ExpirationDate | str | None |
| AcceptedBy | str | None |
| AcceptedDate | str | None |
| GlobalTaxCalculation | str | "TaxExcluded" |
| TrackingNum | str | "" |

### Nested Objects

| Field | Type |
|-------|------|
| BillAddr | Address |
| ShipAddr | Address |
| ShipFromAddr | Address |
| CustomerRef | Ref |
| ProjectRef | Ref |
| TxnTaxDetail | TxnTaxDetail |
| CustomerMemo | CustomerMemo |
| BillEmail | EmailAddress |
| DepartmentRef | Ref |
| CurrencyRef | Ref |
| ClassRef | Ref |
| SalesTermRef | Ref |
| ShipMethodRef | Ref |

### Detail Types: SalesItemLine, GroupLine, DescriptionOnlyLine, DiscountLine, SubtotalLine

---

## Purchase

```python
from quickbooks.objects.purchase import Purchase
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

Three types: Cash, Check, Credit Card (set via `PaymentType`).

### Fields

| Field | Type | Default |
|-------|------|---------|
| DocNumber | str | "" |
| TxnDate | str | "" |
| ExchangeRate | decimal | 1 |
| PrivateNote | str | "" |
| PaymentType | str | "" |
| Credit | bool | False |
| TotalAmt | decimal | 0 |
| PrintStatus | str | "NeedToPrint" |
| PurchaseEx | - | None |
| TxnSource | str | None |
| GlobalTaxCalculation | str | "TaxExcluded" |

### Nested Objects

| Field | Type |
|-------|------|
| TxnTaxDetail | TxnTaxDetail |
| DepartmentRef | Ref |
| AccountRef | Ref |
| EntityRef | Ref |
| CurrencyRef | Ref |
| PaymentMethodRef | Ref |
| RemitToAddr | Address |

### Detail Types: AccountBasedExpenseLine, ItemBasedExpenseLine, TDSLine

---

## PurchaseOrder

```python
from quickbooks.objects.purchaseorder import PurchaseOrder
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, SendMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| POStatus | str | None |
| DocNumber | str | None |
| TxnDate | str | None |
| PrivateNote | str | None |
| TotalAmt | decimal | 0 |
| DueDate | str | None |
| ExchangeRate | decimal | 1 |
| GlobalTaxCalculation | str | "TaxExcluded" |
| Memo | str | None |

### Nested Objects

VendorAddr, ShipAddr, VendorRef, APAccountRef, AttachableRef, ClassRef, SalesTermRef, ShipMethodRef, TaxCodeRef, CurrencyRef, TxnTaxDetail (all Ref or Address types)

### Detail Types: ItemBasedExpenseLine, AccountBasedExpenseLine, TDSLine

---

## SalesReceipt

```python
from quickbooks.objects.salesreceipt import SalesReceipt
```

Mixins: DeleteMixin, QuickbooksPdfDownloadable, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin, VoidMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| DocNumber | str | "" |
| TxnDate | str | "" |
| PrivateNote | str | "" |
| ShipDate | str | "" |
| TrackingNum | str | "" |
| TotalAmt | decimal | 0 |
| PrintStatus | str | "NotSet" |
| EmailStatus | str | "NotSet" |
| Balance | decimal | 0 |
| PaymentRefNum | str | "" |
| ApplyTaxAfterDiscount | bool | False |
| ExchangeRate | decimal | 1 |
| GlobalTaxCalculation | str | "TaxExcluded" |

### Nested Objects

DepartmentRef, CurrencyRef, TxnTaxDetail, DepositToAccountRef, CustomerRef, BillAddr, ShipAddr, ClassRef, BillEmail, PaymentMethodRef, ShipMethodRef

**Warning — empty `detail_dict`**: SalesReceipt has `detail_dict = {}` (empty). When reading SalesReceipts from the API, all line items deserialize as generic `DetailLine` objects instead of typed classes like `SalesItemLine`. You lose access to typed detail attributes (e.g., `SalesItemLineDetail.UnitPrice`). Workaround: manually check each line's `DetailType` string and access the raw detail dict.

---

## CreditMemo

```python
from quickbooks.objects.creditmemo import CreditMemo
```

Mixins: DeleteMixin, QuickbooksTransactionEntity, QuickbooksManagedObject, LinkedTxnMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| RemainingCredit | decimal | 0 |
| ExchangeRate | decimal | 0 |
| DocNumber | str | "" |
| TxnDate | str | "" |
| PrivateNote | str | "" |
| TotalAmt | decimal | 0 |
| ApplyTaxAfterDiscount | str | "" |
| PrintStatus | str | "NotSet" |
| EmailStatus | str | "NotSet" |
| Balance | decimal | 0 |
| GlobalTaxCalculation | str | "TaxExcluded" |

### Detail Types: SalesItemLine, SubtotalLine, DiscountLine, DescriptionOnlyLine

---

## RefundReceipt

```python
from quickbooks.objects.refundreceipt import RefundReceipt
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

DocNumber, TotalAmt, ApplyTaxAfterDiscount, PrintStatus, Balance, PaymentRefNum, TxnDate, ExchangeRate, PrivateNote, PaymentType, GlobalTaxCalculation

### Nested Objects

DepartmentRef, CurrencyRef, TxnTaxDetail, DepositToAccountRef, CustomerRef, BillAddr, ShipAddr, ClassRef, BillEmail, PaymentMethodRef, CheckPayment (RefundReceiptCheckPayment), CreditCardPayment, CustomerMemo

**Warning — empty `detail_dict`**: Like SalesReceipt, RefundReceipt has `detail_dict = {}`. See SalesReceipt warning above.

---

## VendorCredit

```python
from quickbooks.objects.vendorcredit import VendorCredit
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

DocNumber, TxnDate, PrivateNote, TotalAmt, ExchangeRate, GlobalTaxCalculation

### Nested Objects

VendorRef, APAccountRef, DepartmentRef, CurrencyRef

### Detail Types: AccountBasedExpenseLine, ItemBasedExpenseLine, TDSLine

---

## Deposit

```python
from quickbooks.objects.deposit import Deposit
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| TotalAmt | decimal | 0 |
| HomeTotalAmt | decimal | 0 |
| TxnDate | str | "" |
| DocNumber | str | "" |
| ExchangeRate | decimal | 1 |
| GlobalTaxCalculation | str | "TaxExcluded" |
| PrivateNote | str | "" |
| TxnStatus | str | "" |
| TxnSource | str | None |

### Nested Objects

DepositToAccountRef, DepartmentRef, CurrencyRef, AttachableRef, CashBack (CashBackInfo)

### Line: DepositLine

**Note**: `DepositLine` extends `QuickbooksBaseObject` directly, NOT `DetailLine`. It reimplements the same base fields (`Id`, `LineNum`, `Description`, `Amount`, `DetailType`, `LinkedTxn`) manually.

| Field | Type |
|-------|------|
| Id | int |
| LineNum | int |
| Description | str |
| Amount | decimal |
| DetailType | str ("DepositLineDetail") |
| DepositLineDetail | DepositLineDetail |
| LinkedTxn | list |

### DepositLineDetail

| Field | Type |
|-------|------|
| CheckNum | str |
| TxnType | str |
| Entity | Ref |
| ClassRef | Ref |
| AccountRef | Ref |
| PaymentMethodRef | Ref |

---

## Transfer

```python
from quickbooks.objects.transfer import Transfer
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| Amount | decimal | 0 |
| TxnDate | str | None |
| PrivateNote | str | None |
| TxnSource | str | None |

### Nested Objects

| Field | Type |
|-------|------|
| FromAccountRef | Ref |
| ToAccountRef | Ref |

---

## JournalEntry

```python
from quickbooks.objects.journalentry import JournalEntry
```

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| Adjustment | bool | False |
| TxnDate | str | "" |
| DocNumber | str | "" |
| PrivateNote | str | "" |
| TotalAmt | decimal | 0 |
| ExchangeRate | decimal | 1 |

### Nested Objects

| Field | Type |
|-------|------|
| TxnTaxDetail | TxnTaxDetail |
| CurrencyRef | Ref |

### Detail Types: DescriptionOnlyLine, JournalEntryLine

### JournalEntryLine

A specialized DetailLine with `DetailType = "JournalEntryLineDetail"`.

### JournalEntryLineDetail

| Field | Type |
|-------|------|
| PostingType | str ("Debit" or "Credit") |
| TaxApplicableOn | str ("Sales") |
| TaxAmount | decimal |
| BillableStatus | str |
| Entity | Entity (contains EntityRef: Ref, Type: str) |
| AccountRef | Ref |
| ClassRef | Ref |
| DepartmentRef | Ref |
| TaxCodeRef | Ref |

---

## CreditCardPayment (Entity)

```python
from quickbooks.objects.creditcardpayment_entity import CreditCardPayment
```

**Note**: This is distinct from `quickbooks.objects.creditcardpayment.CreditCardPayment` (a nested object used inside Payment/SalesReceipt). This entity records balance payments to credit card accounts.

Mixins: DeleteMixin, QuickbooksManagedObject, QuickbooksTransactionEntity, LinkedTxnMixin

### Fields

| Field | Type | Default |
|-------|------|---------|
| TxnDate | str | None |
| Amount | decimal | 0 |
| PrivateNote | str | None |
| Memo | str | None |
| PrintStatus | str | None |
| CheckNum | str | None |

### Nested Objects

| Field | Type |
|-------|------|
| BankAccountRef | Ref |
| CreditCardAccountRef | Ref |
| VendorRef | Ref |
| MetaData | MetaData |

**Special**: `qbo_json_object_name = "CreditCardPaymentTxn"` — the JSON object name doesn't match the endpoint name.

---

## Tax-Related Nested Objects

### TxnTaxDetail

Used on Invoice, Bill, Estimate, Purchase, PurchaseOrder, SalesReceipt, JournalEntry, etc.

| Field | Type |
|-------|------|
| TotalTax | decimal |
| TxnTaxCodeRef | Ref |
| TaxLine | list[TaxLine] |

### TaxLine

| Field | Type |
|-------|------|
| Amount | decimal |
| DetailType | str |
| TaxLineDetail | TaxLineDetail |

### TaxLineDetail

| Field | Type |
|-------|------|
| PercentBased | bool |
| TaxPercent | decimal |
| NetAmountTaxable | decimal |
| TaxRateRef | Ref |
