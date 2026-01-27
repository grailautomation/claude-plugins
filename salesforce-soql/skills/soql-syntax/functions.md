# SOQL Functions Reference

## Aggregate Functions

Aggregate functions summarize data across records.

| Function | Description | Example |
|----------|-------------|---------|
| `COUNT()` | Count all records | `SELECT COUNT() FROM Account` |
| `COUNT(field)` | Count non-null values | `SELECT COUNT(Email) FROM Contact` |
| `COUNT_DISTINCT(field)` | Count unique values | `SELECT COUNT_DISTINCT(AccountId) FROM Contact` |
| `SUM(field)` | Sum numeric values | `SELECT SUM(Amount) FROM Opportunity` |
| `AVG(field)` | Average of values | `SELECT AVG(Amount) FROM Opportunity` |
| `MIN(field)` | Minimum value | `SELECT MIN(CloseDate) FROM Opportunity` |
| `MAX(field)` | Maximum value | `SELECT MAX(Amount) FROM Opportunity` |

### GROUP BY

Group results by field values:

```sql
SELECT StageName, COUNT(Id), SUM(Amount)
FROM Opportunity
GROUP BY StageName

-- Multiple fields
SELECT AccountId, StageName, COUNT(Id)
FROM Opportunity
GROUP BY AccountId, StageName

-- With rollup (subtotals)
SELECT StageName, COUNT(Id)
FROM Opportunity
GROUP BY ROLLUP(StageName)
```

### HAVING

Filter grouped results:

```sql
SELECT StageName, COUNT(Id) cnt
FROM Opportunity
GROUP BY StageName
HAVING COUNT(Id) > 10

SELECT AccountId, SUM(Amount) total
FROM Opportunity
GROUP BY AccountId
HAVING SUM(Amount) > 100000
```

## Date Functions

### Date Extraction

| Function | Returns | Example |
|----------|---------|---------|
| `CALENDAR_MONTH(date)` | Month (1-12) | `GROUP BY CALENDAR_MONTH(CloseDate)` |
| `CALENDAR_QUARTER(date)` | Quarter (1-4) | `GROUP BY CALENDAR_QUARTER(CloseDate)` |
| `CALENDAR_YEAR(date)` | Year | `GROUP BY CALENDAR_YEAR(CloseDate)` |
| `DAY_IN_MONTH(date)` | Day (1-31) | `GROUP BY DAY_IN_MONTH(CreatedDate)` |
| `DAY_IN_WEEK(date)` | Day (1=Sun, 7=Sat) | `GROUP BY DAY_IN_WEEK(CreatedDate)` |
| `DAY_IN_YEAR(date)` | Day (1-366) | `GROUP BY DAY_IN_YEAR(CreatedDate)` |
| `DAY_ONLY(datetime)` | Date only | `GROUP BY DAY_ONLY(CreatedDate)` |
| `FISCAL_MONTH(date)` | Fiscal month | `GROUP BY FISCAL_MONTH(CloseDate)` |
| `FISCAL_QUARTER(date)` | Fiscal quarter | `GROUP BY FISCAL_QUARTER(CloseDate)` |
| `FISCAL_YEAR(date)` | Fiscal year | `GROUP BY FISCAL_YEAR(CloseDate)` |
| `HOUR_IN_DAY(datetime)` | Hour (0-23) | `GROUP BY HOUR_IN_DAY(CreatedDate)` |
| `WEEK_IN_MONTH(date)` | Week (1-5) | `GROUP BY WEEK_IN_MONTH(CloseDate)` |
| `WEEK_IN_YEAR(date)` | Week (1-53) | `GROUP BY WEEK_IN_YEAR(CloseDate)` |

### Example: Monthly Summary

```sql
SELECT CALENDAR_YEAR(CloseDate) yr, CALENDAR_MONTH(CloseDate) mo, SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate >= 2024-01-01
GROUP BY CALENDAR_YEAR(CloseDate), CALENDAR_MONTH(CloseDate)
ORDER BY CALENDAR_YEAR(CloseDate), CALENDAR_MONTH(CloseDate)
```

## Format Functions

### FORMAT()

Format field values for display (useful for currency, dates):

```sql
SELECT Id, FORMAT(Amount), FORMAT(CloseDate) FROM Opportunity
```

**Note**: FORMAT() returns strings, which may affect sorting.

### convertCurrency()

Convert currency to user's currency:

```sql
SELECT Id, Amount, convertCurrency(Amount) FROM Opportunity
```

### convertTimezone()

Convert datetime to user's timezone in GROUP BY:

```sql
SELECT DAY_ONLY(convertTimezone(CreatedDate)), COUNT(Id)
FROM Case
GROUP BY DAY_ONLY(convertTimezone(CreatedDate))
```

## Special Functions

### toLabel()

Get translated picklist label:

```sql
SELECT Id, toLabel(Status) FROM Case
```

### TYPEOF (Polymorphic Fields)

Handle polymorphic fields (like Task.WhoId):

```sql
SELECT Id, Subject,
  TYPEOF Who
    WHEN Contact THEN FirstName, LastName, Account.Name
    WHEN Lead THEN FirstName, LastName, Company
  END
FROM Task
```

## Limitations

1. **No String Functions**: SOQL doesn't have UPPER(), LOWER(), SUBSTRING(), etc.
2. **No Math Functions**: No ROUND(), ABS(), etc.
3. **No DISTINCT**: Use `COUNT_DISTINCT()` or `GROUP BY` instead
4. **Aggregate + Non-Aggregate**: Cannot mix without GROUP BY
5. **Nested Aggregates**: Not supported (no `SUM(COUNT())`)
