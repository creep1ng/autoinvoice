# Settings Configuration - AutoInvoice

This document describes the settings configuration system for the AutoInvoice project using `pydantic-settings`.

## Overview

The `src/config/settings.py` file provides a centralized configuration system that:

- ✅ Loads configuration from environment variables
- ✅ Supports `.env` files for local development
- ✅ Provides type validation using Pydantic
- ✅ Offers sensible defaults for all settings
- ✅ Computes derived properties (e.g., database URLs)
- ✅ Is cached for performance (singleton pattern)

## File Location

```
src/config/settings.py
```

## Settings Class

The `Settings` class is a Pydantic model that automatically reads from:

1. Environment variables
2. `.env` file (if present)
3. Default values (if not specified)

### Model Configuration

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",              # Read from .env file
        env_file_encoding="utf-8",    # UTF-8 encoding
        case_sensitive=False,         # ENV_VAR and env_var both work
        extra="ignore",               # Ignore unknown env vars
    )
```

## Available Settings

### Application Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `app_name` | `str` | `"AutoInvoice"` | Application name |
| `app_version` | `str` | `"0.1.0"` | Application version |
| `debug` | `bool` | `False` | Enable debug mode |

**Environment variables:**
```env
APP_NAME=AutoInvoice
APP_VERSION=0.1.0
DEBUG=true
```

### Logging Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `log_level` | `str` | `"INFO"` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `log_format` | `str` | `"text"` | Log format: 'text' or 'json' |
| `log_file` | `str \| None` | `None` | Log file path (None disables file logging) |
| `log_file_max_bytes` | `int` | `10485760` | Maximum log file size (10MB) |
| `log_file_backup_count` | `int` | `5` | Number of backup log files to keep |

**Environment variables:**
```env
LOG_LEVEL=INFO
LOG_FORMAT=text
LOG_FILE=logs/autoinvoice.log
LOG_FILE_MAX_BYTES=10485760
LOG_FILE_BACKUP_COUNT=5
```

### Database Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `postgres_host` | `str` | `"localhost"` | PostgreSQL host |
| `postgres_port` | `int` | `5432` | PostgreSQL port |
| `postgres_user` | `str` | `"autoinvoice"` | PostgreSQL username |
| `postgres_password` | `str` | `"autoinvoice"` | PostgreSQL password |
| `postgres_db` | `str` | `"autoinvoice"` | PostgreSQL database name |

**Environment variables:**
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=autoinvoice
POSTGRES_PASSWORD=autoinvoice
POSTGRES_DB=autoinvoice
```

**Derived property:**
```python
settings.database_url  # Returns: postgresql+psycopg://user:pass@host:port/db
```

### OpenAI Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `openai_api_key` | `str \| None` | `None` | OpenAI API key |
| `openai_model` | `str` | `"gpt-4o-mini"` | OpenAI model to use |

**Environment variables:**
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### Path Properties

| Property | Type | Description |
|----------|------|-------------|
| `project_root` | `Path` | Project root directory (computed) |
| `logs_dir` | `Path` | Logs directory (computed, auto-created) |

## Usage

### Basic Usage

```python
from src.config import settings

# Access settings
print(settings.app_name)           # "AutoInvoice"
print(settings.log_level)          # "INFO"
print(settings.database_url)       # "postgresql+psycopg://..."
print(settings.project_root)       # PosixPath('/workspace')
```

### In Application Initialization

```python
from src.config import settings, setup_logging

# Initialize logging with settings
setup_logging(settings)

# Use database URL with SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine(settings.database_url)
```

### In FastAPI Application

```python
from fastapi import FastAPI
from src.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

@app.get("/config")
async def get_config():
    """Return non-sensitive configuration."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "log_level": settings.log_level,
    }
```

### In Service Classes

```python
from src.config import settings
from langchain_openai import ChatOpenAI

class InvoiceExtractor:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0,
        )
    
    def extract_invoice_data(self, text: str):
        # Use LLM to extract data
        pass
```

### In Database Modules

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

