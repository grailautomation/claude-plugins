# Batch Operations

Batch operations allow creating, updating, or deleting multiple objects in a single API call.

```python
from quickbooks.batch import batch_create, batch_update, batch_delete
```

## batch_create

```python
from quickbooks.objects.customer import Customer
from quickbooks.batch import batch_create

customers = []
for i in range(5):
    customer = Customer()
    customer.DisplayName = f"Customer {i}"
    customers.append(customer)

results = batch_create(customers, qb=client)
```

## batch_update

```python
from quickbooks.objects.customer import Customer
from quickbooks.batch import batch_update

# Get existing customers
customers = Customer.filter(Active=True, qb=client)
for c in customers:
    c.Notes = "Updated via batch"

results = batch_update(customers, qb=client)
```

## batch_delete

```python
from quickbooks.objects.invoice import Invoice
from quickbooks.batch import batch_delete

# Must have Id and SyncToken
invoices = Invoice.filter(DocNumber="TEST-001", qb=client)
results = batch_delete(invoices, qb=client)
```

## Processing Results

All batch functions return a `BatchResponse` object:

```python
results = batch_create(customers, qb=client)

# Successful operations
for obj in results.successes:
    print(f"Created: {obj.DisplayName} (Id: {obj.Id})")

# Failed operations
for fault in results.faults:
    print(f"Failed: {fault.original_object.DisplayName}")
    for error in fault.Error:
        print(f"  Error {error.code}: {error.Message}")
        print(f"  Detail: {error.Detail}")

# All responses (both success and failure)
for response in results.batch_responses:
    pass

# Original list passed in
for obj in results.original_list:
    pass
```

## BatchResponse

| Attribute | Type | Description |
|-----------|------|-------------|
| `successes` | list | Successfully processed objects (re-hydrated from response) |
| `faults` | list[Fault] | Failed operations with error details |
| `batch_responses` | list[BatchItemResponse] | All raw responses |
| `original_list` | list | The original objects passed to the batch function |

## Fault Object

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | str | Fault type |
| `original_object` | object | The original object that failed |
| `Error` | list[FaultError] | List of errors |

## FaultError Object

| Attribute | Type | Description |
|-----------|------|-------------|
| `Message` | str | Error message |
| `code` | str | Error code |
| `Detail` | str | Detailed error description |
| `element` | str | Element that caused the error |

## Auto-Chunking

The batch API has a maximum of **30 items per request**. The `BatchManager` automatically chunks larger lists:

```python
# This works even with > 30 items — automatically split into chunks
customers = [Customer() for _ in range(100)]
for i, c in enumerate(customers):
    c.DisplayName = f"Customer {i}"

results = batch_create(customers, qb=client)  # Sends 4 batches of 30, 30, 30, 10
```

The `BatchManager` processes each chunk sequentially and aggregates results into a single `BatchResponse`.

## BatchManager Internals

```python
from quickbooks.batch import BatchManager
from quickbooks.objects.batchrequest import BatchOperation

# Direct usage (usually prefer batch_create/update/delete functions)
mgr = BatchManager(operation="create", max_request_items=30)
results = mgr.save(obj_list, qb=client)
```

### Supported operations

```python
class BatchOperation:
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
```

### Processing flow

1. `save()` chunks the list into groups of `max_request_items` (default 30)
2. Each chunk is converted to an `IntuitBatchRequest` with unique `bId` per item
3. Sent to QBO's `/batch` endpoint
4. Response is parsed, matching results back to original objects via `bId`
5. Results are aggregated across all chunks

## Error Handling Pattern

```python
results = batch_create(customers, qb=client)

if results.faults:
    print(f"{len(results.faults)} failures out of {len(customers)}")

    for fault in results.faults:
        obj = fault.original_object
        errors = [f"{e.code}: {e.Message}" for e in fault.Error]
        print(f"  {obj.DisplayName}: {', '.join(errors)}")

    # Retry failed items
    failed_objects = [f.original_object for f in results.faults]
    # Fix issues, then retry
    retry_results = batch_create(failed_objects, qb=client)
```

## Batch Request/Response Objects

### IntuitBatchRequest

Container for batch items. Serialized to JSON for the API call.

| Field | Type |
|-------|------|
| BatchItemRequest | list[BatchItemRequest] |

### BatchItemRequest

| Field | Type |
|-------|------|
| bId | str (UUID) |
| operation | str ("create"/"update"/"delete") |

Plus the QBO object dynamically set via `set_object()`.

### BatchItemResponse

| Field | Type |
|-------|------|
| bId | str |
| Fault | Fault or None |

Plus the result QBO object if successful.
