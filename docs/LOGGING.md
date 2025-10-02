# Logging Foundation - AutoInvoice

This document describes the logging implementation for the AutoInvoice project using Python's built-in `logging` module.

## Overview

The logging foundation provides:

- **Structured Logging**: Support for both human-readable text and JSON formats
- **Environment-Based Configuration**: Different log levels and formats for dev/prod
- **Request Tracking**: Automatic request ID generation for API calls
- **File Rotation**: Automatic log file rotation to prevent disk space issues
- **Colored Console Output**: Easy-to-read colored logs during development
- **Context-Rich Logging**: Add custom fields to any log entry

## Architecture

```
src/
├── config/
│   ├── __init__.py           # Config module exports
│   ├── settings.py           # Pydantic settings with env support
│   └── logging_config.py     # Logging setup and formatters
├── utils/
│   ├── __init__.py           # Utils module exports
│   └── logger.py             # Logger utility and mixin
└── api/
    └── middleware.py         # FastAPI request logging middleware
```

## Quick Start

### 1. Environment Configuration

Create a `.env` file in the project root (use `.env.example` as template):

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env`:

```env
# Logging Configuration
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=text             # text or json
LOG_FILE=logs/autoinvoice.log  # Optional: file path for logging
```

### 2. Initialize Logging

At your application entry point (e.g., `main.py` or FastAPI app):

```python
from src.config import setup_logging, settings

# Initialize logging (do this once at startup)
setup_logging(settings)
```

### 3. Use Logging in Your Code

```python
from src.utils import get_logger

logger = get_logger(__name__)

# Basic logging
logger.info("Processing started")
logger.error("Something went wrong")

# Logging with context
logger.info(
    "Invoice processed",
    extra={
        "invoice_id": "INV-001",
        "customer_id": "CUST-123",
        "amount": 1500.50,
    }
)

# Exception logging
try:
    process_invoice()
except Exception as e:
    logger.error("Failed to process invoice", exc_info=True)
