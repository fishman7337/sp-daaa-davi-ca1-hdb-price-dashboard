# Data Dictionary

## Processed HDB Resale Dataset

Path: `data/processed/hdb_resale_flat_prices_clean.csv`

| Column | Description |
| --- | --- |
| `month` | Transaction month in `YYYY-MM` format. |
| `town` | HDB town, normalized to title case. |
| `flat_type` | Flat type, normalized to title case. |
| `block` | HDB block number. |
| `street_name` | Street name, normalized to title case and expanded where appropriate. |
| `storey_range` | Storey band in normalized `n to n` form. |
| `floor_area_sqm` | Flat floor area in square metres. |
| `flat_model` | HDB flat model, normalized to a consistent display form. |
| `lease_commence_date` | Year the flat lease commenced. |
| `remaining_lease` | Remaining lease in normalized text form. |
| `resale_price` | Transaction price in Singapore dollars. |
| `remaining_lease_months` | Remaining lease converted into total months. |

## Processed Location-Enriched Dataset

Path: `data/processed/location_enriched_hdb_resale_clean.csv`

| Column | Description |
| --- | --- |
| `month` | Transaction month as a date. |
| `town` | HDB town, normalized to title case. |
| `blk_no` | HDB block number. |
| `road_name` | Road name, normalized to title case. |
| `building` | Building name where available; `Nil` where absent. |
| `postal` | Postal code. |
| `resale_price` | Transaction price in Singapore dollars. |
| `storey_range` | Storey band in normalized `n to n` form. |
| `flat_type` | Flat type, normalized to title case. |
| `flat_model` | HDB flat model. |
| `lease_commence_date` | Lease commencement date. |
| `remaining_lease_years` | Whole years of remaining lease at transaction time. |
| `remaining_lease_months` | Remaining lease months after whole years. |
| `floor_area_sqm` | Flat floor area in square metres. |
| `floor_area_sqft` | Flat floor area in square feet. |
| `price_per_sqft` | Resale price divided by square-foot floor area. |
| `planning_area_ura` | URA planning area. |
| `region_ura` | URA region. |
| `x` | SVY21 x coordinate. |
| `y` | SVY21 y coordinate. |
| `latitude` | Latitude coordinate. |
| `longitude` | Longitude coordinate. |
| `closest_mrt_station` | Closest MRT or LRT station. |
| `distance_to_mrt_meters` | Displacement to closest MRT or LRT station in metres. |
| `transport_type` | Closest rail transport type, such as MRT or LRT. |
| `line_color` | Rail line colour for the closest station. |
| `distance_to_cbd` | Displacement to the CBD proxy point in metres. |
| `closest_pri_school` | Closest primary school. |
| `distance_to_pri_school_meters` | Displacement to closest primary school in metres. |

## Raw Data Notes

- `data/raw/hdb_resale_flat_prices_2017_2025_raw.csv` contains inconsistent labels and formatting that are intentionally retained for traceability.
- `data/raw/location_enriched_hdb_resale_raw.csv` includes a leading unnamed index column from export.
- `data/raw/location_enriched_hdb_resale_metadata.txt` describes source provenance and original field meanings.

