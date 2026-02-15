# Tax & Settings Objects

## TaxCode

```python
from quickbooks.objects.taxcode import TaxCode
```

Mixins: ReadMixin, ListMixin (get, all — **read-only, no save**)

TaxCodes track taxable/non-taxable status. Created via the TaxService endpoint, not directly.

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | Read-only |
| SyncToken | int | 0 | |
| Name | str | None | Read-only |
| Description | str | None | Read-only |
| Taxable | bool | None | Read-only |
| TaxGroup | bool | None | Read-only |
| Active | bool | True | |

### Nested Objects

| Field | Type |
|-------|------|
| SalesTaxRateList | TaxRateList |
| PurchaseTaxRateList | TaxRateList |

### TaxRateList

| Field | Type |
|-------|------|
| TaxRateDetail | list[TaxRateDetail] |

### TaxRateDetail

| Field | Type |
|-------|------|
| TaxTypeApplicable | str |
| TaxOrder | int |
| TaxRateRef | Ref |

---

## TaxRate

```python
from quickbooks.objects.taxrate import TaxRate
```

Mixins: ReadMixin, ListMixin (get, all — **read-only, no save**)

Created via TaxService, not directly.

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | Read-only |
| SyncToken | int | 0 | |
| Name | str | "" | Read-only |
| Description | str | "" | Read-only |
| RateValue | decimal | 0 | Read-only |
| SpecialTaxType | str | "" | |
| Active | bool | True | |
| DisplayType | str | "" | |
| EffectiveTaxRate | str | "" | |

### Nested Objects

| Field | Type |
|-------|------|
| AgencyRef | Ref |
| TaxReturnLineRef | Ref |

---

## TaxAgency

```python
from quickbooks.objects.taxagency import TaxAgency
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save)

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| SyncToken | int | 0 |
| DisplayName | str | "" |
| TaxRegistrationNumber | str | "" |
| TaxTrackedOnSales | bool | True |
| TaxTrackedOnPurchases | bool | False |

---

## TaxService

```python
from quickbooks.objects.taxservice import TaxService
```

Mixins: UpdateMixin (save only — **custom save method**)

Used to create new TaxCodes and TaxRates.

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| TaxCode | str | None | **Required** — name for the tax code |
| TaxCodeId | int | None | Read-only — set after save |
| Id | int | 0 | |

### List Fields

| Field | Type |
|-------|------|
| TaxRateDetails | list[TaxRateDetails] |

### TaxRateDetails

| Field | Type | Default |
|-------|------|---------|
| TaxRateName | str | None |
| TaxRateId | int | None |
| RateValue | str | None |
| TaxAgencyId | str | None |
| TaxApplicableOn | str | "Sales" |

### Usage

```python
from quickbooks.objects.taxservice import TaxService, TaxRateDetails

tax_service = TaxService()
tax_service.TaxCode = "State Sales Tax"

detail = TaxRateDetails()
detail.TaxRateName = "CA Sales Tax"
detail.RateValue = "7.25"
detail.TaxAgencyId = "1"
detail.TaxApplicableOn = "Sales"
tax_service.TaxRateDetails.append(detail)

result = tax_service.save(qb=client)
print(tax_service.TaxCodeId)  # New TaxCode ID
```

**Note**: TaxService uses the `TaxService/Taxcode` endpoint. Tax agencies referenced must already exist.

---

## PaymentMethod

```python
from quickbooks.objects.paymentmethod import PaymentMethod
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| SyncToken | int | 0 |
| Name | str | "" |
| Type | str | "" |
| Active | bool | True |

**Delete**: Set `Active = False` and save (soft delete).

---

## CompanyInfo

```python
from quickbooks.objects.company_info import CompanyInfo
```

Mixins: `QuickbooksManagedObject` (get, save, to_ref — **no all()**)

**Note**: There is only one CompanyInfo per company. Use `CompanyInfo.get(1, qb=client)` to retrieve it.

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| CompanyName | str | "" |
| LegalName | str | "" |
| CompanyStartDate | str | "" |
| FiscalYearStartMonth | str | "" |
| Country | str | "" |
| SupportedLanguages | str | "" |

### Nested Objects

| Field | Type |
|-------|------|
| CompanyAddr | Address |
| CustomerCommunicationAddr | Address |
| LegalAddr | Address |
| PrimaryPhone | PhoneNumber |
| Email | EmailAddress |
| WebAddr | WebAddress |
| MetaData | MetaData |

---

## Preferences

```python
from quickbooks.objects.preferences import Preferences
```

Mixins: PrefMixin, UpdateNoIdMixin, QuickbooksTransactionEntity

**Special**: `Preferences.get(qb=client)` — no `id` parameter needed.

### Sub-Preference Classes

| Field | Type |
|-------|------|
| EmailMessagesPrefs | EmailMessagesPrefs |
| ProductAndServicesPrefs | ProductAndServicesPrefs |
| ReportPrefs | ReportPrefs |
| AccountingInfoPrefs | AccountingInfoPrefs |
| SalesFormsPrefs | SalesFormsPrefs |
| VendorAndPurchasesPrefs | VendorAndPurchasesPrefs |
| TaxPrefs | TaxPrefs |
| OtherPrefs | OtherPrefs |
| TimeTrackingPrefs | TimeTrackingPrefs |
| CurrencyPrefs | CurrencyPrefs |

### EmailMessagesPrefs

| Field | Type |
|-------|------|
| InvoiceMessage | EmailMessageType (Message, Subject) |
| EstimateMessage | EmailMessageType |
| SalesReceiptMessage | EmailMessageType |
| StatementMessage | EmailMessageType |

### ProductAndServicesPrefs

