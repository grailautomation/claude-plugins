# Python Version Management

## Installing Python Versions

```bash
# Install Python version
uv python install 3.12

# Install multiple versions
uv python install 3.11 3.12 3.13

# Install latest version
uv python install

# List installed versions
uv python list

# Find available versions
uv python list --all-versions
```

## Setting Python Version

```bash
# Set Python version for project (creates/updates .python-version)
uv python pin 3.12

# Use specific Python version for a command
uv --python 3.11 run python script.py

# Create venv with specific version
uv venv --python 3.12
```
