---
name: salesforce-reference
description: Salesforce object schema, field names, and relationships. Use when building SOQL queries to understand object structures and field types.
user-invocable: false
---

# Salesforce Object Reference

This skill provides reference information for Salesforce standard objects.

## Quick Object Lookup

| Object | Key Fields | Relationships |
|--------|-----------|---------------|
| Account | Id, Name, BillingCity, Industry, Type | Contacts, Opportunities, Cases |
| Contact | Id, FirstName, LastName, Email, AccountId | Account, Cases, Opportunities |
| Opportunity | Id, Name, Amount, CloseDate, StageName, AccountId | Account, OpportunityLineItems |
| Lead | Id, FirstName, LastName, Email, Company, Status | ConvertedAccount, ConvertedContact |
| Case | Id, Subject, Status, Priority, AccountId, ContactId | Account, Contact |
| Contract | Id, ContractNumber, Status, StartDate, AccountId | Account |
| Task | Id, Subject, Status, Priority, WhoId, WhatId | Who (Contact/Lead), What (any object) |
| Event | Id, Subject, StartDateTime, EndDateTime, WhoId | Who, What |

## Detailed References

For complete field lists, see:
- [Core Objects](core-objects.md) - Account, Contact, Opportunity, Lead, Case, Contract
- [Activity Objects](activity-objects.md) - Task, Event, ActivityHistory
- [Relationships](relationships.md) - How objects relate to each other

## Common Field Patterns

### Standard Fields (All Objects)
- `Id` - 18-character unique identifier
- `Name` - Record name (auto-generated or editable)
- `CreatedDate`, `LastModifiedDate` - Timestamps
- `CreatedById`, `LastModifiedById` - User references
- `OwnerId` - Record owner
- `IsDeleted` - Soft delete flag (use `--all-rows` to include)
- `RecordTypeId` - Record type reference

### Custom Fields
- End with `__c` (e.g., `Custom_Field__c`)
- Custom relationships end with `__r` (e.g., `Custom_Object__r.Name`)

### Relationship Naming
- Standard child-to-parent: Use field name without `Id` (e.g., `Account.Name` not `AccountId.Name`)
- Custom child-to-parent: Replace `__c` with `__r` (e.g., `Custom_Lookup__r.Name`)
- Parent-to-child: Use relationship name (e.g., `Contacts`, `Opportunities`)

## Org-Specific Schemas

For org-specific custom objects and fields, check `org-schemas/<org-name>/` directory.