# Create engine using settings
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL if debug is enabled
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
```

## get_settings() Function

The `get_settings()` function returns a cached instance of the Settings class (singleton pattern):

```python
from src.config import get_settings

# Get settings instance
settings = get_settings()

# Multiple calls return the same instance (cached)
settings1 = get_settings()
settings2 = get_settings()
assert settings1 is settings2  # True
```

**Why use `get_settings()`?**

- **Performance**: Settings are loaded once and cached
- **Consistency**: Same settings throughout the application
- **Testing**: Can be overridden with `lru_cache` clearing

### Overriding Settings in Tests

```python
from functools import lru_cache
from src.config import get_settings, Settings

def test_with_custom_settings():
    # Clear the cache
    get_settings.cache_clear()
    
    # Set test environment variables
    import os
    os.environ["POSTGRES_DB"] = "test_db"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    # Get fresh settings
    settings = get_settings()
    assert settings.postgres_db == "test_db"
    assert settings.log_level == "DEBUG"
    
    # Clean up
    get_settings.cache_clear()
```

## Environment Configuration

### Development Environment

Create a `.env` file in the project root:

```env
# Application
DEBUG=true

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=autoinvoice
POSTGRES_PASSWORD=autoinvoice
POSTGRES_DB=autoinvoice

# OpenAI
OPENAI_API_KEY=sk-your-development-key
OPENAI_MODEL=gpt-4o-mini
```

### Production Environment

Set environment variables directly (e.g., in Docker, Kubernetes, or cloud providers):

```bash
export DEBUG=false
export LOG_LEVEL=INFO
export LOG_FORMAT=json
export LOG_FILE=/var/log/autoinvoice/app.log
export POSTGRES_HOST=prod-db.example.com
export POSTGRES_PASSWORD=secure-password-here
export OPENAI_API_KEY=sk-your-production-key
```

### Docker Compose

In `docker-compose.yml`:

```yaml
services:
  api:
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
      - LOG_FORMAT=json
      - POSTGRES_HOST=db
      - POSTGRES_USER=autoinvoice
      - POSTGRES_PASSWORD=autoinvoice
      - POSTGRES_DB=autoinvoice
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## Adding New Settings

### Step 1: Add to Settings Class

Edit `src/config/settings.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # New setting
    max_file_size_mb: int = Field(
        default=10,
        description="Maximum upload file size in MB",
    )
    
    allowed_file_types: list[str] = Field(
        default=["pdf", "png", "jpg"],
        description="Allowed file types for upload",
    )
```

### Step 2: Update .env.example

Add to `.env.example`:

```env
# File Upload
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=["pdf","png","jpg"]
```

### Step 3: Use in Your Code

```python
from src.config import settings

def validate_upload(file_size: int, file_type: str):
    max_size = settings.max_file_size_mb * 1024 * 1024
    
    if file_size > max_size:
        raise ValueError(f"File too large: {file_size} > {max_size}")
    
    if file_type not in settings.allowed_file_types:
        raise ValueError(f"Invalid file type: {file_type}")
```

## Type Validation

Pydantic automatically validates types:

```python
# ✅ Valid
DEBUG=true              # Parsed as boolean True
DEBUG=false             # Parsed as boolean False
DEBUG=1                 # Parsed as boolean True
DEBUG=0                 # Parsed as boolean False

POSTGRES_PORT=5432      # Parsed as int 5432
POSTGRES_PORT="5432"    # Also parsed as int 5432

# ❌ Invalid (raises ValidationError)
POSTGRES_PORT=not_a_number   # Fails validation
DEBUG=maybe                  # Fails validation
```

## Best Practices

### 1. Use Field() for Documentation

```python
# ❌ Bad - no documentation
max_retries: int = 3

# ✅ Good - documented
max_retries: int = Field(
    default=3,
    description="Maximum number of retry attempts",
    ge=0,  # Greater than or equal to 0
    le=10, # Less than or equal to 10
)
```

### 2. Use Properties for Derived Values

