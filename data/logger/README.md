# Data Logger

This folder stores raw data captured from the application. Each log file should be in JSON format with a timestamped filename.

Example log file structure:
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "customerOrder": {
    "bundleType": "SNAP Bundle",
    "items": [/* ... */]
  },
  "groceryPrices": [/* ... */]
}
```
