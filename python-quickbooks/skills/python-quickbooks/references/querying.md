# Querying

All queryable objects inherit from `ListMixin`, which provides `all()`, `filter()`, `where()`, `query()`, `count()`, and `choose()`.

## all()

Returns all objects (default max 100).

```python
from quickbooks.objects.customer import Customer

# Basic — returns up to 100
customers = Customer.all(qb=client)

# With ordering
customers = Customer.all(order_by="DisplayName", qb=client)

# With pagination
customers = Customer.all(start_position=1, max_results=50, qb=client)

# Descending order
customers = Customer.all(order_by="DisplayName DESC", qb=client)
```

### Signature

```python
@classmethod
def all(cls, order_by="", start_position="", max_results=100, qb=None)
```

**Note**: For `Item` objects, `all()` automatically includes `SELECT *, Sku` to retrieve the SKU field.

## filter()

Filters using keyword arguments that map to object fields. Builds a WHERE clause automatically.

```python
# Single filter
customers = Customer.filter(Active=True, qb=client)

# Multiple filters (AND)
customers = Customer.filter(Active=True, CompanyName="Acme Corp", qb=client)

# With ordering and pagination
customers = Customer.filter(
    Active=True,
    order_by="DisplayName",
    start_position=1,
    max_results=25,
    qb=client,
)
```

### Signature

```python
@classmethod
def filter(cls, order_by="", start_position="", max_results="", qb=None, **kwargs)
```

### How kwargs are converted

The `build_where_clause()` utility converts kwargs to a QBO WHERE clause:

- String values are single-quoted: `CompanyName="Acme"` → `CompanyName = 'Acme'`
- Non-string values (int, float, Decimal, bool) are unquoted: `Balance=0` → `Balance = 0`, `Active=True` → `Active = True`

**Limitation**: `filter()` only supports equality (`=`) comparisons. For `LIKE`, `>`, `<`, `IN`, `BETWEEN`, or any operator beyond `=`, use `where()` instead.

## where()

Accepts a raw WHERE clause string (without the `WHERE` keyword).

```python
# Simple where
customers = Customer.where("Active = true", qb=client)

# Complex conditions
customers = Customer.where(
    "Active = true AND Balance > '100.00'",
    qb=client,
)

# LIKE queries
customers = Customer.where("DisplayName LIKE 'A%'", qb=client)

# IN queries
customers = Customer.where("Id IN ('1', '2', '3')", qb=client)

# With ordering and pagination
invoices = Invoice.where(
    "TxnDate > '2024-01-01'",
    order_by="TxnDate DESC",
    start_position=1,
    max_results=50,
    qb=client,
)
```

### Signature

```python
@classmethod
def where(cls, where_clause="", order_by="", start_position="", max_results="", qb=None)
```

**Important**: Do NOT include `WHERE` in the clause — it's added automatically.

## query()

Executes a complete raw SQL-like query string.

```python
# Full query control
customers = Customer.query(
    "SELECT * FROM Customer WHERE Active = true ORDER BY DisplayName STARTPOSITION 1 MAXRESULTS 50",
    qb=client,
)

# Count query (use count() method instead for convenience)
result = Customer.query("SELECT COUNT(*) FROM Customer", qb=client)
```

### Signature

```python
@classmethod
def query(cls, select, qb=None)
```

## count()

Returns the count of objects matching an optional WHERE clause.

```python
# Count all
total = Customer.count(qb=client)

# Count with filter
active_count = Customer.count("Active = true", qb=client)
```

### Signature

```python
@classmethod
def count(cls, where_clause="", qb=None)
```

Returns `int` or `None` if no `totalCount` in response.

## choose()

Retrieves objects matching a list of values for a given field (IN query).

```python
# Get specific customers by ID
customers = Customer.choose([1, 2, 3], field="Id", qb=client)

# By another field
customers = Customer.choose(
    ["Acme Corp", "Beta Inc"],
    field="CompanyName",
    qb=client,
)
```

### Signature

```python
@classmethod
def choose(cls, choices, field="Id", qb=None)
```

## Pagination

QBO API limits results to 1000 entities maximum. Use `start_position` and `max_results` for pagination.

```python
def get_all_customers(client):
    """Paginate through all customers."""
    all_customers = []
    start = 1
    page_size = 100

    while True:
        batch = Customer.all(
            start_position=start,
            max_results=page_size,
            qb=client,
        )
        if not batch:
            break
        all_customers.extend(batch)
        if len(batch) < page_size:
            break
        start += page_size

    return all_customers
```

### Pagination in raw queries

When using `query()`, include STARTPOSITION and MAXRESULTS directly:

```python
customers = Customer.query(
    "SELECT * FROM Customer WHERE Active = true STARTPOSITION 101 MAXRESULTS 100",
    qb=client,
)
```

**Note**: STARTPOSITION is 1-based.

## Ordering

### Single field

```python
customers = Customer.all(order_by="DisplayName", qb=client)
customers = Customer.all(order_by="DisplayName DESC", qb=client)
```

### Multiple fields (via where/query)

```python
invoices = Invoice.where(
    "TxnDate > '2024-01-01'",
    order_by="TxnDate DESC, TotalAmt",
    qb=client,
)
```

### In raw query

The `where()` method uses `ORDERBY` (no space). In raw `query()`, use `ORDER BY`:

```python
# via where() — ORDERBY is inserted automatically
Invoice.where("Balance > '0'", order_by="TxnDate DESC", qb=client)

# via query() — use standard SQL ORDER BY
Invoice.query("SELECT * FROM Invoice WHERE Balance > '0' ORDER BY TxnDate DESC", qb=client)
```

## Query Security

**The library does NOT sanitize inputs.** Never pass user input directly into WHERE clauses:

```python
# DANGEROUS — SQL injection risk
Customer.where(f"DisplayName = '{user_input}'", qb=client)

# SAFER — use filter() which handles quoting
Customer.filter(DisplayName=user_input, qb=client)
```
