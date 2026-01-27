# SOQL WHERE Clause Reference

## Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `WHERE Status = 'Active'` |
| `!=` or `<>` | Not equals | `WHERE Status <> 'Closed'` |
| `<` | Less than | `WHERE Amount < 1000` |
| `<=` | Less than or equal | `WHERE Amount <= 1000` |
| `>` | Greater than | `WHERE Amount > 1000` |
| `>=` | Greater than or equal | `WHERE Amount >= 1000` |

**Note**: Use `<>` instead of `!=` when running queries via CLI to avoid shell escaping issues.

## String Operators

### LIKE

Pattern matching with wildcards:
- `%` - matches any number of characters
- `_` - matches exactly one character

```sql
WHERE Name LIKE 'Acme%'           -- Starts with 'Acme'
WHERE Name LIKE '%Corp'           -- Ends with 'Corp'
WHERE Name LIKE '%Software%'      -- Contains 'Software'
WHERE Name LIKE 'A_me'            -- 'Aame', 'Abme', etc.
```

**Escaping**: Use backslash to match literal `%`, `_`, or `\`:
```sql
WHERE Name LIKE '100\% Complete'  -- Literal percent sign
```

## List Operators

### IN

Match any value in a list:

```sql
WHERE Status IN ('New', 'Working', 'Qualified')
WHERE Id IN ('001xxx', '001yyy', '001zzz')
WHERE AccountId IN (SELECT Id FROM Account WHERE Industry = 'Technology')
```

### NOT IN

Exclude values in a list:

```sql
WHERE Status NOT IN ('Closed Won', 'Closed Lost')
WHERE Id NOT IN (SELECT AccountId FROM Opportunity WHERE IsClosed = true)
```

### INCLUDES / EXCLUDES (Multi-Select Picklists)

```sql
WHERE Categories__c INCLUDES ('A', 'B')     -- Has A or B
WHERE Categories__c EXCLUDES ('C')          -- Does not have C
```

## Null Operators

```sql
WHERE AccountId = null            -- Field is null
WHERE AccountId <> null           -- Field is not null (use <> for CLI)
```

## Logical Operators

### AND

```sql
WHERE Status = 'Active' AND Amount > 1000
WHERE AccountId <> null AND IsDeleted = false AND CreatedDate > 2024-01-01
```

### OR

```sql
WHERE Status = 'New' OR Status = 'Working'
WHERE (Type = 'Customer' OR Type = 'Partner') AND IsActive = true
```

### NOT

```sql
WHERE NOT Status = 'Closed'
WHERE NOT (Amount < 100 OR Amount > 10000)
```

## Date/DateTime Literals

### Absolute Values

```sql
-- Date (no time)
WHERE CloseDate = 2024-06-15
WHERE CloseDate >= 2024-01-01

-- DateTime (with time, UTC)
WHERE CreatedDate >= 2024-01-01T00:00:00Z
WHERE CreatedDate < 2024-12-31T23:59:59Z
```

### Relative Date Literals

| Literal | Description |
|---------|-------------|
| `TODAY` | Current day |
| `YESTERDAY` | Previous day |
| `TOMORROW` | Next day |
| `THIS_WEEK` | Current week (Sunday-Saturday) |
| `LAST_WEEK` | Previous week |
| `NEXT_WEEK` | Following week |
| `THIS_MONTH` | Current month |
| `LAST_MONTH` | Previous month |
| `NEXT_MONTH` | Following month |
| `THIS_QUARTER` | Current quarter |
| `LAST_QUARTER` | Previous quarter |
| `NEXT_QUARTER` | Following quarter |
| `THIS_YEAR` | Current year |
| `LAST_YEAR` | Previous year |
| `NEXT_YEAR` | Following year |
| `THIS_FISCAL_QUARTER` | Current fiscal quarter |
| `THIS_FISCAL_YEAR` | Current fiscal year |

### N-Days Literals

```sql
WHERE CreatedDate = LAST_N_DAYS:30     -- Last 30 days
WHERE CreatedDate >= LAST_N_DAYS:7     -- Within last 7 days
WHERE CloseDate <= NEXT_N_DAYS:30      -- Within next 30 days
WHERE CreatedDate > LAST_N_WEEKS:4     -- More than 4 weeks ago
WHERE CloseDate < NEXT_N_MONTHS:3      -- Within next 3 months
```

Available: `LAST_N_DAYS`, `NEXT_N_DAYS`, `LAST_N_WEEKS`, `NEXT_N_WEEKS`, `LAST_N_MONTHS`, `NEXT_N_MONTHS`, `LAST_N_QUARTERS`, `NEXT_N_QUARTERS`, `LAST_N_YEARS`, `NEXT_N_YEARS`

## Subqueries in WHERE

### Semi-Join (IN with subquery)

```sql
SELECT Id, Name FROM Account
WHERE Id IN (SELECT AccountId FROM Opportunity WHERE Amount > 100000)
```

### Anti-Join (NOT IN with subquery)

```sql
SELECT Id, Name FROM Account
WHERE Id NOT IN (SELECT AccountId FROM Case WHERE Status = 'Open')
```

## Filtering on Relationships

### Parent Fields

```sql
WHERE Account.Industry = 'Technology'
WHERE Account.Parent.Name = 'Parent Corp'
WHERE Contact.Account.BillingCountry = 'USA'
```

### Record Type

```sql
WHERE RecordType.DeveloperName = 'Customer'
WHERE RecordType.Name = 'Partner Account'
```

## Combining Complex Conditions

Use parentheses to control precedence:

```sql
WHERE (Status = 'New' OR Status = 'Working')
  AND (Amount > 1000 OR Priority = 'High')
  AND AccountId <> null
  AND CreatedDate >= LAST_N_DAYS:30
```
