# Quality Assurance

## Automated Checks

Run the full local check set with:

```bash
python scripts/validate_data.py
python -m pytest
python -m bandit -r scripts
python -m py_compile scripts/*.py
pip-audit -r requirements-dev.txt
pip-audit -r requirements-cleaning.txt
pip-audit -r requirements-notebooks.txt
```

## What The Tests Cover

- Required project files exist in their expected folders.
- Processed CSV schemas match the documented headers.
- Processed CSV row counts match the current baselines.
- Numeric columns parse correctly and stay within expected bounds.
- Normalized fields do not reintroduce obvious raw formatting issues.
- Known corrected records keep their corrected values.

## Manual Checks

Before submitting or publishing an updated version:

- open the Tableau workbook and confirm charts load;
- confirm the written report and slides open correctly;
- confirm the academic integrity declaration is present;
- skim the README after any file rename or folder movement;
- keep source and dataset attribution visible.

## Known Limitations

- The tests validate the current processed outputs; they do not rerun every notebook cell.
- Keep notebook outputs light before version control so reviews focus on the cleaning logic.
- Some large HDB terrace and maisonette floor areas are legitimate outliers and should not be removed solely because they are large.
