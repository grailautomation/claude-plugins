---
name: reconciliation
description: Reconcile accounts by comparing GL balances to subledgers, bank statements, or third-party data. Use when performing bank reconciliations, GL-to-subledger recs, intercompany reconciliations, or identifying and categorizing reconciling items.
argument-hint: "<account> [period]"
disable-model-invocation: true
---

# Reconciliation

**Important**: This skill assists with reconciliation workflows but does not provide financial advice. All reconciliations should be reviewed by qualified financial professionals before sign-off.

Methodology and best practices for account reconciliation, including GL-to-subledger, bank reconciliations, and intercompany. Covers reconciling item categorization, aging analysis, and escalation.

## Reconciliation Types

### GL to Subledger Reconciliation

Compare the general ledger control account balance to the detailed subledger balance.

**Common accounts:**
- Accounts receivable (GL control vs AR subledger aging)
- Accounts payable (GL control vs AP subledger aging)
- Fixed assets (GL control vs fixed asset register)
- Inventory (GL control vs inventory valuation report)
- Prepaid expenses (GL control vs prepaid amortization schedule)
- Accrued liabilities (GL control vs accrual detail schedules)

**Process:**
1. Pull GL balance for the control account as of period end
2. Pull subledger trial balance or detail report as of the same date
3. Compare totals — they should match if posting is real-time
4. Investigate any differences (timing of posting, manual entries not reflected, interface errors)

**Common causes of differences:**
- Manual journal entries posted to the control account but not reflected in the subledger
- Subledger transactions not yet interfaced to the GL
- Timing differences in batch posting
- Reclassification entries in the GL without subledger adjustment
- System interface errors or failed postings

### Bank Reconciliation

Compare the GL cash balance to the bank statement balance.

**Process:**
1. Obtain the bank statement balance as of period end
2. Pull the GL cash account balance as of the same date
3. Identify outstanding checks (issued but not cleared at the bank)
4. Identify deposits in transit (recorded in GL but not yet credited by bank)
5. Identify bank charges, interest, or adjustments not yet recorded in GL
6. Reconcile both sides to an adjusted balance

**Standard format:**

```
Balance per bank statement:         $XX,XXX
Add: Deposits in transit            $X,XXX
Less: Outstanding checks           ($X,XXX)
Add/Less: Bank errors               $X,XXX
Adjusted bank balance:              $XX,XXX

Balance per general ledger:         $XX,XXX
Add: Interest/credits not recorded  $X,XXX
Less: Bank fees not recorded       ($X,XXX)
Add/Less: GL errors                 $X,XXX
Adjusted GL balance:                $XX,XXX

Difference:                         $0.00
```

### Intercompany Reconciliation

Reconcile balances between related entities to ensure they net to zero on consolidation.

**Process:**
1. Pull intercompany receivable/payable balances for each entity pair
2. Compare Entity A's receivable from Entity B to Entity B's payable to Entity A
3. Identify and resolve differences
4. Confirm all intercompany transactions have been recorded on both sides
5. Verify elimination entries are correct for consolidation

**Common causes of differences:**
- Transactions recorded by one entity but not the other (timing)
- Different FX rates used by each entity
- Misclassification (intercompany vs third-party)
- Disputed amounts or unapplied payments
- Different period-end cut-off practices across entities

## Reconciling Item Categorization

### Category 1: Timing Differences

Items that exist because of normal processing timing and will clear without action:

- **Outstanding checks:** Checks issued and recorded in GL, pending bank clearance
- **Deposits in transit:** Deposits made and recorded in GL, pending bank credit
- **In-transit transactions:** Items posted in one system but pending interface to the other
- **Pending approvals:** Transactions awaiting approval to post in one system

**Expected resolution:** These items should clear within the normal processing cycle (typically 1-5 business days). No adjusting entry needed.

### Category 2: Adjustments Required

Items that require a journal entry to correct:

- **Unrecorded bank charges:** Bank fees, wire charges, returned item fees
- **Unrecorded interest:** Interest income or expense from bank/lender
- **Recording errors:** Wrong amount, wrong account, duplicates
- **Missing entries:** Transactions in one system with no corresponding entry in the other
- **Classification errors:** Correctly recorded but in the wrong account

