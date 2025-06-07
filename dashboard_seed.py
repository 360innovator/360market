import json
from typing import Dict


def seed_dashboard(data_file: str) -> Dict:
    """Load seed data for a dashboard from a JSON file."""
    with open(data_file, "r") as f:
        return json.load(f)
