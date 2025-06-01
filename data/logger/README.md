# Data Logger

This folder stores all logging data used by the KPI pipeline. Files are organized into three subfolders:

- `raw_data/` – daily metrics such as orders, locations and finance CSVs
- `trigger_logs/` – grant or investor triggers captured as CSV snapshots
- `quant_search/` – JSON responses from funding program searches

Each log added to the root of `data/logger` must be a JSON file using the structure below.

## Log File Format

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "customer_id": "CUSTOMER_ID_HERE",
  "bundle_id": "BUNDLE_CODE",
  "price_pulled": 0.0,
  "processed_kpis": {
    "margin": 0.0,
    "delivery_cost": 0.0,
    "snap_multiplier": 0.0,
    "bundle_passed": false
  }
}
```

Example:

```json
{
  "timestamp": "2025-05-31T10:00:00Z",
  "customer_id": "ABC123",
  "bundle_id": "SNAP20",
  "price_pulled": 19.99,
  "processed_kpis": {
    "margin": 0.28,
    "delivery_cost": 3.50,
    "snap_multiplier": 1.25,
    "bundle_passed": true
  }
}
```
