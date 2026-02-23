# Issue Solver

A Claude Code plugin for analyzing GitHub issues and implementing AI-generated solution plans.

## Features

- **Solve**: Analyze GitHub issues and generate 2-4 solution plans
- **Implement**: Execute solution plans via worktrees with automated branching, commits, and merge options
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

The `plan-implementer` agent handles implementation. Invoke it naturally:

```
implement option 1 for issue 123
go with option 2 for issue 456
implement plans/issue-123/option-1-fix.md
```

It creates a worktree in `.worktrees/`, implements the plan, commits, and offers merge options (including "leave it" to defer merging).

## Output Structure

```
.worktrees/                          ← gitignored, created during implementation
└── issue-123-minimal-fix/           ← worktree per implementation
plans/                               ← gitignored, created during solving
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

| Agent | Description | Trigger Phrases |
|-------|-------------|-----------------|
| `issue-solver` | Analyzes one issue, generates 2-4 plans | "solve issue", "analyze issue", "create plan for" |
| `plan-implementer` | Implements a chosen plan via worktree | "implement plan", "execute option", "go with option" |

## Commands

| Command | Description |
|---------|-------------|
| `/issue-solver:solve` | Dispatch single or batch issue solving |

## License

MIT
