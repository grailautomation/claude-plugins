# Date-Based Query Patterns

## Today and Relative Dates

```sql
-- Created today
SELECT Id, Name FROM Lead WHERE CreatedDate = TODAY

-- Created this week
SELECT Id, Name FROM Case WHERE CreatedDate = THIS_WEEK

-- Due this month
SELECT Id, Subject FROM Task WHERE ActivityDate = THIS_MONTH

-- Closing this quarter
SELECT Id, Name, Amount FROM Opportunity WHERE CloseDate = THIS_QUARTER
```

## Past Dates

```sql
-- Last N days
SELECT Id, Name FROM Lead WHERE CreatedDate >= LAST_N_DAYS:7
SELECT Id, Name FROM Case WHERE ClosedDate >= LAST_N_DAYS:30

-- Yesterday
SELECT Id, Name FROM Lead WHERE CreatedDate = YESTERDAY

-- Last week/month/quarter/year
SELECT Id, Name FROM Opportunity WHERE CloseDate = LAST_WEEK
SELECT Id, Name FROM Opportunity WHERE CloseDate = LAST_MONTH
SELECT Id, Name FROM Opportunity WHERE CloseDate = LAST_QUARTER
SELECT Id, Name FROM Opportunity WHERE CloseDate = LAST_YEAR
```

## Future Dates

```sql
-- Next N days
SELECT Id, Name, CloseDate FROM Opportunity WHERE CloseDate <= NEXT_N_DAYS:30

-- Tomorrow
SELECT Id, Subject FROM Event WHERE StartDateTime = TOMORROW

-- Next week/month/quarter
SELECT Id, Name FROM Opportunity WHERE CloseDate = NEXT_WEEK
SELECT Id, Name FROM Opportunity WHERE CloseDate = NEXT_MONTH
SELECT Id, Name FROM Opportunity WHERE CloseDate = NEXT_QUARTER
```

## Date Ranges

```sql
-- Between specific dates
SELECT Id, Name FROM Opportunity
WHERE CloseDate >= 2024-01-01 AND CloseDate <= 2024-12-31

-- Between datetimes
SELECT Id, Name FROM Lead
WHERE CreatedDate >= 2024-01-01T00:00:00Z AND CreatedDate < 2024-02-01T00:00:00Z

-- Rolling window
SELECT Id, Name FROM Case
WHERE CreatedDate >= LAST_N_DAYS:90 AND CreatedDate < LAST_N_DAYS:60
```

## Fiscal Periods

```sql
-- This fiscal quarter
SELECT Id, Name, Amount FROM Opportunity WHERE CloseDate = THIS_FISCAL_QUARTER

-- This fiscal year
SELECT Id, Name, Amount FROM Opportunity WHERE CloseDate = THIS_FISCAL_YEAR

-- Last fiscal quarter
SELECT Id, Name, Amount FROM Opportunity WHERE CloseDate = LAST_FISCAL_QUARTER
```

## Date Comparisons

```sql
-- Overdue tasks
SELECT Id, Subject, ActivityDate FROM Task
WHERE IsClosed = false AND ActivityDate < TODAY

-- Expiring contracts
SELECT Id, ContractNumber, EndDate FROM Contract
WHERE Status = 'Activated' AND EndDate <= NEXT_N_DAYS:30

-- Stale opportunities
SELECT Id, Name, LastModifiedDate FROM Opportunity
WHERE IsClosed = false AND LastModifiedDate < LAST_N_DAYS:30
```

## Null Date Handling

```sql
-- Records without a date
SELECT Id, Name FROM Opportunity WHERE CloseDate = null

-- Records with a date
SELECT Id, Name FROM Opportunity WHERE CloseDate <> null

-- Sort with nulls
SELECT Id, Name, CloseDate FROM Opportunity ORDER BY CloseDate ASC NULLS LAST
```

## Group by Time Periods

### Daily

```sql
SELECT DAY_ONLY(CreatedDate) d, COUNT(Id)
FROM Lead
WHERE CreatedDate >= LAST_N_DAYS:30
GROUP BY DAY_ONLY(CreatedDate)
ORDER BY DAY_ONLY(CreatedDate)
```

### Weekly

```sql
SELECT WEEK_IN_YEAR(CreatedDate) wk, COUNT(Id)
FROM Case
WHERE CreatedDate = THIS_YEAR
GROUP BY WEEK_IN_YEAR(CreatedDate)
ORDER BY wk
```

### Monthly

```sql
SELECT CALENDAR_YEAR(CloseDate) yr, CALENDAR_MONTH(CloseDate) mo, SUM(Amount)
FROM Opportunity
WHERE IsWon = true
GROUP BY CALENDAR_YEAR(CloseDate), CALENDAR_MONTH(CloseDate)
ORDER BY yr, mo
```

### Quarterly

```sql
SELECT CALENDAR_QUARTER(CloseDate) qtr, SUM(Amount)
FROM Opportunity
WHERE IsWon = true AND CloseDate = THIS_YEAR
GROUP BY CALENDAR_QUARTER(CloseDate)
```

### Hourly (for DateTime fields)

```sql
SELECT HOUR_IN_DAY(CreatedDate) hr, COUNT(Id)
FROM Case
WHERE CreatedDate = THIS_WEEK
GROUP BY HOUR_IN_DAY(CreatedDate)
ORDER BY hr
```

## Common Date Patterns

### Activity in Last 7 Days

```sql
SELECT Id, Name FROM Account
WHERE Id IN (
  SELECT AccountId FROM Task
  WHERE CreatedDate >= LAST_N_DAYS:7 AND AccountId <> null
)
```

### No Activity in 30 Days

```sql
SELECT Id, Name FROM Account
WHERE Id NOT IN (
  SELECT AccountId FROM Task
  WHERE CreatedDate >= LAST_N_DAYS:30 AND AccountId <> null
)
```

### Created Before Converted (Leads)

```sql
SELECT Id, Name, CreatedDate, ConvertedDate
FROM Lead
WHERE IsConverted = true
ORDER BY ConvertedDate DESC
LIMIT 100
```

### Pipeline by Close Date

```sql
SELECT
  CASE
    WHEN CloseDate <= TODAY THEN 'Overdue'
    WHEN CloseDate <= NEXT_N_DAYS:7 THEN 'This Week'
    WHEN CloseDate <= NEXT_N_DAYS:30 THEN 'This Month'
    WHEN CloseDate <= NEXT_N_DAYS:90 THEN 'This Quarter'
    ELSE 'Future'
  END,
  COUNT(Id), SUM(Amount)
FROM Opportunity
WHERE IsClosed = false
-- Note: CASE in SELECT works, but cannot GROUP BY CASE directly
```

*Note: For complex date bucketing, use formula fields or post-processing.*