**Action:** Prepare adjusting journal entry to correct the GL or subledger.

### Category 3: Requires Investigation

Items that cannot be immediately explained:

- **Unidentified differences:** Variances with no obvious cause
- **Disputed items:** Amounts contested between parties
- **Aged outstanding items:** Items that have not cleared within expected timeframes
- **Recurring unexplained differences:** Same type of difference appearing each period

**Action:** Investigate root cause, document findings, escalate if unresolved.

## Aging Analysis for Outstanding Items

Track the age of reconciling items to identify stale items requiring escalation:

| Age Bucket | Status | Action |
|-----------|--------|--------|
| 0-30 days | Current | Monitor — within normal processing cycle |
| 31-60 days | Aging | Investigate — follow up on why item has not cleared |
| 61-90 days | Overdue | Escalate — notify supervisor, document investigation |
| 90+ days | Stale | Escalate to management — potential write-off or adjustment needed |

### Aging Report Format

| Item # | Description | Amount | Date Originated | Age (Days) | Category | Status | Owner |
|--------|-------------|--------|-----------------|------------|----------|--------|-------|
| 1      | [Detail]    | $X,XXX | [Date]          | XX         | [Type]   | [Status] | [Name] |

### Trending

Track reconciling item totals over time to identify growing balances:

- Compare total outstanding items to prior period
- Flag if total reconciling items exceed materiality threshold
- Flag if number of items is growing period over period
- Identify recurring items that appear every period (may indicate process issue)

## Escalation Thresholds

Define escalation triggers based on your organization's risk tolerance:

| Trigger | Threshold (Example) | Escalation |
|---------|---------------------|------------|
| Individual item amount | > $10,000 | Supervisor review |
| Individual item amount | > $50,000 | Controller review |
| Total reconciling items | > $100,000 | Controller review |
| Item age | > 60 days | Supervisor follow-up |
| Item age | > 90 days | Controller / management review |
| Unreconciled difference | Any amount | Cannot close — must resolve or document |
| Growing trend | 3+ consecutive periods | Process improvement investigation |

*Note: Set thresholds based on your organization's materiality level and risk appetite. The examples above are illustrative.*

## Reconciliation Best Practices

1. **Timeliness:** Complete reconciliations within the close calendar deadline (typically T+3 to T+5 business days after period end)
2. **Completeness:** Reconcile all balance sheet accounts on a defined frequency (monthly for material accounts, quarterly for immaterial)
3. **Documentation:** Every reconciliation should include preparer, reviewer, date, and clear explanation of all reconciling items
4. **Segregation:** The person who reconciles should not be the same person who processes transactions in that account
5. **Follow-through:** Track open items to resolution — do not just carry items forward indefinitely
6. **Root cause analysis:** For recurring reconciling items, investigate and fix the underlying process issue
7. **Standardization:** Use consistent templates and procedures across all accounts
8. **Retention:** Maintain reconciliations and supporting detail per your organization's document retention policy

## User-Invoked Workflow

# Account Reconciliation

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

**Important**: This command assists with reconciliation workflows but does not provide financial advice. All reconciliations should be reviewed by qualified financial professionals before sign-off.

Reconcile GL account balances to subledger, bank, or third-party balances. Identify and categorize reconciling items and generate a reconciliation workpaper.

## Usage

```
/finance:reconciliation <account> <period>
```

### Arguments

- `account` — The account or account category to reconcile. Examples:
  - `cash` or `bank` — Bank reconciliation (GL cash to bank statement)
  - `accounts-receivable` or `ar` — AR subledger reconciliation
  - `accounts-payable` or `ap` — AP subledger reconciliation
  - `fixed-assets` or `fa` — Fixed asset subledger reconciliation
  - `intercompany` or `ic` — Intercompany balance reconciliation
  - `prepaid` — Prepaid expense schedule reconciliation
  - `accrued-liabilities` — Accrued liabilities detail reconciliation
  - Any specific GL account code (e.g., `1010`, `2100`)
