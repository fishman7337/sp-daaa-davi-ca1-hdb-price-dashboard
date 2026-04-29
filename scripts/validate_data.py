"""Validate the processed datasets and required project artifacts."""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]

HDB_CLEAN_PATH = PROJECT_ROOT / "data" / "processed" / "hdb_resale_flat_prices_clean.csv"
LOCATION_CLEAN_PATH = (
    PROJECT_ROOT / "data" / "processed" / "location_enriched_hdb_resale_clean.csv"
)

EXPECTED_FILES = (
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "CODE_OF_CONDUCT.md",
    PROJECT_ROOT / "CONTRIBUTING.md",
    PROJECT_ROOT / "SECURITY.md",
    PROJECT_ROOT / ".env.example",
    PROJECT_ROOT / "CHANGELOG.md",
    PROJECT_ROOT / "docs" / "ACADEMIC_INTEGRITY.md",
    PROJECT_ROOT / "docs" / "DATA_DICTIONARY.md",
    PROJECT_ROOT / "docs" / "DATA_SOURCES.md",
    PROJECT_ROOT / "docs" / "METHODOLOGY.md",
    PROJECT_ROOT / "dashboards" / "tableau" / "hdb_resale_price_visual_analytics.twbx",
    PROJECT_ROOT / "scripts" / "clean_data.py",
    PROJECT_ROOT / "reports" / "written" / "hdb_resale_price_report.docx",
    PROJECT_ROOT / "reports" / "slides" / "hdb_resale_price_presentation.pptx",
    PROJECT_ROOT / "admin" / "academic_integrity_declaration.docx",
    HDB_CLEAN_PATH,
    LOCATION_CLEAN_PATH,
)

HDB_SCHEMA = [
    "month",
    "town",
    "flat_type",
    "block",
    "street_name",
    "storey_range",
    "floor_area_sqm",
    "flat_model",
    "lease_commence_date",
    "remaining_lease",
    "resale_price",
    "remaining_lease_months",
]

LOCATION_SCHEMA = [
    "month",
    "town",
    "blk_no",
    "road_name",
    "building",
    "postal",
    "resale_price",
    "storey_range",
    "flat_type",
    "flat_model",
    "lease_commence_date",
    "remaining_lease_years",
    "remaining_lease_months",
    "floor_area_sqm",
    "floor_area_sqft",
    "price_per_sqft",
    "planning_area_ura",
    "region_ura",
    "x",
    "y",
    "latitude",
    "longitude",
    "closest_mrt_station",
    "distance_to_mrt_meters",
    "transport_type",
    "line_color",
    "distance_to_cbd",
    "closest_pri_school",
    "distance_to_pri_school_meters",
]

EXPECTED_ROW_COUNTS = {
    HDB_CLEAN_PATH: 202_461,
    LOCATION_CLEAN_PATH: 216_695,
}

VALID_FLAT_TYPES = {
    "1 Room",
    "2 Room",
    "3 Room",
    "4 Room",
    "5 Room",
    "Executive",
    "Multi-Generation",
}

MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STOREY_RANGE_RE = re.compile(r"^\d{1,2} to \d{1,2}$")


@dataclass(frozen=True)
class NumericRule:
    column: str
    minimum: float
    maximum: float


@dataclass(frozen=True)
class DatasetSpec:
    path: Path
    schema: list[str]
    expected_rows: int
    row_validator: Callable[[dict[str, str], int, list[str]], None]


def as_float(row: dict[str, str], column: str, line_number: int, errors: list[str]) -> float | None:
    value = row.get(column, "")
    try:
        return float(value)
    except ValueError:
        errors.append(f"Line {line_number}: {column} is not numeric: {value!r}")
        return None


def validate_numeric_rules(
    row: dict[str, str],
    line_number: int,
    rules: tuple[NumericRule, ...],
    errors: list[str],
) -> None:
    for rule in rules:
        value = as_float(row, rule.column, line_number, errors)
        if value is None:
            continue
        if not rule.minimum <= value <= rule.maximum:
            errors.append(
                f"Line {line_number}: {rule.column}={value} outside "
                f"{rule.minimum}..{rule.maximum}"
            )


def validate_common_fields(
    row: dict[str, str],
    line_number: int,
    errors: list[str],
    month_pattern: re.Pattern[str],
) -> None:
    if row["flat_type"] not in VALID_FLAT_TYPES:
        errors.append(f"Line {line_number}: unexpected flat_type {row['flat_type']!r}")

    if not month_pattern.match(row["month"]):
        errors.append(f"Line {line_number}: unexpected month format {row['month']!r}")

    if not STOREY_RANGE_RE.match(row["storey_range"]):
        errors.append(
            f"Line {line_number}: storey_range is not normalized: {row['storey_range']!r}"
        )


