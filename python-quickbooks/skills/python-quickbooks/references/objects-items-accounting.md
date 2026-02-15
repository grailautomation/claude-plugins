# Items & Accounting Objects

## Item

```python
from quickbooks.objects.item import Item
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

### Types

- **Inventory** — tracks merchandise purchased, stocked, and re-sold
- **Service** — tracks services charged, and non-inventory merchandise

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| Name | str | "" | |
| Description | str | "" | |
| Active | bool | True | |
| SubItem | bool | False | |
| FullyQualifiedName | str | "" | Read-only |
| Taxable | bool | False | |
| SalesTaxIncluded | bool | None | |
| UnitPrice | decimal | 0 | |
| Type | str | "" | "Inventory" or "Service" |
| Level | int | None | Read-only |
| PurchaseDesc | str | None | |
| PurchaseTaxIncluded | bool | None | |
| PurchaseCost | decimal | None | |
| TrackQtyOnHand | bool | False | |
| QtyOnHand | decimal | None | |
| InvStartDate | str | None | |
| AbatementRate | decimal | None | Minor version 3+ |
| ReverseChargeRate | decimal | None | Minor version 3+ |
| ServiceType | str | None | Minor version 3+ |
| ItemCategoryType | str | None | Minor version 3+ |
| Sku | str | None | Minor version 4+ |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| AssetAccountRef | Ref |
| ExpenseAccountRef | Ref |
| IncomeAccountRef | Ref |
| ParentRef | Ref |
| SalesTaxCodeRef | Ref |
| PurchaseTaxCodeRef | Ref |

**Note**: `Item.all()` automatically includes `SELECT *, Sku` to retrieve the SKU field.

---

## Account

```python
from quickbooks.objects.account import Account
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

Five basic types: Asset, Liability, Revenue (Income), Expense, Equity.

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| Name | str | "" | |
| SubAccount | bool | False | |
| FullyQualifiedName | str | "" | |
| Active | bool | True | |
| Classification | str | None | Read-only |
| AccountType | str | None | Required for create |
| AccountSubType | str | "" | |
| Description | str | "" | |
| AcctNum | str | "" | |
| CurrentBalance | decimal | None | Read-only |
| CurrentBalanceWithSubAccounts | decimal | None | Read-only |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| CurrencyRef | Ref |
| ParentRef | Ref |
| TaxCodeRef | Ref |

### to_ref()

Returns a Ref with `name=FullyQualifiedName`.

**Delete**: Set `Active = False` and save (soft delete, record hidden but references intact).

---

## Term

```python
from quickbooks.objects.term import Term
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

Represents sales terms (e.g., Net 30, 2%/15 Net 60).

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| Name | str | "" | |
| Active | bool | True | |
| Type | str | None | Read-only |
| DiscountPercent | decimal | None | |
| DueDays | int | None | |
| DiscountDays | int | None | |
| DayOfMonthDue | int | None | |
| DueNextMonthDays | int | None | |
| DiscountDayOfMonth | int | None | |

---

## Class

```python
from quickbooks.objects.trackingclass import Class
```

**Note**: Import path is `trackingclass`, not `class` (reserved Python keyword).

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

Classes track different business segments and are applied to **individual line items** (vs Department which applies to entire transactions).

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| SyncToken | int | 0 |
| Name | str | "" |
| SubClass | bool | False |
| FullyQualifiedName | str | "" |
| Active | bool | True |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| ParentRef | Ref |

---

## Budget

```python
from quickbooks.objects.budget import Budget
```

Mixins: `QuickbooksReadOnlyObject`, `QuickbooksTransactionEntity` (get, all — **read-only**)

**Note**: Budgets cannot be created or updated via the QBO API.

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| SyncToken | int | 0 |
| Name | str | "" |
| StartDate | str | "" |
| EndDate | str | "" |
| BudgetType | str | "" |
| BudgetEntryType | str | "" |
| Active | bool | True |

### List Fields

| Field | Type |
|-------|------|
| BudgetDetail | list[BudgetDetail] |

### BudgetDetail

| Field | Type |
|-------|------|
| BudgetDate | str |
| Amount | decimal |
| AccountRef | Ref |
| CustomerRef | Ref |
| ClassRef | Ref |
| DepartmentRef | Ref |

---

## TimeActivity

```python
from quickbooks.objects.timeactivity import TimeActivity
```

Mixins: DeleteMixin, `QuickbooksManagedObject`, `QuickbooksTransactionEntity`, LinkedTxnMixin (get, all, filter, save, delete)

Records time worked by a vendor or employee.

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| NameOf | str | "" | **Required** — "Vendor" or "Employee" |
| TxnDate | str | None | |
| BillableStatus | str | None | |
| Taxable | bool | False | |
| HourlyRate | decimal | None | |
| Hours | int | None | |
| Minutes | int | None | |
| BreakHours | int | None | |
| BreakMinutes | int | None | |
| StartTime | str | None | |
| EndTime | str | None | |
| Description | str | None | |
| CostRate | decimal | None | |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| VendorRef | Ref |
| CustomerRef | Ref |
| DepartmentRef | Ref |
| EmployeeRef | Ref |
| ItemRef | Ref |
| ClassRef | Ref |
| AttachableRef | AttachableRef |

---

## ExchangeRate

```python
from quickbooks.objects.exchangerate import ExchangeRate
```

Mixins: ListMixin, UpdateNoIdMixin (all, filter, save — **no get()***)

Only for multicurrency-enabled companies.

### Fields

| Field | Type | Default |
|-------|------|---------|
| AsOfDate | str | "" |
| SourceCurrencyCode | str | "" |
| Rate | decimal | 0 |
| TargetCurrencyCode | str | "" |

### Nested Objects

| Field | Type |
|-------|------|
| MetaData | ExchangeRateMetaData |
| CustomField | CustomField |

### Usage

```python
rate = ExchangeRate()
rate.SourceCurrencyCode = "EUR"
rate.TargetCurrencyCode = "USD"
rate.Rate = 1.15
rate.AsOfDate = "2024-01-15"
rate.save(qb=client)  # Always updates (UpdateNoIdMixin)
```
