# Activity Objects

## Task

The Task object represents a to-do item or action.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Task ID | id | Primary key |
| Subject | Subject | combobox | |
| Description | Comments | textarea | Long text - NOT filterable |
| Status | Status | picklist | Not Started, In Progress, Completed, etc. |
| Priority | Priority | picklist | High, Normal, Low |
| ActivityDate | Due Date | date | |
| WhoId | Name | reference | Contact or Lead |
| WhatId | Related To | reference | Any object (polymorphic) |
| OwnerId | Assigned To | reference | User |
| IsRecurrence | Create Recurring Series | boolean | |
| IsClosed | Closed | boolean | Computed |
| IsHighPriority | High Priority | boolean | Computed |
| TaskSubtype | Task Subtype | picklist | Task, Email, Call, etc. |
| Type | Type | picklist | |

### Polymorphic Relationships

The `WhoId` and `WhatId` fields are polymorphic:
- `WhoId` can reference Contact or Lead
- `WhatId` can reference Account, Opportunity, Case, or custom objects

To query the related object type:
```sql
SELECT Id, Subject, Who.Type, What.Type FROM Task
```

---

## Event

The Event object represents a calendar event.

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Event ID | id | Primary key |
| Subject | Subject | combobox | |
| Description | Description | textarea | Long text - NOT filterable |
| Location | Location | string | |
| StartDateTime | Start Date/Time | datetime | |
| EndDateTime | End Date/Time | datetime | |
| IsAllDayEvent | All-Day Event | boolean | |
| DurationInMinutes | Duration | int | Computed |
| WhoId | Name | reference | Contact or Lead |
| WhatId | Related To | reference | Any object (polymorphic) |
| OwnerId | Assigned To | reference | User |
| ShowAs | Show Time As | picklist | Busy, Free, Out of Office |
| IsRecurrence | Create Recurring Series | boolean | |
| IsPrivate | Private | boolean | |
| Type | Type | picklist | |

---

## ActivityHistory

ActivityHistory is a read-only view of completed activities (Tasks and Events) related to a record.

### Querying ActivityHistory

ActivityHistory is accessed via a subquery from a parent object:

```sql
SELECT Id, Name,
  (SELECT Id, Subject, ActivityDate, Status FROM ActivityHistories ORDER BY ActivityDate DESC LIMIT 5)
FROM Account WHERE Id = '001xxx'
```

### Key Fields

| API Name | Label | Type | Notes |
|----------|-------|------|-------|
| Id | Activity ID | id | |
| Subject | Subject | string | |
| ActivityDate | Date | date | |
| ActivityType | Type | picklist | Call, Email, Meeting, etc. |
| Status | Status | string | For Tasks only |
| Description | Comments | string | |
| WhoId | Name | reference | |
| OwnerId | Assigned To | reference | |
| IsTask | Is Task | boolean | True for Tasks, False for Events |

---

## OpenActivity

OpenActivity is a read-only view of open/upcoming activities related to a record.

### Querying OpenActivity

```sql
SELECT Id, Name,
  (SELECT Id, Subject, ActivityDate, Status FROM OpenActivities ORDER BY ActivityDate ASC LIMIT 5)
FROM Opportunity WHERE Id = '006xxx'
```