def validate_hdb_row(row: dict[str, str], line_number: int, errors: list[str]) -> None:
    validate_common_fields(row, line_number, errors, MONTH_RE)
    validate_numeric_rules(
        row,
        line_number,
        (
            NumericRule("floor_area_sqm", 31.0, 400.0),
            NumericRule("resale_price", 100_000.0, 1_700_000.0),
            NumericRule("remaining_lease_months", 0.0, 1_200.0),
        ),
        errors,
    )

    if any(token in row["street_name"] for token in ("@", "---")):
        errors.append(f"Line {line_number}: street_name still contains raw noise")


def validate_location_row(row: dict[str, str], line_number: int, errors: list[str]) -> None:
    validate_common_fields(row, line_number, errors, DATE_RE)
    validate_numeric_rules(
        row,
        line_number,
        (
            NumericRule("floor_area_sqm", 31.0, 400.0),
            NumericRule("floor_area_sqft", 300.0, 4_500.0),
            NumericRule("price_per_sqft", 100.0, 2_000.0),
            NumericRule("resale_price", 100_000.0, 1_800_000.0),
            NumericRule("remaining_lease_years", 0.0, 99.0),
            NumericRule("remaining_lease_months", 0.0, 11.0),
            NumericRule("latitude", 1.20, 1.50),
            NumericRule("longitude", 103.60, 104.10),
            NumericRule("distance_to_mrt_meters", 0.0, 5_000.0),
            NumericRule("distance_to_cbd", 0.0, 25_000.0),
            NumericRule("distance_to_pri_school_meters", 0.0, 5_000.0),
        ),
        errors,
    )

    if row["transport_type"] not in {"MRT", "LRT"}:
        errors.append(
            f"Line {line_number}: unexpected transport_type {row['transport_type']!r}"
        )


def validate_required_files() -> list[str]:
    return [f"Missing required file: {path.relative_to(PROJECT_ROOT)}" for path in EXPECTED_FILES if not path.exists()]


def validate_dataset(spec: DatasetSpec) -> list[str]:
    errors: list[str] = []
    corrected_hdb_records = {
        ("2017-01", "233", "Ang Mo Kio Avenue 3", "295000.0"): "67.0",
        ("2017-01", "465", "Ang Mo Kio Avenue 10", "265000.0"): "68.0",
    }
    seen_corrected_hdb_records: set[tuple[str, str, str, str]] = set()

    with spec.path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != spec.schema:
            errors.append(
                f"{spec.path.relative_to(PROJECT_ROOT)} schema mismatch: "
                f"expected {spec.schema}, found {reader.fieldnames}"
            )
            return errors

        if any(not field or field.lower().startswith("unnamed") for field in reader.fieldnames):
            errors.append(f"{spec.path.relative_to(PROJECT_ROOT)} contains an unnamed column")

        row_count = 0
        for line_number, row in enumerate(reader, start=2):
            row_count += 1
            spec.row_validator(row, line_number, errors)

            if spec.path == HDB_CLEAN_PATH:
                key = (
                    row["month"],
                    row["block"],
                    row["street_name"],
                    row["resale_price"],
                )
                expected_area = corrected_hdb_records.get(key)
                if expected_area is not None:
                    seen_corrected_hdb_records.add(key)
                    if row["floor_area_sqm"] != expected_area:
                        errors.append(
                            f"Line {line_number}: corrected HDB record {key} has "
                            f"floor_area_sqm={row['floor_area_sqm']}, expected {expected_area}"
                        )

        if row_count != spec.expected_rows:
            errors.append(
                f"{spec.path.relative_to(PROJECT_ROOT)} row count mismatch: "
                f"expected {spec.expected_rows}, found {row_count}"
            )

    if spec.path == HDB_CLEAN_PATH:
        missing = set(corrected_hdb_records) - seen_corrected_hdb_records
        for key in sorted(missing):
            errors.append(f"Corrected HDB record not found: {key}")

    return errors


def validate_project() -> list[str]:
    errors = validate_required_files()
    specs = (
        DatasetSpec(HDB_CLEAN_PATH, HDB_SCHEMA, EXPECTED_ROW_COUNTS[HDB_CLEAN_PATH], validate_hdb_row),
        DatasetSpec(
            LOCATION_CLEAN_PATH,
            LOCATION_SCHEMA,
            EXPECTED_ROW_COUNTS[LOCATION_CLEAN_PATH],
            validate_location_row,
        ),
    )
    for spec in specs:
        if spec.path.exists():
            errors.extend(validate_dataset(spec))
    return errors


def main() -> int:
    errors = validate_project()
    if errors:
        print("Data validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Data validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
