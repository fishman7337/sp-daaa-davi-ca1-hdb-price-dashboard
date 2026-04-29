from scripts.validate_data import EXPECTED_FILES, PROJECT_ROOT, validate_project


def test_required_files_are_documented_and_present():
    missing = [path.relative_to(PROJECT_ROOT) for path in EXPECTED_FILES if not path.exists()]

    assert missing == []


def test_processed_datasets_pass_validation():
    assert validate_project() == []
