
# Autoinvoice v0.1

Autoinvoice is a PDF invoice processor that leverages LLMs for data extraction, designed with SOLID principles and clean architecture. This project is a rewrite of "Arte Invoice Processor" and is currently in its foundational phase (v0.1).

## Project Status: v0.1 Foundation

See [docs/v0.1.md](docs/v0.1.md) for detailed requirements, architecture, and flow.

### Epic: PDF Upload, Extraction, and Response ([Issue #3](https://github.com/creep1ng/autoinvoice/issues/3))
- Accept PDF via API (`/upload`)
- Store file (local for v0.1)
- Process PDF (text extraction, OCR if needed)
- Extract invoice data using OpenAI LLM (via LangChain)
- Normalize and return structured data in API response
- Robust error handling and logging
- Unit/integration tests for core components

## Project Structure

```
src/
		api/         # API endpoints (e.g., upload)
		config/      # Settings, logging config
		models/      # Data models
		services/    # Business logic (PDF, extraction)
		utils/       # Utilities (logger, helpers)
docs/           # Documentation, ADRs
examples/       # Example scripts
logs/           # Log output
uploads/        # Uploaded files
```

## API (v0.1)

| Endpoint | Method | Description |
|----------|--------|-------------|
| /upload  | POST   | Upload PDF, returns extracted invoice data |

**Request:**
POST /upload (multipart/form-data, base64-encoded PDF)

**Response:**
```json
{
	"status": "success",
	"data": {
		"invoice_number": "...",
		"date": "...",
		"amount": "..."
		// ...other extracted fields
	}
}
```

## Development

- Python 3.12+
- See `pyproject.toml` for dependencies
- Run tests with `pytest`

## Testing

- Unit tests for extractors, services, and API endpoints
- Use mocks for LLM providers and file storage

## Roadmap

- [ ] Project structure, config, and docs
- [ ] API contract and `/upload` endpoint
- [ ] File storage abstraction
- [ ] PDF processing service
- [ ] OpenAI LLM integration
- [ ] Response normalization
- [ ] Error handling/logging
- [ ] Unit/integration tests

---
For more, see [docs/v0.1.md](docs/v0.1.md) and [Issue #3](https://github.com/creep1ng/autoinvoice/issues/3).
