---
name: soql-syntax
description: SOQL query language syntax, clauses, operators, and functions. Use when writing or debugging SOQL queries.
user-invocable: false
---

# SOQL Syntax Reference

Salesforce Object Query Language (SOQL) for querying Salesforce data.

## Basic Query Structure

```sql
SELECT field1, field2, ...
FROM ObjectName
[WHERE conditions]
[ORDER BY field [ASC|DESC] [NULLS FIRST|LAST]]
[LIMIT n]
[OFFSET n]
```

## Clauses

### SELECT

```sql
-- Specific fields
SELECT Id, Name, CreatedDate FROM Account

-- Parent fields (dot notation)
SELECT Id, Name, Account.Name FROM Contact

-- Child records (subquery)
SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account

-- Aggregate functions
SELECT COUNT(Id), SUM(Amount), AVG(Amount) FROM Opportunity GROUP BY StageName
```

### WHERE

See [clauses.md](clauses.md) for complete WHERE clause reference.

```sql
-- Comparison
WHERE Amount > 10000
WHERE Name = 'Acme'
WHERE CloseDate < 2024-01-01

-- Null checks (use <> not != for CLI compatibility)
WHERE AccountId <> null
WHERE AccountId = null

-- LIKE (wildcards: % = any chars, _ = single char)
WHERE Name LIKE 'Acme%'
WHERE Email LIKE '%@gmail.com'

-- IN list
WHERE Status IN ('New', 'Working', 'Qualified')
WHERE Id IN ('001xxx', '001yyy')

-- AND/OR/NOT
WHERE Amount > 1000 AND StageName = 'Closed Won'
WHERE (Status = 'New' OR Status = 'Working')
WHERE NOT Status = 'Closed'
```

### ORDER BY

```sql
ORDER BY Name                    -- Ascending (default)
ORDER BY Amount DESC             -- Descending
ORDER BY CloseDate DESC NULLS LAST
ORDER BY Account.Name, Name      -- Multiple fields
```

### LIMIT and OFFSET

```sql
LIMIT 100                        -- Return max 100 records
LIMIT 10 OFFSET 20               -- Skip 20, return 10 (pagination)
```

## Functions

See [functions.md](functions.md) for complete function reference.

### Aggregate Functions

```sql
SELECT COUNT(Id) FROM Account
SELECT SUM(Amount), AVG(Amount), MIN(Amount), MAX(Amount) FROM Opportunity
SELECT COUNT(Id), StageName FROM Opportunity GROUP BY StageName
SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY StageName HAVING COUNT(Id) > 5
```

### Date Functions

```sql
WHERE CreatedDate = TODAY
WHERE CloseDate = THIS_MONTH
WHERE CreatedDate = LAST_N_DAYS:30
WHERE CloseDate > NEXT_N_DAYS:7
WHERE CreatedDate >= 2024-01-01T00:00:00Z
```

## Important Limitations

1. **Long Text Fields Cannot Be Filtered**: `Description`, `Body`, and custom long text areas cannot use LIKE or = in WHERE
2. **No DISTINCT**: Use GROUP BY instead
3. **No JOIN**: Use relationship queries instead
4. **Subquery Depth**: Max 1 level of nested subqueries
5. **Relationship Traversal**: Max 5 levels up, 1 level down
6. **Result Limit**: 50,000 records max (use bulk export for more)

## Common Gotchas

See [gotchas.md](gotchas.md) for detailed troubleshooting.
