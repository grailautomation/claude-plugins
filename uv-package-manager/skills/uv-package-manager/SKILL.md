---
name: uv-package-manager
version: 0.1.0
user-invocable: true
description: >-
  This skill should be used when the user asks to "set up a Python project
  with uv", "manage Python dependencies", "configure uv", "create a virtual
  environment with uv", "migrate from pip to uv", "speed up CI with uv",
  or when working with uv for virtual environments, package management,
  lockfiles, Docker builds, or Python version management.
---

# uv Package Manager

Fast Python package installer and resolver written in Rust. 10-100x faster than pip, with built-in virtual environment management, Python version management, and lockfile support.

## When to Activate

- Setting up new Python projects
- Managing Python dependencies
- Creating and managing virtual environments
- Installing or pinning Python interpreters
- Resolving dependency conflicts
- Migrating from pip, pip-tools, or poetry
- Optimizing CI/CD pipelines or Docker builds
- Working with lockfiles for reproducible builds
- Managing monorepo Python projects

## Quick Start

```bash
# Create a new project
uv init my-project
cd my-project

# Add dependencies
uv add requests pandas

# Add dev dependencies
uv add --dev pytest black ruff

# Sync all dependencies (creates venv if needed)
uv sync

# Run commands in the virtual environment
uv run pytest
uv run python app.py
```

## Essential Commands

```bash
# Project management
uv init [PATH]              # Initialize project
uv add PACKAGE              # Add dependency
uv remove PACKAGE           # Remove dependency
uv sync                     # Install dependencies
uv lock                     # Create/update lockfile

# Virtual environments
uv venv [PATH]              # Create venv
uv run COMMAND              # Run in venv (no activation needed)

# Python management
uv python install VERSION   # Install Python
uv python list              # List installed Pythons
uv python pin VERSION       # Pin Python version

# Package installation (pip-compatible)
uv pip install PACKAGE      # Install package
uv pip uninstall PACKAGE    # Uninstall package
uv pip freeze               # List installed
uv pip list                 # List packages

# Utility
uv cache clean              # Clear cache
uv --version                # Show version
```

## Best Practices

1. **Always use lockfiles** — Commit `uv.lock` for reproducibility
2. **Pin Python version** — Use `.python-version` via `uv python pin`
3. **Separate dev dependencies** — Use `uv add --dev` for test/lint tools
4. **Prefer `uv run`** — Avoid manual venv activation
5. **Use `--frozen` in CI** — Exact reproduction from lockfile
6. **Leverage global cache** — uv shares a cache across all projects
7. **Use workspaces** — For monorepo projects with `[tool.uv.workspace]`
8. **Export for compatibility** — `uv export --format requirements-txt` when needed

## Reference Documentation

Detailed guides for each workflow:

- **Virtual Environments** — [references/virtual-environments.md](references/virtual-environments.md) — Creating, activating, `uv run`
- **Package Management** — [references/package-management.md](references/package-management.md) — Adding, removing, upgrading, locking deps
- **Python Versions** — [references/python-versions.md](references/python-versions.md) — Installing, pinning Python versions
- **Project Configuration** — [references/project-configuration.md](references/project-configuration.md) — pyproject.toml, existing projects, monorepo
- **CI/CD & Docker** — [references/ci-cd-docker.md](references/ci-cd-docker.md) — GitHub Actions, multi-stage Dockerfiles
- **Lockfiles & Caching** — [references/lockfiles-caching.md](references/lockfiles-caching.md) — Lockfile workflows, cache, parallel, offline
- **Migration Guide** — [references/migration-guide.md](references/migration-guide.md) — From pip, poetry, pip-tools
- **Tooling Integration** — [references/tooling-integration.md](references/tooling-integration.md) — Pre-commit hooks, VS Code settings

## Resources

- [Official documentation](https://docs.astral.sh/uv/)
- [GitHub repository](https://github.com/astral-sh/uv)
- [Migration guides](https://docs.astral.sh/uv/guides/)