```python
# ✅ Good - computed from other settings
@property
def database_url(self) -> str:
    """Construct database URL."""
    return (
        f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
        f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    )
```

### 3. Don't Hardcode Values

```python
# ❌ Bad - hardcoded
API_KEY = "sk-1234567890"

# ✅ Good - from settings
from src.config import settings
api_key = settings.openai_api_key
```

### 4. Use Type Hints

```python
# ✅ Good - type hints for validation
openai_api_key: str | None = None
postgres_port: int = 5432
debug: bool = False
allowed_extensions: list[str] = [".pdf", ".png"]
```

### 5. Provide Sensible Defaults

```python
# ✅ Good - sensible defaults
log_level: str = Field(default="INFO")
log_format: str = Field(default="text")
max_retries: int = Field(default=3)
```

### 6. Don't Store Secrets in Code

```python
# ❌ Bad - secret in code
postgres_password: str = "my-secret-password"

# ✅ Good - secret from environment
postgres_password: str = Field(default="autoinvoice")
# Then override with: export POSTGRES_PASSWORD=actual-secret
```

## Troubleshooting

### Settings Not Loading

**Problem**: Settings show default values instead of `.env` values

**Solution**:
1. Verify `.env` file exists in project root
2. Check file encoding is UTF-8
3. Verify environment variable names match (case-insensitive)
4. Clear cache: `get_settings.cache_clear()`

### ValidationError

**Problem**: `pydantic.ValidationError` when loading settings

**Solution**:
1. Check environment variable types match expected types
2. Use `DEBUG=true` not `DEBUG=yes` for booleans
3. Use `POSTGRES_PORT=5432` not `POSTGRES_PORT=5432.0` for integers
4. Check Field validators (ge, le, etc.)

### Database Connection Fails

**Problem**: Can't connect to database

**Solution**:
```python
from src.config import settings

print(settings.database_url)  # Check the constructed URL
print(settings.postgres_host)  # Verify individual settings
```

### Secrets Visible in Logs

**Problem**: Sensitive data in logs or error messages

**Solution**: Use Pydantic's `Field` with `repr=False`:

```python
openai_api_key: str | None = Field(
    default=None,
    repr=False,  # Don't include in __repr__
)
```

## Security Considerations

### 1. Never Commit .env Files

Add to `.gitignore`:
```
.env
.env.*
!.env.example
```

### 2. Use Secrets Management in Production

- **AWS**: AWS Secrets Manager or Parameter Store
- **GCP**: Secret Manager
- **Azure**: Key Vault
- **Kubernetes**: Secrets
- **Docker**: Docker Secrets

### 3. Validate Sensitive Settings

```python
openai_api_key: str | None = Field(
    default=None,
    min_length=20,  # Ensure it's not empty or too short
)

@model_validator(mode='after')
def check_api_key_in_production(self):
    if not self.debug and not self.openai_api_key:
        raise ValueError("OPENAI_API_KEY required in production")
    return self
```

## Examples

### Complete Application Setup

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine
from src.config import settings, setup_logging

# Initialize logging
setup_logging(settings)

# Create database engine
engine = create_engine(settings.database_url)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    logger.info(
        "Application starting",
        extra={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
        }
    )
    yield
    # Shutdown
    logger.info("Application shutting down")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)
```

### Dynamic Configuration

```python
from src.config import settings

# Adjust behavior based on environment
if settings.debug:
    # Development mode
    timeout = 60  # Longer timeout for debugging
    retries = 1   # Fewer retries
else:
    # Production mode
    timeout = 10  # Shorter timeout
    retries = 3   # More retries
```

## References

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Pydantic Field Documentation](https://docs.pydantic.dev/latest/concepts/fields/)
- [Environment Variables Best Practices](https://12factor.net/config)
- [Settings Module: `src/config/settings.py`](../src/config/settings.py)

## Related Documentation

- [Logging Configuration](../logging/LOGGING.md)
- [Database Setup](./DATABASE.md) *(to be created)*
- [API Configuration](./API.md) *(to be created)*
