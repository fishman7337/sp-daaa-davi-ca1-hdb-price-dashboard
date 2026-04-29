# Changelog

## 0.1.0 - 2026-04-29

### Added

- Standard project structure for data, notebooks, dashboards, reports, admin files, scripts, tests, and documentation.
- README with project overview, academic context, setup instructions, validation commands, and artifact map.
- Code of conduct, contribution guide, security policy, licence notice, and environment template.
- Data dictionary, methodology, quality assurance, data sources, and academic integrity documentation.
- Lightweight CSV validation script using the Python standard library.
- Pytest regression tests for project artifacts and processed data.
- GitHub Actions CI with validation, pytest, Bandit security scanning, and pip-audit dependency auditing.
- Standalone Python cleaning script at `scripts/clean_data.py`.

### Changed

- Renamed project artifacts with clearer, descriptive filenames.
- Corrected documentation typos in the location-enriched dataset metadata.
- Updated development and notebook dependency pins after `pip-audit` flagged known pytest and JupyterLab vulnerabilities.
- Replaced the previous no-licence notice with the MIT License.
- Removed notebook-export Python files in favour of maintainable cleaning code.

### Fixed

- Corrected two processed HDB resale records where `floor_area_sqm` had been changed from 67/68 sqm to 200 sqm.
