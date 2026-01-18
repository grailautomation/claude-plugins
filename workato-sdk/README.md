# Workato SDK Plugin

Workato Connector SDK best practices for recipe developer UX.

## Overview

This plugin provides guidance for building Workato custom connectors with excellent recipe developer experience. It focuses on:

- **Field visibility patterns** — `sticky: true`, `default:` values
- **Dynamic schemas** — `extends_schema`, `ngIf` conditionals
- **Input patterns** — Control types, type conversions
- **Schema design** — Object definitions, methods, pick lists

## Skills

### workato-connector-ux

Triggers when users ask about:
- Building Workato connectors
- Creating custom connectors
- Improving connector UX
- Adding input fields
- Using `sticky`, `extends_schema`, `ngIf`
- Working with Workato SDK Ruby DSL

## Installation

This plugin is part of the local-plugins marketplace. Enable it in Claude Code settings.

## Contents

```
workato-sdk/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── workato-connector-ux/
│       ├── SKILL.md
│       └── references/
│           ├── field-patterns.md
│           ├── control-types.md
│           └── schema-patterns.md
└── README.md
```

## Usage

The skill activates automatically when discussing Workato connector development. Key topics:

- "How do I make a field always visible?" → Use `sticky: true`
- "How do I show fields conditionally?" → Use `ngIf` expressions
- "How do I pre-select a dropdown value?" → Use `default:`
- "How do I refresh fields when selection changes?" → Use `extends_schema: true`

## Reference Topics

- **Field Patterns**: sticky, default, optional, ordering
- **Control Types**: text, select, integer, checkbox, schema-designer
- **Schema Patterns**: object_definitions, methods, config_fields, pick_lists
