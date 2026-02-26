# Project Configuration

## pyproject.toml with uv

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    # Additional dev dependencies managed by uv
]

[tool.uv.sources]
# Custom package sources
my-package = { git = "https://github.com/user/repo.git" }
```

## Using uv with Existing Projects

```bash
# Migrate from requirements.txt
uv add -r requirements.txt

# Migrate from poetry (already have pyproject.toml)
uv sync

# Export to requirements.txt
uv pip freeze > requirements.txt

# Export with hashes
uv pip freeze --require-hashes > requirements.txt
```

## Monorepo Support

```bash
# Project structure
# monorepo/
#   packages/
#     package-a/
#       pyproject.toml
#     package-b/
#       pyproject.toml
#   pyproject.toml (root)

# Root pyproject.toml
# [tool.uv.workspace]
# members = ["packages/*"]

# Install all workspace packages
uv sync

# Add workspace dependency
uv add --path ./packages/package-a
```
