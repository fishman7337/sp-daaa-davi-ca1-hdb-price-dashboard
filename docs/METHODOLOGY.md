# Methodology

## Data Preparation

The coursework uses two related HDB resale datasets:

- a raw resale transaction dataset for cleaning practice and baseline analysis;
- a location-enriched dataset with geospatial, transport, CBD distance, and primary school proximity attributes.

The notebooks in `notebooks/` document the original cleaning process. The standalone cleaning implementation is in `scripts/clean_data.py`. The processed CSV files in `data/processed/` are the canonical cleaned outputs used for analysis and dashboarding.

## Cleaning Themes

The cleaning work addresses:

- inconsistent town naming, including abbreviations such as `AMK`;
- inconsistent flat type labels such as `3-ROOM`, `3 ROOM`, and title-case variants;
- street-name abbreviations such as `AVE`;
- malformed storey ranges such as `01@03` and `04---06`;
- inconsistent flat model spellings;
- inconsistent remaining-lease strings;
- unwanted index columns in raw exported data;
- casing normalization for presentation-ready fields.

## Data Quality Corrections

During repository touch-up, two clear errors were corrected in `data/processed/hdb_resale_flat_prices_clean.csv`:

| Month | Block | Street | Field | Previous | Corrected |
| --- | --- | --- | --- | --- | --- |
| 2017-01 | 233 | Ang Mo Kio Avenue 3 | `floor_area_sqm` | 200.0 | 67.0 |
| 2017-01 | 465 | Ang Mo Kio Avenue 10 | `floor_area_sqm` | 200.0 | 68.0 |

Both corrections match the raw HDB file and the location-enriched raw dataset where comparable records exist.

## Validation Approach

The validation script checks that:

- required files exist;
- processed files have the expected schemas;
- row counts match documented baselines;
- key numeric columns are parseable and within defensible ranges;
- categorical fields use normalized labels;
- the processed location-enriched file does not retain the raw unnamed index column;
- the two corrected HDB records retain their expected floor areas.

## Reproducibility Notes

The notebooks are retained as the main cleaning narrative. The automated tests are not a replacement for the notebooks; they are guardrails to detect accidental file corruption, schema drift, or reintroduced data-cleaning mistakes.
