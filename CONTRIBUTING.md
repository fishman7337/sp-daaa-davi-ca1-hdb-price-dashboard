# Contributing

## Scope

This is an academic coursework repository, so changes should preserve the original assessment context while improving clarity, reproducibility, and correctness.

## Recommended Workflow

1. Create or activate a Python environment.
2. Install development dependencies with `python -m pip install -r requirements-dev.txt`.
3. Make focused changes.
4. Run `python scripts/validate_data.py`.
5. Run `python -m pytest`.
6. Run `python -m bandit -r scripts` for Python security scanning.
7. Update documentation when paths, data assumptions, or outputs change.

## Documentation Standards

- Keep dataset paths accurate.
- Explain why a cleaning rule exists, not only what it does.
- Document known limitations and assumptions.
- Use clear filenames with lowercase words separated by underscores.
- Avoid committing generated caches, local environments, credentials, or temporary exports.

## Data Change Standards

When changing a processed CSV:

- preserve headers unless the documentation and Tableau workbook are also updated;
- record the reason for the change in documentation or commit notes;
- run the validation script and pytest suite;
- verify that Tableau dashboards still open and point to the expected data.

## Academic Integrity

Do not add unattributed analysis, copied text, generated content, or external code. If external assistance is used, document it according to module and school requirements.
