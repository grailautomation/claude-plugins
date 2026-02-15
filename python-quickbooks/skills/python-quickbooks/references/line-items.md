# Line Items

All line items inherit from `DetailLine`. The `DetailType` field determines which line detail class is used during JSON deserialization via the object's `detail_dict`.

```python
from quickbooks.objects.detailline import (
    DetailLine, SalesItemLine, SalesItemLineDetail,
    AccountBasedExpenseLine, AccountBasedExpenseLineDetail,
    ItemBasedExpenseLine, ItemBasedExpenseLineDetail,
    DiscountLine, DiscountLineDetail,
    SubtotalLine, SubtotalLineDetail,
    DescriptionOnlyLine, DescriptionLineDetail,
    GroupLine, GroupLineDetail,
    TDSLine, TDSLineDetail,
)
from quickbooks.objects.journalentry import JournalEntryLine, JournalEntryLineDetail
```

## DetailLine (Base Class)

All line items share these base fields:

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| LineNum | int | 0 |
| Description | str | None |
| Amount | decimal | 0 |
| DetailType | str | "" |
| LinkedTxn | list[LinkedTxn] | [] |
| CustomField | list[CustomField] | [] |

## SalesItemLine

Used on: **Invoice**, **Estimate**, **CreditMemo**, **SalesReceipt**

`DetailType = "SalesItemLineDetail"`

### SalesItemLineDetail Fields

| Field | Type | Default |
|-------|------|---------|
| UnitPrice | decimal | 0 |
| Qty | decimal | 0 |
| ServiceDate | str | "" |
| TaxInclusiveAmt | decimal | 0 |
| MarkupInfo | MarkupInfo | None |
| ItemRef | Ref | None |
| ItemAccountRef | Ref | None |
| ClassRef | Ref | None |
| TaxCodeRef | Ref | None |
| PriceLevelRef | Ref | None |

### Usage

```python
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects.base import Ref

line = SalesItemLine()
line.Amount = 100.00
line.Description = "Consulting services"

detail = SalesItemLineDetail()
detail.UnitPrice = 50.00
detail.Qty = 2

item_ref = Ref()
item_ref.value = "1"
item_ref.name = "Consulting"
detail.ItemRef = item_ref

line.SalesItemLineDetail = detail
```

## AccountBasedExpenseLine

Used on: **Bill**, **Purchase**, **PurchaseOrder**, **VendorCredit**

`DetailType = "AccountBasedExpenseLineDetail"`

### AccountBasedExpenseLineDetail Fields

| Field | Type | Default |
|-------|------|---------|
| BillableStatus | str | None |
| TaxInclusiveAmt | decimal | 0 |
| CustomerRef | Ref | None |
| AccountRef | Ref | None |
| TaxCodeRef | Ref | None |
| ClassRef | Ref | None |
| MarkupInfo | MarkupInfo | None |

### Usage

```python
from quickbooks.objects.detailline import AccountBasedExpenseLine, AccountBasedExpenseLineDetail
from quickbooks.objects.base import Ref

line = AccountBasedExpenseLine()
line.Amount = 250.00
line.Description = "Office supplies"

detail = AccountBasedExpenseLineDetail()

account_ref = Ref()
account_ref.value = "7"
account_ref.name = "Office Expenses"
detail.AccountRef = account_ref

line.AccountBasedExpenseLineDetail = detail
```

## ItemBasedExpenseLine

Used on: **Bill**, **Purchase**, **PurchaseOrder**, **VendorCredit**

`DetailType = "ItemBasedExpenseLineDetail"`

### ItemBasedExpenseLineDetail Fields

| Field | Type | Default |
|-------|------|---------|
| BillableStatus | str | None |
| UnitPrice | decimal | 0 |
| Qty | decimal | 0 |
| TaxInclusiveAmt | decimal | 0 |
| ItemRef | Ref | None |
| ClassRef | Ref | None |
| PriceLevelRef | Ref | None |
| TaxCodeRef | Ref | None |
| MarkupInfo | MarkupInfo | None |
| CustomerRef | Ref | None |

### Usage

```python
from quickbooks.objects.detailline import ItemBasedExpenseLine, ItemBasedExpenseLineDetail
from quickbooks.objects.base import Ref

line = ItemBasedExpenseLine()
line.Amount = 500.00

detail = ItemBasedExpenseLineDetail()
detail.UnitPrice = 50.00
detail.Qty = 10
detail.BillableStatus = "Billable"

item_ref = Ref()
item_ref.value = "3"
item_ref.name = "Widget"
detail.ItemRef = item_ref

customer_ref = Ref()
customer_ref.value = "1"
detail.CustomerRef = customer_ref

line.ItemBasedExpenseLineDetail = detail
```

## DiscountLine

Used on: **Invoice**, **Estimate**, **CreditMemo**

`DetailType = "DiscountLineDetail"`

### DiscountLineDetail Fields

| Field | Type | Default |
|-------|------|---------|
| Discount | DiscountOverride | None |
| ClassRef | Ref | None |
| TaxCodeRef | Ref | None |
| DiscountAccountRef | Ref | None |
| PercentBased | bool | False |
| DiscountPercent | decimal | 0 |

