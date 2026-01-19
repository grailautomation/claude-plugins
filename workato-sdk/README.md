# Workato SDK Plugin

Comprehensive Workato Connector SDK documentation and best practices for Claude Code.

## Overview

This plugin provides expertise for building Workato custom connectors, covering:

- **Complete SDK Documentation** — All SDK blocks, methods, and patterns
- **Authentication** — OAuth 2.0, API key, JWT, AWS Signature, multi-auth
- **Actions & Triggers** — Building operations with proper schemas
- **CLI & Testing** — Local development with workato gem and RSpec
- **Best Practices** — UX patterns, error handling, performance

## Skills

### Core Documentation

| Skill | Triggers When User Asks About |
|-------|------------------------------|
| **workato-sdk-quickstart** | "getting started", "first connector", "connector examples", "walkthrough" |
| **workato-sdk-reference** | "sdk reference", "actions block", "triggers block", "object_definitions", "methods block" |
| **workato-sdk-cli** | "workato cli", "workato gem", "rspec test", "vcr cassettes", "workato exec" |

### Building Connectors

| Skill | Triggers When User Asks About |
|-------|------------------------------|
| **workato-sdk-authentication** | "oauth workato", "api key auth", "jwt authentication", "connection block" |
| **workato-sdk-actions** | "build action", "execute block", "streaming action", "multistep action" |
| **workato-sdk-triggers** | "poll trigger", "webhook trigger", "dynamic webhook", "dedup", "closure" |
| **workato-sdk-data-formats** | "request_format", "xml format", "multipart form", "parse xml" |

### Advanced Topics

| Skill | Triggers When User Asks About |
|-------|------------------------------|
| **workato-sdk-advanced** | "connector planning", "code patterns", "best practices", "error handling" |
| **workato-connector-ux** | "sticky fields", "extends_schema", "ngIf", "input field UX" |

## Installation

This plugin is part of the local-plugins marketplace. Enable it in Claude Code settings.

## Contents

```
workato-sdk/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── workato-connector-ux/      # UX patterns & field visibility
│   ├── workato-sdk-quickstart/    # Getting started guide
│   ├── workato-sdk-reference/     # SDK API reference
│   ├── workato-sdk-cli/           # CLI & local testing
│   ├── workato-sdk-authentication/ # Auth implementations
│   ├── workato-sdk-actions/       # Building actions
│   ├── workato-sdk-triggers/      # Building triggers
│   ├── workato-sdk-data-formats/  # Request/response formats
│   └── workato-sdk-advanced/      # Advanced patterns
└── README.md
```

Each skill contains:
- `SKILL.md` — Core guidance and common patterns
- `references/` — Detailed documentation from Workato SDK docs

## Usage Examples

Skills activate automatically based on context:

- "How do I authenticate with OAuth 2.0?" → workato-sdk-authentication
- "How do I build a polling trigger?" → workato-sdk-triggers
- "How do I test my connector locally?" → workato-sdk-cli
- "How do I handle XML responses?" → workato-sdk-data-formats
- "How do I make a field always visible?" → workato-connector-ux

## Documentation Coverage

The plugin includes 90+ SDK documentation pages covering:

- SDK Reference (actions, triggers, connection, methods, streams, etc.)
- Authentication guides (OAuth variants, API key, JWT, AWS, multi-auth)
- Building actions (CRUD patterns, streaming, multistep, wait-for-resume)
- Building triggers (poll, static/dynamic webhooks, hybrid)
- CLI guides (installation, testing, actions, triggers, RSpec)
- Data formats (JSON, XML, multipart, form-encoded)
- Advanced patterns (planning, code patterns, error handling, best practices)
