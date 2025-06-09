# Data Logger

This directory stores operational logs used by the pricing and KPI system. Every log must be a JSON file that conforms to the schema below. Files that fail validation will be rejected by downstream modules. The validation script requires **Python 3.8+**.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | Time the order was logged (UTC). |
| `customer_id` | String | Unique customer identifier. |
| `bundle_id` | String | Reference to the bundle purchased. |
| `price_pulled` | Float | Final price from the pricing API. |
| `processed_kpis` | Object | Metrics generated after processing. |

### `processed_kpis` Fields

| Field | Type | Description |
|-------|------|-------------|
| `margin` | Float | Net margin after all costs. |
| `delivery_cost` | Float | Cost to deliver the bundle. |
| `snap_multiplier` | Float | Multiplier applied for EBT bundles. |
| `bundle_passed` | Boolean | Whether the bundle cleared margin rules. |

## Example Log

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

A starter template is provided in `log_template.json`. An additional example
file, `example_log.json`, is included so you can immediately test the
validation script.

## Validation

Run `validate_log.py` with **Python 3.8 or later** to verify all log files:

```bash
python validate_log.py
```

The script checks each JSON file in this directory for required fields and correct types. It prints `PASS` for valid logs or an error message describing any issues.