- `period` — The accounting period end date (e.g., `2024-12`, `2024-12-31`)

## Workflow

### 1. Gather Both Sides of the Reconciliation

If ~~erp or ~~data warehouse is connected:
- Pull the GL balance for the specified account(s) as of period end
- Pull the subledger, bank statement, or third-party balance for comparison
- Pull prior period reconciliation (if available) for outstanding item carryforward

If no data source is connected:
> Connect ~~erp or ~~data warehouse to pull account balances automatically. To reconcile manually, provide:
> 1. **GL side:** The general ledger balance for the account as of period end
> 2. **Other side:** The subledger balance, bank statement balance, or third-party confirmation balance
> 3. **Prior period outstanding items** (optional): Any reconciling items from the prior period reconciliation

### 2. Compare Balances

Calculate the difference between the two sides:

```
GL Balance:                    $XX,XXX.XX
Subledger/Bank/Other Balance:  $XX,XXX.XX
                               ----------
Difference:                    $XX,XXX.XX
```

### 3. Identify Reconciling Items

Analyze the difference and categorize reconciling items:

**Timing Differences** (items that will clear in subsequent periods):
- Outstanding checks / payments issued but not yet cleared
- Deposits in transit / receipts recorded but not yet credited
- Invoices posted in one system but pending in the other
- Accruals awaiting reversal

**Permanent Differences** (items requiring adjustment):
- Errors in recording (wrong amount, wrong account, duplicate entries)
- Missing entries (transactions in one system but not the other)
- Bank fees or charges not yet recorded
- Foreign currency translation differences

**Prior Period Items** (carryforward from prior reconciliation):
- Items from prior period that have now cleared (remove from reconciliation)
- Items from prior period still outstanding (carry forward with aging)

### 4. Generate Reconciliation Workpaper

```
ACCOUNT RECONCILIATION
Account: [Account code] — [Account name]
Period End: [Date]
Prepared by: [User]
Date Prepared: [Today]

RECONCILIATION SUMMARY
=======================

Balance per General Ledger:              $XX,XXX.XX

Add: Reconciling items increasing GL
  [Item description]                     $X,XXX.XX
  [Item description]                     $X,XXX.XX
                                         ---------
  Subtotal additions:                    $X,XXX.XX

Less: Reconciling items decreasing GL
  [Item description]                    ($X,XXX.XX)
  [Item description]                    ($X,XXX.XX)
                                         ---------
  Subtotal deductions:                  ($X,XXX.XX)

Adjusted GL Balance:                     $XX,XXX.XX

Balance per [Subledger/Bank/Other]:      $XX,XXX.XX

Add: Reconciling items
  [Item description]                     $X,XXX.XX

Less: Reconciling items
  [Item description]                    ($X,XXX.XX)

Adjusted [Other] Balance:                $XX,XXX.XX

DIFFERENCE:                              $0.00
```

### 5. Reconciling Items Detail

Present each reconciling item with:

| # | Description | Amount | Category | Age (Days) | Status | Action Required |
|---|-------------|--------|----------|------------|--------|-----------------|
| 1 | [Detail]    | $X,XXX | Timing   | 5          | Expected to clear | Monitor |
| 2 | [Detail]    | $X,XXX | Error    | N/A        | Requires correction | Post adjusting JE |

### 6. Review and Escalation

Flag items that require attention:

- **Aged items:** Reconciling items outstanding more than 30/60/90 days
- **Large items:** Individual items exceeding materiality thresholds
- **Growing balances:** Reconciling item totals increasing period over period
- **Unresolved prior period items:** Items carried forward without resolution
- **Unexplained differences:** Amounts that cannot be tied to specific transactions

### 7. Output

Provide:
1. The formatted reconciliation workpaper
2. List of reconciling items with categorization and aging
3. Required adjusting entries (if any permanent differences identified)
4. Action items for items requiring follow-up
5. Comparison to prior period reconciliation (if available)
6. Sign-off section for preparer and reviewer
