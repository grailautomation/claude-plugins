# Aggregate Query Patterns

## Basic Counts

```sql
-- Count all records
SELECT COUNT() FROM Account

-- Count with filter
SELECT COUNT() FROM Opportunity WHERE IsWon = true

-- Count non-null field values
SELECT COUNT(Email) FROM Contact

-- Count unique values
SELECT COUNT_DISTINCT(AccountId) FROM Contact
```

## Sum, Average, Min, Max

```sql
-- Total revenue
SELECT SUM(Amount) FROM Opportunity WHERE IsWon = true

-- Average deal size
SELECT AVG(Amount) FROM Opportunity WHERE IsWon = true

-- Largest deal
SELECT MAX(Amount) FROM Opportunity

-- Date range
SELECT MIN(CloseDate), MAX(CloseDate) FROM Opportunity WHERE IsWon = true
```

## GROUP BY Patterns

### Count by Picklist Value

```sql
-- Opportunities by stage
SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY StageName

-- Cases by status
SELECT Status, COUNT(Id) FROM Case GROUP BY Status

-- Leads by source
SELECT LeadSource, COUNT(Id) FROM Lead GROUP BY LeadSource ORDER BY COUNT(Id) DESC
```

### Sum by Category

```sql
-- Revenue by stage
SELECT StageName, SUM(Amount) FROM Opportunity
GROUP BY StageName
ORDER BY SUM(Amount) DESC

-- Revenue by account
SELECT AccountId, Account.Name, SUM(Amount)
FROM Opportunity
WHERE IsWon = true
GROUP BY AccountId, Account.Name
ORDER BY SUM(Amount) DESC
LIMIT 10
```

### Multiple Aggregates

```sql
SELECT StageName, COUNT(Id), SUM(Amount), AVG(Amount)
FROM Opportunity
GROUP BY StageName
```

### Group by Multiple Fields

```sql
SELECT Account.Industry, StageName, COUNT(Id), SUM(Amount)
FROM Opportunity
GROUP BY Account.Industry, StageName
ORDER BY Account.Industry, StageName
```

## GROUP BY with Date Functions

### By Month

```sql
SELECT CALENDAR_YEAR(CloseDate) yr, CALENDAR_MONTH(CloseDate) mo, SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate >= 2024-01-01
GROUP BY CALENDAR_YEAR(CloseDate), CALENDAR_MONTH(CloseDate)
ORDER BY yr, mo
```

### By Quarter

```sql
SELECT CALENDAR_QUARTER(CloseDate) qtr, SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate = THIS_YEAR
GROUP BY CALENDAR_QUARTER(CloseDate)
ORDER BY qtr
```

### By Week

```sql
SELECT WEEK_IN_YEAR(CreatedDate), COUNT(Id)
FROM Case
WHERE CreatedDate = THIS_QUARTER
GROUP BY WEEK_IN_YEAR(CreatedDate)
```

### By Fiscal Period

```sql
SELECT FISCAL_QUARTER(CloseDate), SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate = THIS_FISCAL_YEAR
GROUP BY FISCAL_QUARTER(CloseDate)
```

## HAVING Clause

Filter grouped results:

```sql
-- Accounts with more than 5 contacts
SELECT AccountId, Account.Name, COUNT(Id)
FROM Contact
GROUP BY AccountId, Account.Name
HAVING COUNT(Id) > 5

-- Stages with > $100K pipeline
SELECT StageName, SUM(Amount)
FROM Opportunity
WHERE IsClosed = false
GROUP BY StageName
HAVING SUM(Amount) > 100000

-- Products sold more than 10 times
SELECT Product2Id, Product2.Name, COUNT(Id)
FROM OpportunityLineItem
GROUP BY Product2Id, Product2.Name
HAVING COUNT(Id) > 10
ORDER BY COUNT(Id) DESC
```

## ROLLUP (Subtotals)

```sql
-- Stage totals with grand total
SELECT StageName, SUM(Amount)
FROM Opportunity
GROUP BY ROLLUP(StageName)

-- Hierarchical rollup
SELECT Account.Industry, StageName, SUM(Amount)
FROM Opportunity
GROUP BY ROLLUP(Account.Industry, StageName)
```

## CUBE (All Combinations)

```sql
SELECT Account.Industry, StageName, SUM(Amount)
FROM Opportunity
GROUP BY CUBE(Account.Industry, StageName)
```

## Common Aggregate Patterns

### Top N by Metric

```sql
-- Top 10 accounts by revenue
SELECT AccountId, Account.Name, SUM(Amount) total
FROM Opportunity
WHERE IsWon = true
GROUP BY AccountId, Account.Name
ORDER BY SUM(Amount) DESC
LIMIT 10
```

### Percentage Calculation (Manual)

```sql
-- Get counts, calculate percentage in code
SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY StageName
```

### Year-over-Year Comparison

```sql
-- This year
SELECT CALENDAR_MONTH(CloseDate) mo, SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate = THIS_YEAR
GROUP BY CALENDAR_MONTH(CloseDate)

-- Last year (run separately)
SELECT CALENDAR_MONTH(CloseDate) mo, SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate = LAST_YEAR
GROUP BY CALENDAR_MONTH(CloseDate)
```

### Distribution Analysis

```sql
-- Deal size distribution
SELECT
  CASE
    WHEN Amount < 1000 THEN 'Small'
    WHEN Amount < 10000 THEN 'Medium'
    WHEN Amount < 100000 THEN 'Large'
    ELSE 'Enterprise'
  END Size,
  COUNT(Id)
FROM Opportunity
GROUP BY -- Note: CASE not directly supported in GROUP BY, use calculated field
```

*Note: Complex CASE expressions in GROUP BY require formula fields or post-processing.*
