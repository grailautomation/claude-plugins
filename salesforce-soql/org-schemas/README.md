# Org-Specific Schemas

This folder contains org-specific schema documentation for Salesforce orgs.

## Adding a New Org

1. Create a folder with your org's name or alias:
   ```
   org-schemas/my-company-production/
   ```

2. Add a `manifest.md` with org metadata

3. Add object-specific files for custom objects and customized standard objects

## Structure

```
org-schemas/
└── <org-name>/
    ├── manifest.md          # Org metadata and overview
    ├── opportunity.md       # Customized Opportunity object
    ├── contract.md          # Customized Contract object
    ├── custom-object.md     # Custom object documentation
    └── ...
```

## Object File Template

```markdown
# Object Name - Org Name

## Overview
Brief description of how this object is used in this org.

## Record Types
| DeveloperName | Display Name | Description |
|---------------|--------------|-------------|

## Key Custom Fields
| API Name | Label | Type | Notes |
|----------|-------|------|-------|

## Picklist Values
### Field Name
| Value | Label |
|-------|-------|

## Relationships
| Field | Related Object | Type |
|-------|----------------|------|
```

## Generating Schema Documentation

Use the `/describe` command or `sf sobject describe` to get field information:

```bash
sf sobject describe --sobject ObjectName --target-org production --json
```

Extract field info:
```bash
sf sobject describe --sobject Account --target-org production --json 2>&1 | \
  grep -E '"name"|"label"|"type"' | paste - - -
```
