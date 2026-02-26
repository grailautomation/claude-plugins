# Migration Guide

## From pip + requirements.txt

```bash
# Before
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# After (quick migration)
uv venv
uv pip install -r requirements.txt

# After (full migration to uv project)
uv init
uv add -r requirements.txt
```

## From Poetry

```bash
# Before
poetry install
poetry add requests

# After
uv sync
uv add requests

# Keep existing pyproject.toml
# uv reads [project] and [tool.poetry] sections
```

## From pip-tools

```bash
# Before
pip-compile requirements.in
pip-sync requirements.txt

# After
uv lock
uv sync --frozen
```
