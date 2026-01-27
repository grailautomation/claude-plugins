# Custom Objects - Mural Production

## Overview

This document provides a reference for custom objects in the Mural Salesforce org.

## Key Custom Objects

| API Name | Description |
|----------|-------------|
| Team__c | Mural workspace teams |
| Workspaces__c | Mural workspaces |
| Subscription_Relationship__c | Links between subscriptions |
| Account_Snapshot__c | Point-in-time account snapshots |
| Opportunity_Snapshots__c | Point-in-time opportunity snapshots |
| Invoice__c | Invoice records |
| BP_Invoice__c | Billing platform invoices |
| Contract_Price__c | Contract pricing details |
| Product_Quantity_Tier__c | Quantity tier pricing |
| VR__c | (Unknown - investigate) |

## Managed Package Objects

Objects from installed packages (use package prefix in queries):

### Gainsight (JBCXM__)
- `JBCXM__C360Sections__c`
- `JBCXM__ScorecardConfig__c`
- `JBCXM__Widgets__c`
- `JBCXM__UsageTracker__c`

### LeanData (LeanData__)
- `LeanData__Tagging_Log__c`
- `LeanData__Quarterly_Metric__c`

### ZoomInfo (DOZISF__)
- `DOZISF__ZoomInfo_Scoop__c`

### Gong (Gong__)
- `Gong__Topic__c`
- `Gong__Note__c`
- `Gong__Gong_Scorecard__c`

### Celigo (integrator_da__, celigo_sfnsio__)
- `integrator_da__Celigo_Queued_Message__c`
- `celigo_sfnsio__Contract_Item__c`

## Describing Custom Objects

To get details about a custom object:

```bash
sf sobject describe --sobject Team__c --target-org production --json
```

To get field names:

```bash
sf sobject describe --sobject Team__c --target-org production --json 2>&1 | \
  grep -E '"name"|"label"|"type"' | paste - - -
```

## Query Examples

### Team Records

```sql
SELECT Id, Name, CreatedDate FROM Team__c LIMIT 10
```

### Workspace Records

```sql
SELECT Id, Name, CreatedDate FROM Workspaces__c LIMIT 10
```

### Account Snapshots

```sql
SELECT Id, Name, Account__c, SnapshotDate__c FROM Account_Snapshot__c
WHERE SnapshotDate__c >= LAST_N_DAYS:30
ORDER BY SnapshotDate__c DESC
```

## Adding Object Documentation

For detailed field-level documentation of a specific custom object, create a new file:

```
org-schemas/mural-production/<object-name>.md
```

Use the object file template from the README.
