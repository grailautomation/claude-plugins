---
name: query-patterns
description: Common SOQL query patterns and examples for typical use cases. Use when building queries for common scenarios.
user-invocable: false
---

# SOQL Query Patterns

Common query patterns organized by use case.

## Pattern Categories

- [Basic Queries](basic-queries.md) - Simple SELECT, filtering, sorting
- [Relationship Queries](relationship-queries.md) - Parent/child relationships
- [Aggregate Queries](aggregate-queries.md) - COUNT, SUM, GROUP BY
- [Date-Based Queries](date-queries.md) - Time-based filtering

## Quick Examples

### Find Records by Name

```sql
SELECT Id, Name, Industry FROM Account WHERE Name LIKE '%Acme%'
```

### Get Related Records

```sql
SELECT Id, Name, (SELECT Id, FirstName, LastName FROM Contacts) FROM Account WHERE Id = '001xxx'
```

### Count by Status

```sql
SELECT Status, COUNT(Id) FROM Case GROUP BY Status
```

### Recent Records

```sql
SELECT Id, Name, CreatedDate FROM Lead WHERE CreatedDate >= LAST_N_DAYS:7 ORDER BY CreatedDate DESC
```

### Find by Email Domain

```sql
SELECT Id, Name, Email FROM Contact WHERE Email LIKE '%@acme.com'
```

### Records Without Related Records

```sql
SELECT Id, Name FROM Account WHERE Id NOT IN (SELECT AccountId FROM Opportunity)
```

### Closed Won Opportunities This Quarter

```sql
SELECT Id, Name, Amount, CloseDate FROM Opportunity
WHERE IsWon = true AND CloseDate = THIS_QUARTER
ORDER BY Amount DESC
```

### Get Record Types

```sql
SELECT Id, DeveloperName, Name FROM RecordType WHERE SObjectType = 'Opportunity'
```
