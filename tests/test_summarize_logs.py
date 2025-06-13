import json
import os
import sys
from pathlib import Path
import types

# Ensure repository root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.logger import summarize_logs


def test_load_logs(tmp_path, monkeypatch):
    log1 = {
        "timestamp": "2025-05-31T10:00:00Z",
        "customer_id": "ABC123",
        "bundle_id": "SNAP20",
        "price_pulled": 19.99,
        "processed_kpis": {
            "margin": 0.5,
            "delivery_cost": 3.0,
            "snap_multiplier": 1.2,
            "bundle_passed": True,
        },
    }
    log2 = {
        "timestamp": "2025-06-01T11:00:00Z",
        "customer_id": "XYZ789",
        "bundle_id": "SNAP40",
        "price_pulled": 29.99,
        "processed_kpis": {
            "margin": 0.3,
            "delivery_cost": 4.0,
            "snap_multiplier": 1.4,
            "bundle_passed": False,
        },
    }
    (tmp_path / "a.json").write_text(json.dumps(log1))
    (tmp_path / "b.json").write_text(json.dumps(log2))

    monkeypatch.setattr(summarize_logs, "LOG_DIR", tmp_path)

    metrics = summarize_logs.load_logs()

    assert metrics == {
        "total_logs": 2,
        "avg_margin": (0.5 + 0.3) / 2,
        "avg_delivery_cost": (3.0 + 4.0) / 2,
        "avg_snap_multiplier": (1.2 + 1.4) / 2,
        "pass_rate": 1 / 2,
    }


def test_summarize_with_gemini_no_api_key(monkeypatch):
    class DummyGenAI:
        def configure(self, api_key):
            self.api_key = api_key
        def GenerativeModel(self, name):
            class DummyModel:
                def generate_content(self, prompt):
                    return types.SimpleNamespace(text="dummy")
            return DummyModel()

    monkeypatch.setattr(summarize_logs, "genai", DummyGenAI())
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    result = summarize_logs.summarize_with_gemini({"total_logs": 1})
    assert result == "GEMINI_API_KEY environment variable not set."


def test_summarize_with_gemini_success(monkeypatch):
    class DummyModel:
        def __init__(self):
            self.prompt = None
        def generate_content(self, prompt):
            self.prompt = prompt
            return types.SimpleNamespace(text="summary")

    class DummyGenAI:
        def __init__(self, model):
            self.model = model
            self.api_key = None
        def configure(self, api_key):
            self.api_key = api_key
        def GenerativeModel(self, name):
            return self.model

    dummy_model = DummyModel()
    monkeypatch.setattr(summarize_logs, "genai", DummyGenAI(dummy_model))
    monkeypatch.setenv("GEMINI_API_KEY", "token")

    result = summarize_logs.summarize_with_gemini({"metric": 1})

    assert result == "summary"
    assert dummy_model.prompt is not None

