import json
from pathlib import Path
import sys
import os
import pytest

# Ensure repository root is on the Python path when running with `pytest`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.logger.validate_log import validate_iso8601, validate_file


def test_validate_iso8601_valid():
    assert validate_iso8601("2025-05-31T10:00:00Z")


def test_validate_iso8601_invalid():
    assert not validate_iso8601("2025/05/31 10:00")


def test_validate_file_valid(tmp_path: Path):
    log = {
        "timestamp": "2025-05-31T10:00:00Z",
        "customer_id": "ABC123",
        "bundle_id": "SNAP20",
        "price_pulled": 19.99,
        "processed_kpis": {
            "margin": 0.28,
            "delivery_cost": 3.5,
            "snap_multiplier": 1.25,
            "bundle_passed": True,
        },
    }
    p = tmp_path / "log.json"
    p.write_text(json.dumps(log))
    assert validate_file(p) == "PASS"


def test_validate_file_missing_field(tmp_path: Path):
    log = {
        "timestamp": "2025-05-31T10:00:00Z",
        # missing customer_id
        "bundle_id": "SNAP20",
        "price_pulled": 19.99,
        "processed_kpis": {
            "margin": 0.28,
            "delivery_cost": 3.5,
            "snap_multiplier": 1.25,
            "bundle_passed": True,
        },
    }
    p = tmp_path / "log.json"
    p.write_text(json.dumps(log))
    result = validate_file(p)
    assert "Missing field: customer_id" == result
