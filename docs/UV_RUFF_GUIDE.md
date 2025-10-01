# UV & Ruff Development Guide

## UV Commands

### Initial Setup
```bash
# Sync all dependencies (including dev)
uv sync --dev

# Sync only production dependencies
uv sync
```

### Managing Dependencies
```bash
# Add a new dependency
uv add fastapi

# Add a dev dependency
uv add --dev pytest

# Remove a dependency
uv remove package-name

# Update all dependencies
uv sync --upgrade
```

### Running Commands
```bash
# Run the application
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing
```

### Python REPL
```bash
# Start Python in the UV environment
uv run python

# Or activate the venv manually
source .venv/bin/activate
python
```

## Ruff Commands

### Linting
```bash
# Check for linting issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Show detailed error messages
uv run ruff check --output-format=full .
```

### Formatting
```bash
# Check formatting
uv run ruff format --check .

# Format all files
uv run ruff format .
```

### Combined (Lint + Format)
```bash
# Check both
uv run ruff check . && uv run ruff format --check .

# Fix both
uv run ruff check --fix . && uv run ruff format .
```

## VS Code Integration

The devcontainer is configured to:
- **Auto-format on save** using Ruff
- **Auto-organize imports** on save
- **Show linting errors** inline
- **Use the UV-managed virtual environment** at `/workspace/.venv`

## Lock File

The `uv.lock` file is automatically generated and should be committed to version control. It ensures reproducible builds across all environments.

## Tips

1. **No need for pip**: UV replaces pip entirely
2. **Fast dependency resolution**: UV is written in Rust and is 10-100x faster than pip
3. **Automatic virtual environment**: UV creates `.venv` automatically
4. **Ruff replaces**: black, isort, flake8, pylint (all in one, much faster)
5. **Run scripts**: You can add scripts to `pyproject.toml` under `[project.scripts]`

## Example pyproject.toml Scripts

Add this to your `pyproject.toml`:

```toml
[project.scripts]
dev = "uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
test = "pytest"
lint = "ruff check ."
format = "ruff format ."
```

Then run:
```bash
uv run dev    # Start development server
uv run test   # Run tests
uv run lint   # Lint code
uv run format # Format code
```
