# Schemas

This directory stores JSON and YAML schema definitions for data ingestion and validation. Schemas ensure that incoming data conforms to expected formats before being processed by Gemini, DeepSeek, and related LLM workflows.

## Contents
- `data_audit_schema.json` – baseline schema describing required fields for order and KPI logs.
- Additional schemas for APIs and CSV transforms can be added here.

Use these schemas with your ingestion tools to validate data before running analytics or feeding it into language models.
