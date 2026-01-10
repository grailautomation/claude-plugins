# Issue Solver

A Claude Code plugin for analyzing GitHub issues and implementing AI-generated solution plans.

## Features

- **Solve**: Analyze GitHub issues and generate 2-4 solution plans
- **Implement**: Execute solution plans by creating branches and implementing changes
- **Parallel Processing**: Solve multiple issues concurrently using Task tool

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`) for code search

## Installation

### Via Plugin Marketplace

```bash
# Install from marketplace (when published)
/plugin install issue-solver@claude-plugins
```

### Manual Installation

```bash
git clone https://github.com/kreitter/issue-solver ~/.claude-plugins/issue-solver
```

Then add to your Claude Code settings.

## Usage

### Solve Issues

```bash
# Solve a single issue
/issue-solver:solve 123

# Solve multiple issues in parallel
/issue-solver:solve 1 2 3

# Specify repository explicitly
/issue-solver:solve 123 --repo owner/repo
```

### Implement Plans

```bash
# Implement by issue and option number
/issue-solver:implement 123 1

# Implement by plan path
/issue-solver:implement plans/issue-123/option-1-fix.md
```

## Output Structure

```
plans/
└── issue-123/
    ├── option-1-minimal-fix.md
    ├── option-2-refactor.md
    └── option-3-new-abstraction.md
```

Each plan file contains:
- YAML frontmatter with metadata (issue number, effort, breaking changes)
- Issue summary and research findings
- Step-by-step implementation plan
- Pros/cons analysis

## Agents

This plugin provides two agents:

| Agent | Description | Trigger Phrases |
|-------|-------------|-----------------|
| `issue-solver` | Analyzes issues and generates plans | "solve issue", "analyze issue", "create plan for" |
| `plan-implementer` | Executes solution plans | "implement plan", "execute option", "go with option" |

## License

MIT
