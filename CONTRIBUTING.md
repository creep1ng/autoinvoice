# Contributing to Autoinvoice

Thank you for your interest in contributing! Please follow these conventions to ensure a smooth workflow and maintain code quality.

## Branching Strategy
- **Branch names:** `{issue-number}-{category}/{short-title}`
  - Example: `42-feature/pdf-upload`
  - `category`: `feature`, `bugfix`, `chore`, `docs`, `test`, `research`, `epic` (match `.github/ISSUE_TEMPLATE`)
- **Base branch:** Always branch from `main` unless otherwise specified.

## Commit Messages
- **Format:**
  ```
  {category}({scope}): {short summary}

  [optional body]

  Closes #{issue-number}
  ```
  - Example:
    ```
    feature(api): add PDF upload endpoint

    Implements FastAPI /upload endpoint for PDF processing.

    Closes #42
    ```
- **Category:** Use the same as branch category.
- **Scope:** Affected area (e.g., `api`, `settings`, `logging`).
- **Summary:** Short, imperative mood.

## Pull Requests
- Use the PR template in `.github/pull_request_template.md`.
- Reference related issues (e.g., `Closes #42`).
- Clearly describe what was changed and why.

## Code Quality
- **Lint/format:** Run `ruff` before pushing.
- **Tests:** Add/modify tests in `tests/` for all features and bugfixes. Run `pytest` and ensure all tests pass.
- **Docs:** Update or add docs in `docs/` as needed. Add/modify ADRs for architectural changes.

## Environment & Tooling
- Use the devcontainer and `docker-compose` for local development.
- Use `uv` for dependency management.

## Review & Merge
- At least one approval required before merging.
- Use "Squash and merge" to keep history clean.

## Other Considerations
- Follow the commit message format for automated changelogs.
- Do not commit secrets or sensitive data.
- Check `docs/adr/` for architectural decisions before major changes.

---
See [AGENTS.md](AGENTS.md) for AI agent conventions and project-specific automation guidelines.
