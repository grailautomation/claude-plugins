# Lockfiles and Caching

## Lockfile Workflows

```bash
# Create lockfile (uv.lock)
uv lock

# Install from lockfile (exact versions)
uv sync --frozen

# Update lockfile without installing
uv lock --no-install

# Upgrade specific package in lock
uv lock --upgrade-package requests

# Check if lockfile is up to date
uv lock --check

# Export lockfile to requirements.txt
uv export --format requirements-txt > requirements.txt

# Export with hashes for security
uv export --format requirements-txt --hash > requirements.txt
```

## Global Cache

```bash
# UV automatically uses global cache at:
# Linux: ~/.cache/uv
# macOS: ~/Library/Caches/uv
# Windows: %LOCALAPPDATA%\uv\cache

# Clear cache
uv cache clean

# Check cache location
uv cache dir
```

## Parallel Installation

```bash
# UV installs packages in parallel by default

# Control parallelism
uv pip install --jobs 4 package1 package2

# Sequential (no parallel)
uv pip install --jobs 1 package
```

## Offline Mode

```bash
# Install from cache only (no network)
uv pip install --offline package

# Sync from lockfile offline
uv sync --frozen --offline
```
