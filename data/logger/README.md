# Data Logger

This folder stores operational logs used by the analytics pipeline. All files must be valid JSON.

## Subfolders

- `raw_data/` – daily operational CSVs such as location metrics and orders
- `trigger_logs/` – snapshots of grant eligibility or investor signals
- `quant_search/` – raw responses from external funding or accelerator searches

See the [system diagram](../docs/system_diagram.md) for how these logs flow through the platform.

### Example log entry
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "customerOrder": {
    "bundleType": "SNAP Bundle",
    "items": []
  },
  "groceryPrices": []
}
```
