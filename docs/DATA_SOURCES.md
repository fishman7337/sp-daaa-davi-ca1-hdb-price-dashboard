# Data Sources

## HDB Resale Flat Prices

Raw file:

```text
data/raw/hdb_resale_flat_prices_2017_2025_raw.csv
```

Processed file:

```text
data/processed/hdb_resale_flat_prices_clean.csv
```

This dataset contains Singapore HDB resale flat transactions used for cleaning and baseline visual analysis. The raw file intentionally retains messy labels and formatting issues used in the coursework cleaning task.

## Location-Enriched HDB Resale Dataset

Raw file:

```text
data/raw/location_enriched_hdb_resale_raw.csv
```

Metadata:

```text
data/raw/location_enriched_hdb_resale_metadata.txt
```

Processed file:

```text
data/processed/location_enriched_hdb_resale_clean.csv
```

This dataset expands HDB resale transactions with location features including latitude, longitude, nearest MRT or LRT station, rail line colour, distance to CBD, nearest primary school, and URA planning area.

## Usage Rights

The bundled metadata cites Singapore's National Data Repository and the Singapore Open Data Licence v1.0 for the underlying HDB source. Reuse should follow the original data-provider terms and Singapore Polytechnic assessment rules.

Project code and documentation are licensed under the MIT License. This does not override the original dataset licences or provider terms.

## Traceability

Keep raw files immutable where possible. If processed files are regenerated, compare:

- row counts;
- headers;
- numeric ranges;
- known corrected records;
- Tableau workbook compatibility.

The automated checks in `scripts/validate_data.py` provide the current baseline.