```

## Features

### 1. Text Format (Development)

Best for development with colored console output:

```bash
LOG_FORMAT=text
```

Output:
```
2025-01-15 10:30:45 | INFO     | src.services.invoice:process:42 | Processing invoice
2025-01-15 10:30:46 | ERROR    | src.services.invoice:process:45 | Invoice validation failed
```

### 2. JSON Format (Production)

Best for production with log aggregation tools (ELK, Splunk, etc.):

```bash
LOG_FORMAT=json
```

Output:
```json
{
  "timestamp": "2025-01-15T10:30:45.123456Z",
  "level": "INFO",
  "logger": "src.services.invoice",
  "message": "Processing invoice",
  "module": "invoice",
  "function": "process",
  "line": 42,
  "invoice_id": "INV-001",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. File Logging with Rotation

Enable file logging:

```env
LOG_FILE=logs/autoinvoice.log
LOG_FILE_MAX_BYTES=10485760  # 10MB
LOG_FILE_BACKUP_COUNT=5       # Keep 5 backup files
```

This creates:
- `logs/autoinvoice.log` (current)
- `logs/autoinvoice.log.1` (previous)
- `logs/autoinvoice.log.2` (older)
- ... up to 5 backups

### 4. Request Tracking in FastAPI

Add the middleware to your FastAPI app:

```python
from fastapi import FastAPI
from src.api.middleware import RequestLoggingMiddleware

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)
```

Every request gets:
- Automatic request ID generation
- Request/response logging
- Timing information
- Request ID in response headers

Example log output:
```
2025-01-15 10:30:45 | INFO | POST /api/invoices
2025-01-15 10:30:46 | INFO | POST /api/invoices - 201 | duration_ms=145.23 | request_id=550e8400...
```

### 5. LoggerMixin for Classes

Use the `LoggerMixin` for automatic logger setup in classes:

```python
from src.utils.logger import LoggerMixin

class InvoiceProcessor(LoggerMixin):
    def process(self, invoice_id: str):
        # self.logger is automatically available
        self.logger.info(
            "Processing invoice",
            extra={"invoice_id": invoice_id}
        )
        
        try:
            # Your processing logic
            pass
        except Exception as e:
            self.logger.error(
                "Processing failed",
                extra={"invoice_id": invoice_id},
                exc_info=True
            )
            raise
```

## Configuration Reference

See [SETTINGS.md](./SETTINGS.md) for complete settings documentation.

### Log Levels

Set via `LOG_LEVEL` environment variable:

- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages (default)
- `WARNING`: Something unexpected happened
- `ERROR`: A serious problem occurred
- `CRITICAL`: A very serious error

### Settings Class

All logging configuration is in `src/config/settings.py` (see [SETTINGS.md](./SETTINGS.md) for details):

```python
from src.config import settings

# Access settings
print(settings.log_level)      # "INFO"
print(settings.log_format)     # "text"
print(settings.database_url)   # For other settings

# Or use the getter function
from src.config import get_settings
settings = get_settings()  # Cached singleton instance
```

## Best Practices

### 1. Always Use get_logger(__name__)

```python
from src.utils import get_logger

logger = get_logger(__name__)  # ✅ Good
logger = logging.getLogger()   # ❌ Avoid
```

### 2. Add Context with extra

```python
# ✅ Good - structured context
logger.info(
    "Invoice created",
    extra={
        "invoice_id": invoice_id,
        "customer_id": customer_id,
        "amount": amount,
    }
)

# ❌ Avoid - context in message
logger.info(f"Invoice {invoice_id} created for {customer_id}")
```

### 3. Log Exceptions Properly

```python
try:
    process_invoice()
except Exception as e:
    # ✅ Good - includes stack trace
    logger.error("Failed to process", exc_info=True)
    
    # ❌ Avoid - no stack trace
    logger.error(f"Failed: {str(e)}")
```

### 4. Use Appropriate Log Levels

```python
logger.debug("Entering function with params: x=1, y=2")  # Detailed debug info
logger.info("Invoice processed successfully")            # Normal operations
logger.warning("Rate limit approaching")                 # Warnings
logger.error("Database connection failed")               # Errors
logger.critical("System out of memory")                  # Critical failures
```

### 5. Don't Log Sensitive Data

```python
# ❌ Bad - logs sensitive data
logger.info(f"User password: {password}")

# ✅ Good - redact sensitive data
logger.info(f"User authenticated: {username}")
```

## Examples

See the `examples/` directory for complete working examples:

- **`examples/logging_examples.py`**: Basic usage, context logging, class usage
- **`examples/fastapi_example.py`**: FastAPI integration with middleware

Run examples:

```bash
# Basic examples
python examples/logging_examples.py

# FastAPI example
python examples/fastapi_example.py
# Then visit http://localhost:8000
```

## Testing Different Formats

### Test Text Format

```bash
export LOG_FORMAT=text
export LOG_LEVEL=DEBUG
python examples/logging_examples.py
```

### Test JSON Format

```bash
export LOG_FORMAT=json
export LOG_LEVEL=INFO
python examples/logging_examples.py
```

### Test with File Logging

```bash
export LOG_FILE=logs/test.log
python examples/logging_examples.py
cat logs/test.log
```

## Integration with Other Services

### Log Aggregation (ELK Stack)

Use JSON format and ship logs to Elasticsearch:

```env
LOG_FORMAT=json
LOG_FILE=logs/autoinvoice.log
```

Configure Filebeat to read `logs/autoinvoice.log` and send to Elasticsearch.

### Cloud Logging (AWS CloudWatch, GCP Cloud Logging)

These services can parse JSON logs automatically:

```env
LOG_FORMAT=json
```

### Docker Logging

Logs to stdout are captured by Docker:

```env
LOG_FORMAT=json
# Don't set LOG_FILE - let Docker handle it
```

## Troubleshooting

### No logs appearing

1. Check log level: `LOG_LEVEL=DEBUG`
2. Verify logging is initialized: `setup_logging(settings)`
3. Check if logger is configured: `logging.getLogger().handlers`

### File not being created

1. Verify directory exists: `mkdir -p logs`
2. Check permissions: `ls -la logs/`
3. Check absolute path: `settings.logs_dir`

### Too many logs in production

1. Increase log level: `LOG_LEVEL=WARNING`
2. Filter third-party libraries (already done in `logging_config.py`)

### Performance issues

1. Use JSON format for production (more efficient)
2. Reduce log level to `WARNING` or `ERROR`
3. Use asynchronous logging for high-traffic applications

## Next Steps

1. **Add monitoring**: Integrate with Prometheus for metrics
2. **Add alerting**: Set up alerts for ERROR/CRITICAL logs
3. **Add log retention**: Configure log cleanup policies
4. **Add log analysis**: Use tools like Grafana Loki for log analysis
5. **Add distributed tracing**: Integrate with OpenTelemetry

## References

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
