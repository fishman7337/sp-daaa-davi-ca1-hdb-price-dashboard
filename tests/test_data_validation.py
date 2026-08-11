from scripts.clean_data import (
    clean_street,
    standardise_flat_model,
    standardise_location_flat_model,
    standardise_location_street,
    standardise_mrt_station,
)
from scripts.validate_data import EXPECTED_FILES, PROJECT_ROOT, validate_project


def test_required_files_are_documented_and_present():
    missing = [path.relative_to(PROJECT_ROOT) for path in EXPECTED_FILES if not path.exists()]

    assert missing == []


def test_processed_datasets_pass_validation():
    assert validate_project() == []


def test_cleaning_helpers_reproduce_canonical_labels():
    assert clean_street("LOR 8 TP") == "Lorong 8 Toa Payoh"
    assert clean_street("NEW UPP CHANGI RD") == "New Upper Changi Road"
    assert standardise_flat_model("DBSS") == "DBSS"
    assert standardise_flat_model("2-room") == "2-room"
    assert standardise_location_flat_model("DBSS") == "Dbss"
    assert standardise_location_street("TG PAGAR PLAZA") == "Tanjong Pagar Plaza"
    assert standardise_mrt_station("HARBOURFRONT") == "HarbourFront"