| Field | Type | Default |
|-------|------|---------|
| QuantityWithPriceAndRate | bool | True |
| ForPurchase | bool | True |
| QuantityOnHand | bool | True |
| ForSales | bool | True |
| RevenueRecognition | bool | True |
| RevenueRecognitionFrequency | str | "" |

### ReportPrefs

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| ReportBasis | str | "Accrual" | "Accrual" or "Cash" |
| CalcAgingReportFromTxnDate | bool | False | Read-only |

### AccountingInfoPrefs

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| FirstMonthOfFiscalYear | str | "January" | Read-only |
| UseAccountNumbers | bool | True | Read-only |
| TaxYearMonth | str | "January" | Read-only |
| ClassTrackingPerTxn | bool | False | |
| TrackDepartments | bool | False | |
| TaxForm | str | "6" | |
| CustomerTerminology | str | "" | Clients/Customers/Donors/etc. |
| BookCloseDate | str | "" | |
| DepartmentTerminology | str | "" | Business/Department/Division/etc. |
| ClassTrackingPerTxnLine | bool | True | |

### SalesFormsPrefs

Key fields: ETransactionPaymentEnabled, CustomTxnNumbers, AllowShipping, AllowServiceDate, DefaultCustomerMessage, AllowEstimates, AllowDiscount, AllowDeposit, AutoApplyPayments, AutoApplyCredit, UsingPriceLevels, UsingProgressInvoicing

Nested: DefaultTerms (Ref), SalesEmailBcc (EmailAddress), SalesEmailCc (EmailAddress), CustomField (PreferencesCustomFieldGroup)

### VendorAndPurchasesPrefs

| Field | Type | Default |
|-------|------|---------|
| BillableExpenseTracking | bool | True |
| TrackingByCustomer | bool | True |
| TPAREnabled | bool | True |

Nested: DefaultTerms (Ref), DefaultMarkupAccount (Ref), POCustomField (PreferencesCustomFieldGroup)

### TaxPrefs

| Field | Type |
|-------|------|
| TaxGroupCodeRef | Ref |
| UsingSalesTax | bool |
| PartnerTaxEnabled | bool |

### TimeTrackingPrefs

| Field | Type | Default |
|-------|------|---------|
| WorkWeekStartDate | str | "" |
| MarkTimeEntriesBillable | bool | True |
| ShowBillRateToAll | bool | False |
| UseServices | bool | True |
| BillCustomers | bool | True |

### CurrencyPrefs

| Field | Type |
|-------|------|
| HomeCurrency | Ref |
| MultiCurrencyEnabled | bool |

### OtherPrefs

Contains a list of `NameValue` pairs (Name: str, Value: str).

---

## Attachable

```python
from quickbooks.objects.attachable import Attachable
```

Mixins: DeleteMixin, `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, delete, to_ref)

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| FileName | str | None | |
| _FilePath | str | "" | Private — path to file for upload |
| _FileBytes | bytes | None | Private — raw bytes for upload |
| Note | str | "" | |
| FileAccessUri | str | None | Read-only |
| TempDownloadUri | str | None | Read-only |
| Size | int | None | Read-only |
| ContentType | str | None | Required for file uploads |
| Category | str | None | |
| Lat | str | None | |
| Long | str | None | |
| PlaceName | str | None | |
| ThumbnailFileAccessUri | str | None | Read-only |
| ThumbnailTempDownloadUri | str | None | Read-only |

### List Fields

| Field | Type |
|-------|------|
| AttachableRef | list[AttachableRef] |

### AttachableRef

| Field | Type |
|-------|------|
| LineInfo | str |
| IncludeOnSend | bool |
| Inactive | bool |
| NoRefOnly | bool |
| EntityRef | Ref |
| CustomField | list[CustomField] |

### Custom save() behavior

- `_FilePath` and `_FileBytes` are mutually exclusive (raises ValueError if both set)
- File upload uses multipart form data with base64 encoding
- On first save with a file, response wraps in `AttachableResponse[0].Attachable`
- On subsequent saves (update), response uses `Attachable` directly

---

## RecurringTransaction

```python
from quickbooks.objects.recurringtransaction import RecurringTransaction
```

Mixins: ReadMixin, UpdateNoIdMixin, ListMixin, DeleteNoIdMixin (get, all, save, delete)

### Supported Transaction Types (12 variants)

| Class | Base |
|-------|------|
| RecurringBill | Bill |
| RecurringPurchase | Purchase |
| RecurringCreditMemo | CreditMemo |
| RecurringDeposit | Deposit |
| RecurringEstimate | Estimate |
| RecurringInvoice | Invoice |
| RecurringJournalEntry | JournalEntry |
| RecurringRefundReceipt | RefundReceipt |
| RecurringSalesReceipt | SalesReceipt |
| RecurringTransfer | Transfer |
| RecurringVendorCredit | VendorCredit |
| RecurringPurchaseOrder | PurchaseOrder |

Each recurring variant inherits all fields from its base class plus adds `RecurringInfo` and `RecurDataRef`.

### ScheduleInfo

| Field | Type |
|-------|------|
| StartDate | str |
| EndDate | str |
| DaysBefore | int |
| MaxOccurrences | int |
| RemindDays | int |
| IntervalType | str |
| NumInterval | int |
| DayOfMonth | int |
| DayOfWeek | str |
| MonthOfYear | str |
| WeekOfMonth | int |
| NextDate | str |
| PreviousDate | str |

### RecurringInfo

| Field | Type | Default |
|-------|------|---------|
| RecurType | str | "Automated" |
| Name | str | "" |
| Active | bool | False |
| ScheduleInfo | ScheduleInfo | None |
