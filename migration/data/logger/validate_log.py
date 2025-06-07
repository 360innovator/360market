import json
import os
import datetime

REQUIRED_FIELDS = {
    "timestamp": str,
    "customer_id": str,
    "bundle_id": str,
    "price_pulled": float,
    "processed_kpis": dict
}

KPI_FIELDS = {
    "margin": float,
    "delivery_cost": float,
    "snap_multiplier": float,
    "bundle_passed": bool
}

def validate_iso8601(ts):
    try:
        datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

def validate_file(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        for field, ftype in REQUIRED_FIELDS.items():
            if field not in data:
                return f"Missing field: {field}"
            if not isinstance(data[field], ftype) and not (field == "price_pulled" and isinstance(data[field], (float, int))):
                return f"Invalid type for {field}, expected {ftype.__name__}"

        if not validate_iso8601(data["timestamp"]):
            return "Invalid ISO 8601 timestamp format"

        kpis = data["processed_kpis"]
        for kfield, ktype in KPI_FIELDS.items():
            if kfield not in kpis:
                return f"Missing KPI field: {kfield}"
            if not isinstance(kpis[kfield], ktype) and not (ktype == float and isinstance(kpis[kfield], int)):
                return f"Invalid type for KPI.{kfield}, expected {ktype.__name__}"

        return "PASS"

    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    log_dir = os.path.dirname(__file__)
    for filename in os.listdir(log_dir):
        if filename.endswith(".json"):
            path = os.path.join(log_dir, filename)
            result = validate_file(path)
            print(f"{filename}: {result}")

if __name__ == "__main__":
    main()