### DiscountOverride

| Field | Type |
|-------|------|
| PercentBased | bool |
| DiscountPercent | decimal |
| DiscountRef | Ref |
| DiscountAccountRef | Ref |

## SubtotalLine

Used on: **Invoice**, **Estimate**, **CreditMemo**

`DetailType = "SubTotalLineDetail"` (note the capital T)

### SubtotalLineDetail Fields

| Field | Type |
|-------|------|
| ItemRef | Ref |

## DescriptionOnlyLine

Used on: **Invoice**, **Estimate**, **CreditMemo**, **JournalEntry**

`DetailType = "DescriptionOnly"`

### DescriptionLineDetail Fields

| Field | Type |
|-------|------|
| ServiceDate | str |
| TaxCodeRef | Ref |

## GroupLine

Used on: **Invoice**, **Estimate**

`DetailType = "GroupLineDetail"`

### GroupLineDetail

Currently an empty class (no additional fields beyond the base).

## TDSLine

Used on: **Bill**, **Purchase**, **PurchaseOrder**, **VendorCredit**

`DetailType = "TDSLineDetail"`

TDS (Tax Deducted at Source) — special tax for Indian companies.

### TDSLineDetail Fields

| Field | Type |
|-------|------|
| TDSSectionTypeId | str |

## JournalEntryLine

Used on: **JournalEntry**

`DetailType = "JournalEntryLineDetail"`

Defined in `quickbooks.objects.journalentry`, not in `detailline.py`.

### JournalEntryLineDetail Fields

| Field | Type | Default |
|-------|------|---------|
| PostingType | str | "" |
| TaxApplicableOn | str | "Sales" |
| TaxAmount | decimal | 0 |
| BillableStatus | str | None |
| Entity | Entity | None |
| AccountRef | Ref | None |
| ClassRef | Ref | None |
| DepartmentRef | Ref | None |
| TaxCodeRef | Ref | None |

### Entity (for JournalEntry)

| Field | Type |
|-------|------|
| Type | str |
| EntityRef | Ref |

## DetailType Mapping by Object

Each financial object defines a `detail_dict` that maps DetailType strings to Python classes:

### Invoice / Estimate detail_dict

```python
{
    "SalesItemLineDetail": SalesItemLine,
    "SubTotalLineDetail": SubtotalLine,
    "DiscountLineDetail": DiscountLine,
    "DescriptionOnly": DescriptionOnlyLine,
    "GroupLineDetail": GroupLine,
}
```

### Bill / Purchase / PurchaseOrder detail_dict

```python
{
    "ItemBasedExpenseLineDetail": ItemBasedExpenseLine,
    "AccountBasedExpenseLineDetail": AccountBasedExpenseLine,
    "TDSLineDetail": TDSLine,
}
```

### CreditMemo detail_dict

```python
{
    "SalesItemLineDetail": SalesItemLine,
    "SubTotalLineDetail": SubtotalLine,
    "DiscountLineDetail": DiscountLine,
    "DescriptionLineDetail": DescriptionOnlyLine,  # WARNING: Key is "DescriptionLineDetail", NOT "DescriptionOnly" (used by Invoice/Estimate)
}
```

**Warning**: CreditMemo uses `"DescriptionLineDetail"` as the key for description-only lines, while Invoice/Estimate use `"DescriptionOnly"`. Code that builds line items with `DetailType = "DescriptionOnly"` (the Invoice pattern) will silently fall back to generic `DetailLine` on CreditMemo. When adding description lines to a CreditMemo, set `DetailType = "DescriptionLineDetail"`.

### SalesReceipt / RefundReceipt detail_dict

```python
{}  # Empty — no detail type mapping
```

**Warning**: Both SalesReceipt and RefundReceipt have an empty `detail_dict`. All lines deserialize as generic `DetailLine`, losing typed detail attributes. The `DetailType` string is still present in the raw data, but the library cannot map it to the correct Python class. You must manually check `DetailType` and access detail fields via the raw dict.

### JournalEntry detail_dict

```python
{
    "DescriptionOnly": DescriptionOnlyLine,
    "JournalEntryLineDetail": JournalEntryLine,
}
```

### Deposit detail_dict

```python
{
    "DepositLineDetail": DepositLine,
}
```

## MarkupInfo

Shared across SalesItemLineDetail, AccountBasedExpenseLineDetail, ItemBasedExpenseLineDetail.

| Field | Type | Default |
|-------|------|---------|
| PercentBased | bool | False |
| Value | decimal | 0 |
| Percent | decimal | 0 |
| PriceLevelRef | Ref | None |

## How DetailLine Deserialization Works

When loading from JSON, the `from_json()` method in `FromJsonMixin` checks:

1. If the list field key is in `list_dict`, iterate over items
2. For each item, check if `DetailType` exists in the data
3. If `DetailType` is in the object's `detail_dict`, instantiate that specific class
4. Otherwise, instantiate the generic class from `list_dict`

This means the `Line` field is always typed as `DetailLine` in `list_dict`, but the actual instances are the specific subclasses based on `DetailType`.
