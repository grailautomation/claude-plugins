# Contract (Subscription) - Mural Production

## Overview

Contracts in Mural represent subscriptions, primarily synced from Stripe via Workato. The display name in the UI is "Subscription" but the API name is `Contract`.

## Key Custom Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Stripe_Customer_Id__c | Stripe Customer Id | Text | Links to Stripe Customer |
| Stripe_Subscription_Id__c | Stripe Subscription Id | Text | Links to Stripe Subscription |
| Stripe_Workspace_Id__c | Stripe Workspace Id | Text | Mural workspace identifier |
| Stripe_Plan__c | Stripe Plan | Text | Subscription plan name |
| Stripe_End_Date__c | Stripe End Date | Date | Subscription end date from Stripe |
| Stripe_Transaction_Value__c | Stripe Transaction Value | Currency | Transaction amount |
| Cancel_At_End_Period_Stripe__c | Cancel At End Period (Stripe) | Checkbox | Subscription set to cancel |
| Workspace__c | Workspace | Lookup | Links to Workspace object |

## Standard Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| ContractNumber | Contract Number | Auto Number | e.g., 00157334 |
| AccountId | Account | Lookup | Parent account |
| Status | Status | Picklist | Draft, In Approval, Activated |
| StartDate | Contract Start Date | Date | |
| EndDate | Contract End Date | Date | Computed |
| ContractTerm | Contract Term (months) | Number | |
| CustomerSignedId | Customer Signed By | Lookup(Contact) | |

## Status Values

| Value | Description |
|-------|-------------|
| Draft | Not yet activated |
| In Approval | Pending approval |
| Activated | Active subscription |
| Churned | Cancelled/churned |

## Relationships

| Field | Related Object | Relationship Name |
|-------|----------------|-------------------|
| AccountId | Account | Account |
| CustomerSignedId | Contact | CustomerSigned |
| Workspace__c | Workspace | Workspace |

## Common Queries

### Contracts by Stripe Customer ID

```sql
SELECT Id, ContractNumber, AccountId, Account.Name,
       Stripe_Subscription_Id__c, Stripe_Customer_Id__c,
       Stripe_Workspace_Id__c, Status, CreatedDate
FROM Contract
WHERE Stripe_Customer_Id__c = 'cus_XXXXX'
```

### Active Contracts with Stripe Data

```sql
SELECT Id, ContractNumber, Account.Name,
       Stripe_Customer_Id__c, Stripe_Subscription_Id__c, Status
FROM Contract
WHERE Stripe_Customer_Id__c <> null
  AND Status = 'Activated'
ORDER BY CreatedDate DESC
LIMIT 100
```

### Contracts Created Since Date

```sql
SELECT Id, ContractNumber, AccountId, Account.Name,
       Stripe_Subscription_Id__c, Stripe_Customer_Id__c, CreatedDate
FROM Contract
WHERE Stripe_Customer_Id__c <> null
  AND CreatedDate >= 2025-01-01T00:00:00Z
ORDER BY CreatedDate DESC
```

### Count Contracts by Status

```sql
SELECT Status, COUNT(Id) FROM Contract GROUP BY Status
```

### Contracts for Specific Stripe Customers (Bulk)

```sql
SELECT Id, ContractNumber, AccountId, Account.Name,
       Stripe_Subscription_Id__c, Stripe_Customer_Id__c
FROM Contract
WHERE Stripe_Customer_Id__c IN ('cus_XXX', 'cus_YYY', 'cus_ZZZ')
```

## Stripe Sync Notes

- Contracts are created/updated by Workato's Stripe-to-Salesforce sync
- The sync matches Stripe Customers to Salesforce Accounts using email/domain logic
- ~50% accuracy historically for account matching
- Use `Forecast_Notes__c` on Opportunities as an "answer key" for expected Account mapping
