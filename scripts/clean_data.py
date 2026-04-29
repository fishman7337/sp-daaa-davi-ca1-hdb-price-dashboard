"""Clean the raw HDB resale datasets used for the ST1502 CA1 project.

This script is intentionally separate from the notebooks. It keeps the cleaning
logic in plain Python so the transformations can be reviewed, rerun, and tested
without notebook display cells.

Examples:
    python scripts/clean_data.py
    python scripts/clean_data.py --dataset hdb
    python scripts/clean_data.py --output-dir data/processed_candidate
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

HDB_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "hdb_resale_flat_prices_2017_2025_raw.csv"
LOCATION_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "location_enriched_hdb_resale_raw.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

HDB_OUTPUT_NAME = "hdb_resale_flat_prices_clean.csv"
LOCATION_OUTPUT_NAME = "location_enriched_hdb_resale_clean.csv"

HDB_COLUMNS = [
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

LOCATION_COLUMNS = [
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

TOWN_FIXES = {
    "ANG MO KIOO": "ANG MO KIO",
    "AMK": "ANG MO KIO",
    "CCK": "CHOA CHU KANG",
    "SENG-KANG": "SENGKANG",
    "SENGKANG NORTH": "SENGKANG",
    "TAMPINES PARK": "TAMPINES",
}

FLAT_MODEL_FIXES = {
    "NG": "New Generation",
    "IMPROVEDV1": "Improved",
    "MODEL -A": "Model A",
    "MODEL A_B": "Model A",
    "NEW-GENERATION": "New Generation",
    "NEW GENERATION": "New Generation",
    "PREMIUM MAISONETTE": "Premium Maisonette",
    "IMPROVED-MAISONETTE": "Improved-Maisonette",
    "3GEN": "3Gen",
    "MULTI GENERATION": "Multi Generation",
    "PREMIUM APARTMENT LOFT": "Premium Apartment Loft",
    "TYPE S2": "Type S2",
    "TYPE S1": "Type S1",
    "2-ROOM": "2-room",
    "ADJOINED FLAT": "Adjoined flat",
    "MODEL A-MAISONETTE": "Model A-Maisonette",
    "MODEL A2": "Model A2",
    "DBSS": "DBSS",
}

STOREY_FIXES = {
    "01@@03": "01 TO 03",
    "07@@09": "07 TO 09",
    "10--12": "10 TO 12",
    "07 --- 09": "07 TO 09",
    "01 ---03": "01 TO 03",
    "13 - 15": "13 TO 15",
    "10-DEC": "10 TO 12",
    "01----03": "01 TO 03",
    "04---06": "04 TO 06",
    "01@03": "01 TO 03",
    "10@12": "10 TO 12",
    "04 TO 06-10": "04 TO 06",
    "13 TO 15-9": "13 TO 15",
    "01 -- 03": "01 TO 03",
    "22 -- 24": "22 TO 24",
    "22 --- 24": "22 TO 24",
    "4-JUN": "04 TO 06",
    "07 -- 09": "07 TO 09",
    "19 -- 21": "19 TO 21",
    "04 -- 06": "04 TO 06",
}

STREET_TOKEN_FIXES = {
    "AMK": "ANG MO KIO",
    "JLN": "JALAN",
    "BT": "BUKIT",
    "TG": "TANJONG",
    "AVE": "AVENUE",
    "ST": "STREET",
    "RD": "ROAD",
    "DR": "DRIVE",
    "CRES": "CRESCENT",
    "CL": "CLOSE",
    "PL": "PLACE",
    "TER": "TERRACE",
    "PK": "PARK",
    "HTS": "HEIGHTS",
    "CTRL": "CENTRAL",
    "NTH": "NORTH",
    "STH": "SOUTH",
}


def normalise_colname(value: str) -> str:
    """Convert a raw column name to lowercase snake_case."""
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def title_clean(value: object) -> str | None:
    """Return a whitespace-normalised title-case string."""
    if pd.isna(value):
        return None
    text = re.sub(r"\s+", " ", str(value).strip())
    return text.title() if text else None


def standardise_town(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.upper()
        .replace(TOWN_FIXES)
        .str.title()
    )
    return cleaned


def standardise_flat_type(value: object) -> str | None:
    if pd.isna(value):
        return None

    text = str(value).strip().upper()
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    direct_fixes = {
        "1 ROOM": "1 Room",
        "2 ROOMS": "2 Room",
        "2 ROOM": "2 Room",
        "3 ROOMS": "3 Room",
        "3 ROOMS": "3 Room",
        "3 ROOMATES": "3 Room",
        "3 RM": "3 Room",
        "3 ROOM": "3 Room",
        "4 ROOMSS": "4 Room",
        "4 ROOMS": "4 Room",
        "44 ROOM": "4 Room",
        "4 ROOM": "4 Room",
        "5 RM": "5 Room",
        "5 ROOM": "5 Room",
        "EXECUTIVE PART 1": "Executive",
        "EXECUTIVE": "Executive",
        "MULTI GENERATION": "Multi-Generation",
    }
    if text in direct_fixes:
        return direct_fixes[text]

    room_match = re.fullmatch(r"([1-5])\s*(?:ROOM|ROOMS|RM)", text)
    if room_match:
        return f"{room_match.group(1)} Room"

    return text.title()


def clean_block(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).upper().strip()
    text = re.sub(r"(^|\W)BLK($|\W)", " ", text)
    text = text.replace("_BLK", " ").replace("BLK_", " ")
    text = re.sub(r"[^A-Z0-9]", "", text)
    text = re.sub(r"^0+(\d.*)$", r"\1", text)
    return text or None


def clean_street(value: object) -> str | None:
    if pd.isna(value):
        return None

    text = str(value).upper().strip()
    text = re.sub(r"[^A-Z0-9\s'\-\.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    if not text:
        return None

    tokens: list[str] = []
    for token in text.split():
        replacement = STREET_TOKEN_FIXES.get(token, token)
        tokens.extend(replacement.split())

    deduped: list[str] = []
    for token in tokens:
        if not deduped or deduped[-1] != token:
            deduped.append(token)

    return " ".join(token if token.isdigit() else token.title() for token in deduped)


def standardise_storey_range(value: object) -> str | None:
    if pd.isna(value):
        return None

    text = str(value).strip().upper()
    text = STOREY_FIXES.get(text, text)
    text = text.replace("@", " TO ")
    text = re.sub(r"\s*[-]{1,}\s*", " TO ", text)
    text = re.sub(r"\s+", " ", text)

    numbers = re.findall(r"\d{1,2}", text)
    if len(numbers) >= 2:
        return f"{int(numbers[0])} to {int(numbers[1])}"

    return text.title() if text else None


def standardise_flat_model(value: object) -> str | None:
    if pd.isna(value):
        return None

    text = re.sub(r"\s+", " ", str(value).strip())
    if not text:
        return None

    key = text.upper()
    if key in FLAT_MODEL_FIXES:
        return FLAT_MODEL_FIXES[key]

    text = text.replace("_", " ")
    text = re.sub(r"-{2,}", "-", text)
    text = re.sub(r"\s+", " ", text).strip()
    key = text.upper()
    if key in FLAT_MODEL_FIXES:
        return FLAT_MODEL_FIXES[key]

    special = {
        "DBSS": "DBSS",
        "3GEN": "3Gen",
        "2-ROOM": "2-room",
    }
    if key in special:
        return special[key]

    return text.title()


def parse_remaining_lease(value: object) -> tuple[int, int] | None:
    if pd.isna(value):
        return None

    text = str(value).strip().lower()
    text = re.sub(r"\bys?\b|\byr?s?\b", " years ", text)
    text = re.sub(r"\bmos?\b|\bmth?s?\b|\bmnths?\b", " months ", text)
    text = text.replace("/", " ").replace("-", " ").replace("_", " ")
    text = re.sub(r"[,\(\)]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    years_match = re.search(r"(\d+)\s*years?", text)
    months_match = re.search(r"(\d+)\s*months?", text)
    if not years_match and not months_match:
        numbers = [int(number) for number in re.findall(r"\d+", text)]
        if not numbers:
            return None
        years = numbers[0]
        months = numbers[1] if len(numbers) > 1 else 0
    else:
        years = int(years_match.group(1)) if years_match else 0
        months = int(months_match.group(1)) if months_match else 0

    years += months // 12
    months = months % 12
    return max(years, 0), max(months, 0)


def format_remaining_lease(value: tuple[int, int] | None) -> str | None:
    if value is None:
        return None
    years, months = value
    return f"{years} years {months} months"


def clean_resale_price(value: object) -> float | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    text = re.sub(r"[\$,]", "", text)
    text = text.replace("-", "")
    text = text.replace(" ", "")
    return pd.to_numeric(text, errors="coerce")


def clean_hdb_resale(raw_path: Path = HDB_RAW_PATH) -> pd.DataFrame:
    """Clean the provided HDB resale transaction dataset."""
    df = pd.read_csv(raw_path, low_memory=False)
    df.columns = [normalise_colname(column) for column in df.columns]
    df = df.drop_duplicates().reset_index(drop=True)

    df["month"] = (
        df["month"]
        .astype(str)
        .str.strip()
        .replace({"2024-02, woodlands": "2024-02", "2023-0113": "2023-01"})
    )
    df["town"] = standardise_town(df["town"])
    df["flat_type"] = df["flat_type"].map(standardise_flat_type)
    df["block"] = df["block"].map(clean_block)
    df["street_name"] = df["street_name"].map(clean_street)
    df["storey_range"] = df["storey_range"].map(standardise_storey_range)
    df["floor_area_sqm"] = pd.to_numeric(df["floor_area_sqm"], errors="coerce")
    df["flat_model"] = df["flat_model"].map(standardise_flat_model)
    df["lease_commence_date"] = pd.to_numeric(
        df["lease_commence_date"], errors="coerce"
    ).astype("Int64")

    parsed_lease = df["remaining_lease"].map(parse_remaining_lease)
    df["remaining_lease"] = parsed_lease.map(format_remaining_lease)
    df["remaining_lease_months"] = parsed_lease.map(
        lambda value: pd.NA if value is None else value[0] * 12 + value[1]
    ).astype("Int64")

    df["resale_price"] = df["resale_price"].map(clean_resale_price).astype(float)
    df.loc[df["resale_price"] > 1_700_000, "resale_price"] = 1_500_000.0

    return df.loc[:, HDB_COLUMNS]


def clean_location_enriched(raw_path: Path = LOCATION_RAW_PATH) -> pd.DataFrame:
    """Clean the location-enriched HDB resale dataset."""
    df = pd.read_csv(raw_path, index_col=False, low_memory=False)
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]
    df.columns = [normalise_colname(column) for column in df.columns]
    df = df.drop_duplicates().reset_index(drop=True)

    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["town"] = standardise_town(df["town"])
    df["blk_no"] = df["blk_no"].map(clean_block)
    df["road_name"] = df["road_name"].map(clean_street)
    df["building"] = df["building"].map(title_clean)
    df["storey_range"] = df["storey_range"].map(standardise_storey_range)
    df["flat_type"] = df["flat_type"].map(standardise_flat_type)
    df["flat_model"] = df["flat_model"].map(standardise_flat_model)
    df["lease_commence_date"] = pd.to_datetime(
        df["lease_commence_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")
    df["planning_area_ura"] = df["planning_area_ura"].map(title_clean)
    df["region_ura"] = df["region_ura"].map(title_clean)
    df["closest_mrt_station"] = df["closest_mrt_station"].map(title_clean)
    df["transport_type"] = df["transport_type"].astype(str).str.strip().str.upper()
    df["line_color"] = df["line_color"].map(title_clean)
    df["closest_pri_school"] = df["closest_pri_school"].map(title_clean)

    numeric_columns = [
        "postal",
        "resale_price",
        "remaining_lease_years",
        "remaining_lease_months",
        "floor_area_sqm",
        "floor_area_sqft",
        "price_per_sqft",
        "x",
        "y",
        "latitude",
        "longitude",
        "distance_to_mrt_meters",
        "distance_to_cbd",
        "distance_to_pri_school_meters",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df.loc[:, LOCATION_COLUMNS]


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        choices=("all", "hdb", "location"),
        default="all",
        help="Dataset to clean. Defaults to all.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where cleaned CSV files should be written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir

    if args.dataset in {"all", "hdb"}:
        hdb = clean_hdb_resale()
        output_path = output_dir / HDB_OUTPUT_NAME
        write_csv(hdb, output_path)
        print(f"Wrote {len(hdb):,} rows to {output_path}")

    if args.dataset in {"all", "location"}:
        location = clean_location_enriched()
        output_path = output_dir / LOCATION_OUTPUT_NAME
        write_csv(location, output_path)
        print(f"Wrote {len(location):,} rows to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
