---
description: Describe a Salesforce object to see its fields, relationships, and metadata
allowed-tools: ["Bash"]
---

# Describe Salesforce Object

Get the schema for: $ARGUMENTS

## Execution

Run the sf CLI describe command:

```bash
sf sobject describe --sobject <ObjectApiName> --target-org <alias> --json
```

## Useful Patterns

### Get All Field Names and Types

```bash
sf sobject describe --sobject Account --target-org production --json 2>&1 | \
  grep -E '"name"|"type"|"label"' | head -100
```

### Get Custom Fields Only

```bash
sf sobject describe --sobject Account --target-org production --json 2>&1 | \
  grep -E '"name".*__c'
```

### Get Relationship Fields

```bash
sf sobject describe --sobject Account --target-org production --json 2>&1 | \
  grep -E '"relationshipName"|"referenceTo"'
```

### Get Picklist Values

```bash
sf sobject describe --sobject Opportunity --target-org production --json 2>&1 | \
  grep -A 50 '"name": "StageName"' | grep -E '"value"|"label"' | head -30
```

## Output Fields of Interest

| Field | Description |
|-------|-------------|
| `name` | API name of the field |
| `label` | Display label |
| `type` | Field type (string, picklist, reference, etc.) |
| `length` | Max length for text fields |
| `referenceTo` | Related object(s) for lookup/master-detail fields |
| `relationshipName` | Name to use in SOQL for traversing relationships |
| `picklistValues` | Available values for picklist fields |
| `filterable` | Whether the field can be used in WHERE clauses |

## For Tooling API Objects

Use `--use-tooling-api` for metadata objects like ApexClass, ApexTrigger:

```bash
sf sobject describe --sobject ApexClass --use-tooling-api --target-org production --json
```
