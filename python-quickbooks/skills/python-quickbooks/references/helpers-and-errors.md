# Helpers & Errors

## Date Helpers

```python
from quickbooks.helpers import qb_date_format, qb_datetime_format, qb_datetime_utc_offset_format
from datetime import datetime
```

### qb_date_format

Converts a date/datetime to QBO date format (`YYYY-MM-DD`).

```python
from datetime import date

formatted = qb_date_format(date(2024, 6, 15))
# "2024-06-15"
```

### qb_datetime_format

Converts a datetime to QBO datetime format (`YYYY-MM-DDTHH:MM:SS`).

```python
formatted = qb_datetime_format(datetime(2024, 6, 15, 14, 30, 0))
# "2024-06-15T14:30:00"
```

### qb_datetime_utc_offset_format

Converts a datetime to QBO datetime format with UTC offset.

```python
formatted = qb_datetime_utc_offset_format(
    datetime(2024, 6, 15, 14, 30, 0),
    "-08:00"
)
# "2024-06-15T14:30:00-08:00"
```

**Parameters**:
- `input_date`: A datetime object
- `utc_offset`: String formatted as `+/-HH:MM` (e.g., `"-08:00"`, `"+05:30"`)

---

## JSON Utilities

### to_json()

Converts any QBO object to a JSON string. Provided by `ToJsonMixin` (inherited by all objects).

```python
customer = Customer.get(42, qb=client)
json_str = customer.to_json()
```

**Behavior**:
- Properties starting with `_` are excluded
- Properties with value `None` are excluded
- `decimal.Decimal` values are converted to strings
- Output is sorted by keys and indented (4 spaces)

### from_json()

Creates an object from a JSON dict. Provided by `FromJsonMixin` (classmethod).

```python
from quickbooks.objects.account import Account

account = Account.from_json({
    "AccountType": "Accounts Receivable",
    "AcctNum": "123123",
    "Name": "MyJobs",
})
account.save(qb=client)
```

**How from_json works**:
1. Iterates over keys in the JSON dict
2. If key is in `class_dict`: instantiates the sub-object class and recursively calls `from_json`
3. If key is in `list_dict`: iterates items, checking `DetailType` against `detail_dict` for proper subclass
4. Otherwise: sets the attribute directly via `setattr`

### to_dict()

Converts any QBO object to a Python dict. Provided by `ToDictMixin`.

```python
customer = Customer.get(42, qb=client)
data = customer.to_dict()
```

**Behavior**:
- Recursively converts nested objects
- Excludes callable attributes and attributes starting with `_`

---

## to_ref()

Many objects provide a `to_ref()` method that creates a `Ref` for linking:

```python
from quickbooks.objects.base import Ref

customer = Customer.get(42, qb=client)
ref = customer.to_ref()
# ref.value = "42"
# ref.name = "Acme Corp"
# ref.type = "Customer"
```

### Objects with to_ref() and their name source

| Object | ref.name source |
|--------|----------------|
| Customer | DisplayName |
| Vendor | DisplayName |
| Employee | DisplayName |
| Department | Name |
| CompanyCurrency | Name (value = Code) |
| Item | Name |
| Account | FullyQualifiedName |
| Term | Name |
| Class | Name |
| PaymentMethod | Name |
| CompanyInfo | CompanyName |
| Invoice | DocNumber |
| Bill | DocNumber |
| CreditMemo | (no name, type + value only) |
| TaxCode | Name |
| Attachable | FileName |

---

## Exception Hierarchy

All exceptions inherit from `QuickbooksException`.

```python
from quickbooks.exceptions import (
    QuickbooksException,
    AuthorizationException,
    UnsupportedException,
    GeneralException,
    ValidationException,
    SevereException,
    ObjectNotFoundException,
)
```

### QuickbooksException (Base)

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | str | Error message |
| `error_code` | int | QBO error code |
| `detail` | str | Detailed error info |

```python
try:
    customer = Customer.get(99999, qb=client)
except QuickbooksException as e:
    print(f"Code: {e.error_code}")
    print(f"Message: {e.message}")
    print(f"Detail: {e.detail}")
```

### Error Code Ranges

| Exception Class | Code Range | Description |
|----------------|------------|-------------|
| `AuthorizationException` | 1–499 | Auth/permission failures |
| `UnsupportedException` | 500–599 | Unsupported operations |
| `GeneralException` | 600–1999 | General errors |
| `ObjectNotFoundException` | 610 | Object not found (**inherits from `QuickbooksException`**, NOT `GeneralException`) |
| `ValidationException` | 2000–4999 | Input validation errors |
| `SevereException` | 10000+ | Severe/internal errors |

### Error handling pattern

```python
from quickbooks.exceptions import (
    AuthorizationException,
    ObjectNotFoundException,
    ValidationException,
    QuickbooksException,
)

try:
    invoice = Invoice.get(42, qb=client)
    invoice.save(qb=client)
except AuthorizationException as e:
    # Token expired, refresh needed
    print(f"Auth error {e.error_code}: {e.message}")
except ObjectNotFoundException as e:
    # Object doesn't exist
    print(f"Not found: {e.detail}")
except ValidationException as e:
    # Invalid data
    print(f"Validation error {e.error_code}: {e.message}")
    print(f"Detail: {e.detail}")
except QuickbooksException as e:
    # Catch-all
    print(f"QBO error {e.error_code}: {e.message}")
```

### How exceptions are raised

The `QuickBooks.handle_exceptions()` method parses the `Fault` response from QBO:

```python
# Response structure from QBO API:
{
    "Fault": {
        "Error": [
            {
                "Message": "Object Not Found",
                "code": "610",
                "Detail": "Object Not Found: something"
            }
        ]
    }
}
```

Each error in the `Error` array is mapped to the appropriate exception class based on its code.

### HTTP 401 handling

HTTP 401 responses raise `AuthorizationException` directly (before JSON parsing):

```python
# Raised with error_code=401 and detail=response.text
raise AuthorizationException("Application authentication failed", error_code=401, detail="...")
```

### JSON parse errors

If the response isn't valid JSON, a `QuickbooksException` with code 10000 is raised:

```python
raise QuickbooksException("Error reading json response: ...", 10000)
```

### Iterator support

Exception objects support iteration for structured access:

```python
try:
    customer.save(qb=client)
except QuickbooksException as e:
    for key, value in e:
        print(f"{key}: {value}")
    # Outputs:
    # error_code: 6240
    # detail: Duplicate Name Exists Error
    # message: ...
```
