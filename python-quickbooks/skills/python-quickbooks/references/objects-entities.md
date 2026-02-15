# Entity Objects

## Customer

```python
from quickbooks.objects.customer import Customer
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | Set by QBO on create |
| SyncToken | int | 0 | For optimistic locking |
| Title | str | "" | |
| GivenName | str | "" | |
| MiddleName | str | "" | |
| FamilyName | str | "" | |
| Suffix | str | "" | |
| FullyQualifiedName | str | "" | Read-only |
| CompanyName | str | "" | |
| DisplayName | str | "" | **Must be unique** |
| PrintOnCheckName | str | "" | |
| Notes | str | "" | |
| Active | bool | True | |
| IsProject | bool | False | |
| Job | bool | False | |
| BillWithParent | bool | False | |
| Taxable | bool | True | |
| Balance | decimal | 0 | Read-only |
| BalanceWithJobs | decimal | 0 | Read-only |
| PreferredDeliveryMethod | str | "" | |
| ResaleNum | str | "" | |
| Level | int | 0 | |
| OpenBalanceDate | str | "" | |
| PrimaryTaxIdentifier | str | "" | |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| BillAddr | Address |
| ShipAddr | Address |
| PrimaryPhone | PhoneNumber |
| AlternatePhone | PhoneNumber |
| Mobile | PhoneNumber |
| Fax | PhoneNumber |
| PrimaryEmailAddr | EmailAddress |
| WebAddr | WebAddress |
| DefaultTaxCodeRef | Ref |
| SalesTermRef | Ref |
| PaymentMethodRef | Ref |
| CurrencyRef | Ref |
| ParentRef | Ref |
| ARAccountRef | Ref |

### to_ref()

Returns a Ref with `name=DisplayName`, `type="Customer"`, `value=Id`.

---

## Vendor

```python
from quickbooks.objects.vendor import Vendor
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| Title | str | "" | |
| GivenName | str | "" | |
| MiddleName | str | "" | |
| FamilyName | str | "" | |
| Suffix | str | "" | |
| CompanyName | str | "" | |
| DisplayName | str | "" | |
| PrintOnCheckName | str | "" | |
| Active | bool | True | |
| TaxIdentifier | str | "" | |
| Balance | decimal | 0 | Read-only |
| BillRate | decimal | 0 | |
| AcctNum | str | "" | |
| Vendor1099 | bool | False | |
| TaxReportingBasis | str | "" | |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| BillAddr | Address |
| PrimaryPhone | PhoneNumber |
| AlternatePhone | PhoneNumber |
| Mobile | PhoneNumber |
| Fax | PhoneNumber |
| PrimaryEmailAddr | EmailAddress |
| WebAddr | WebAddress |
| TermRef | Ref |
| CurrencyRef | Ref |
| APAccountRef | Ref |

### Helper: ContactInfo

```python
from quickbooks.objects.vendor import ContactInfo
```

| Field | Type |
|-------|------|
| Type | str |
| Telephone | PhoneNumber |

---

## Employee

```python
from quickbooks.objects.employee import Employee
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

### Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| Id | int | None | |
| SyncToken | int | 0 | |
| SSN | str | None | |
| GivenName | str | "" | |
| FamilyName | str | "" | |
| MiddleName | str | "" | |
| DisplayName | str | "" | |
| Suffix | str | "" | |
| PrintOnCheckName | str | "" | |
| EmployeeNumber | str | "" | |
| Title | str | "" | |
| BillRate | decimal | 0 | |
| CostRate | decimal | 0 | |
| BirthDate | str | None | |
| Gender | str | None | |
| HiredDate | str | None | |
| ReleasedDate | str | "" | |
| Active | bool | True | |
| Organization | bool | False | |
| BillableTime | bool | False | |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| PrimaryAddr | Address |
| PrimaryPhone | PhoneNumber |
| Mobile | PhoneNumber |
| PrimaryEmailAddr | EmailAddress |

---

## Department

```python
from quickbooks.objects.department import Department
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

Used to track different segments of the business (divisions, locations, stores). Applied to entire transactions (vs Class which applies to individual lines).

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| SyncToken | int | 0 |
| Name | str | "" |
| SubDepartment | bool | False |
| FullyQualifiedName | str | "" |
| Active | bool | True |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| ParentRef | Ref |

**Delete**: Set `Active = False` and save (soft delete).

---

## CompanyCurrency

```python
from quickbooks.objects.companycurrency import CompanyCurrency
```

Mixins: `QuickbooksManagedObject`, `QuickbooksTransactionEntity` (get, all, filter, save, to_ref)

Only applicable for multicurrency-enabled companies.

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| Code | str | "" |
| Name | str | "" |
| Active | bool | True |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| CustomField | CustomField |
| MetaData | MetaData |

### to_ref()

Returns a Ref with `name=Name`, `type="CompanyCurrency"`, `value=Code` (note: uses Code, not Id).

---

## CustomerType

```python
from quickbooks.objects.customertype import CustomerType
```

Mixins: `QuickbooksReadOnlyObject`, `QuickbooksTransactionEntity` (get, all — **read-only**, no save)

Allows categorizing customers (industry, location, referral source).

### Fields

| Field | Type | Default |
|-------|------|---------|
| Id | int | None |
| Name | str | "" |
| Active | bool | False |

### Nested Objects (class_dict)

| Field | Type |
|-------|------|
| MetaData | MetaData |

---

## Common Nested Types

### Address

```python
from quickbooks.objects.base import Address
```

| Field | Type |
|-------|------|
| Id | int |
| Line1–Line5 | str |
| City | str |
| CountrySubDivisionCode | str |
| Country | str |
| PostalCode | str |
| Lat | str |
| Long | str |
| Note | str |

### PhoneNumber

| Field | Type |
|-------|------|
| FreeFormNumber | str |

### EmailAddress

| Field | Type |
|-------|------|
| Address | str |

### WebAddress

| Field | Type |
|-------|------|
| URI | str |

### Ref

| Field | Type | Description |
|-------|------|-------------|
| value | str | The ID value |
| name | str | Display name |
| type | str | Object type name |

### MetaData

| Field | Type |
|-------|------|
| CreateTime | str |
| LastUpdatedTime | str |

### CustomField

| Field | Type |
|-------|------|
| DefinitionId | str |
| Type | str |
| Name | str |
| StringValue | str |

### LinkedTxn

| Field | Type | Notes |
|-------|------|-------|
| TxnId | int | |
| TxnType | str | Initialized as `0` (int) in source, but QBO expects/returns strings ("Invoice", "Payment", etc.). `to_linked_txn()` sets this to `qbo_object_name` (a string). Always assign as string. |
| TxnLineId | int | |
