# Singapore HDB Resale Price Visual Analytics

This repository contains the cleaned datasets, Tableau workbook, cleaning notebooks, report, and presentation for a Singapore Polytechnic data visualisation coursework project on Singapore HDB resale flat prices.

## Academic Context

- Institution: Singapore Polytechnic, School of Computing
- Diploma: Applied AI and Analytics
- Module: Data Visualisation (ST1502)
- Assessment: CA1
- Academic year: AY25/26, Year 2 Semester 2
- Student: Goh Kun Ming
- Lecturer: Senior Lecturer Peter Lee Wai Tong

## Project Overview

The project analyses Singapore HDB resale flat transactions, with a focus on price patterns across flat type, town, floor area, remaining lease, and location-related features. The main deliverables are:

- a Tableau packaged workbook for dashboard exploration;
- cleaned CSV datasets for reproducible analysis;
- Jupyter notebooks documenting the data cleaning process;
- a written report and slide deck for the CA1 submission;
- automated validation tests and CI checks for future maintenance.

## Repository Structure

```text
.
|-- admin/
|   `-- academic_integrity_declaration.docx
|-- dashboards/
|   `-- tableau/
|       `-- hdb_resale_price_visual_analytics.twbx
|-- data/
|   |-- processed/
|   |   |-- hdb_resale_flat_prices_clean.csv
|   |   `-- location_enriched_hdb_resale_clean.csv
|   `-- raw/
|       |-- hdb_resale_flat_prices_2017_2025_raw.csv
|       |-- location_enriched_hdb_resale_metadata.txt
|       `-- location_enriched_hdb_resale_raw.csv
|-- docs/
|   |-- ACADEMIC_INTEGRITY.md
|   |-- DATA_DICTIONARY.md
|   |-- DATA_SOURCES.md
|   |-- METHODOLOGY.md
|   |-- PROJECT_CONTEXT.md
|   `-- QUALITY_ASSURANCE.md
|-- notebooks/
|   |-- 01_hdb_resale_data_cleaning.ipynb
|   `-- 02_location_enriched_data_cleaning.ipynb
|-- reports/
|   |-- slides/
|   |   |-- hdb_resale_price_presentation.pdf
|   |   `-- hdb_resale_price_presentation.pptx
|   `-- written/
|       `-- hdb_resale_price_report.docx
|-- scripts/
|   |-- clean_data.py
|   `-- validate_data.py
|-- tests/
|   `-- test_data_validation.py
|-- .env.example
|-- .github/workflows/ci.yml
|-- CHANGELOG.md
|-- CODE_OF_CONDUCT.md
|-- CONTRIBUTING.md
|-- LICENSE.md
|-- SECURITY.md
|-- pyproject.toml
|-- requirements-cleaning.txt
|-- requirements-dev.txt
`-- requirements-notebooks.txt
```

## Data Assets

The repository uses two dataset families:

- `data/raw/hdb_resale_flat_prices_2017_2025_raw.csv`: raw HDB resale transaction data with intentionally inconsistent labels and formatting issues from the coursework cleaning task.
- `data/raw/location_enriched_hdb_resale_raw.csv`: location-enriched resale dataset containing coordinates, nearby MRT station, CBD distance, and primary school proximity fields.
- `data/processed/hdb_resale_flat_prices_clean.csv`: cleaned version of the HDB resale transaction dataset.
- `data/processed/location_enriched_hdb_resale_clean.csv`: cleaned version of the location-enriched dataset.

See [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for field definitions, [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for source notes, and [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for the cleaning approach.

## Quick Start

Create a local environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the validation checks:

```bash
python scripts/validate_data.py
python -m pytest
```

Run the security checks used by CI:

```bash
python -m bandit -r scripts
pip-audit -r requirements-dev.txt
pip-audit -r requirements-cleaning.txt
pip-audit -r requirements-notebooks.txt
```

## Working With the Notebooks

Install the notebook dependencies when you need to rerun or extend the cleaning work:

```bash
python -m pip install -r requirements-notebooks.txt
jupyter lab
```

The notebooks are kept output-light so the repository stays easier to review. Keep heavy generated outputs out of version control where possible.

## Cleaning Script

The plain Python cleaning code is in:

```text
scripts/clean_data.py
```

Install the cleaning dependency and regenerate the processed CSVs with:

```bash
python -m pip install -r requirements-cleaning.txt
python scripts/clean_data.py
```

## Tableau Workbook

Open the dashboard at:

```text
dashboards/tableau/hdb_resale_price_visual_analytics.twbx
```

The workbook is a packaged Tableau workbook, so it should remain portable with its embedded assets.

## Quality And CI

The project includes a GitHub Actions workflow at `.github/workflows/ci.yml` that runs:

- CSV schema and data-quality validation;
- pytest regression tests;
- Bandit security scanning for Python files;
- pip-audit dependency vulnerability checks for development, cleaning, and notebook dependencies.

The validation script is intentionally lightweight and uses the Python standard library so CI can check the datasets without requiring pandas.

## Environment Variables

Copy `.env.example` to `.env` for local overrides. The current project does not require secrets. Do not commit `.env`.

## Academic Integrity

The academic integrity declaration is stored in `admin/academic_integrity_declaration.docx`. See [docs/ACADEMIC_INTEGRITY.md](docs/ACADEMIC_INTEGRITY.md) for repository maintenance expectations.

## Data Rights

Dataset usage rights belong to the original data providers. The location-enriched dataset metadata cites the Singapore Open Data Licence v1.0 for the underlying HDB source.

## License

Project code and documentation are released under the MIT License. Dataset rights remain with the original data providers and are subject to their published terms.
