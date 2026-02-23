---
name: plan-editing
description: How to modify issue-blaster plans before implementation
---

# Editing Plans

Plans can be modified before implementation to adjust the approach.

## When to Edit vs. Regenerate

**Edit the plan when**:
- Adjusting a single step
- Adding clarifying details
- Changing file paths
- Reordering steps

**Regenerate when**:
- Fundamentally different approach needed
- Issue requirements changed
- Multiple steps need rewriting

## Safe Modifications

### Changing a Step

```markdown
### Step 3: Add validation
- **File**: `src/validators.py`
- **Action**: modify
- **Changes**: Add email format validation using regex
```

Can be edited to:

```markdown
### Step 3: Add validation
- **File**: `src/validators.py`
- **Action**: modify
- **Changes**: Add email format validation using the `email-validator` library
```

### Adding a Step

Insert a new step with the next number:

```markdown
### Step 4: Add unit tests
- **File**: `tests/test_validators.py`
- **Action**: create
- **Changes**: Add tests for email validation edge cases
```

### Removing a Step

Delete the step entirely and renumber subsequent steps.

### Updating Frontmatter

Update `status` when making decisions:

```yaml
status: accepted  # Changed from 'proposed'
```

Add notes about modifications:

```yaml
modified: 2024-12-18T14:00:00Z
modified_by: "Changed step 3 to use email-validator library"
```

## Preserving Structure

The implementer expects this structure:
- Frontmatter must be valid YAML between `---` markers
- Each step needs `### Step N:` heading
- Steps should have `File`, `Action`, `Changes` fields

Avoid:
- Removing required frontmatter fields
- Changing the step heading format
- Nesting steps within other sections
