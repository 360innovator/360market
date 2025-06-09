import os
import json
from collections import defaultdict

try:
    import google.generativeai as genai
except ImportError:  # library may not be installed
    genai = None

LOG_DIR = os.path.dirname(__file__)

# Aggregates numeric metrics across all logs
class LogAggregator:
    def __init__(self):
        self.count = 0
        self.totals = defaultdict(float)
        self.pass_count = 0

    def add_log(self, data: dict):
        self.count += 1
        kpis = data.get("processed_kpis", {})
        for key in ["margin", "delivery_cost", "snap_multiplier"]:
            if isinstance(kpis.get(key), (int, float)):
                self.totals[key] += float(kpis[key])
        if kpis.get("bundle_passed") is True:
            self.pass_count += 1

    def summary(self) -> dict:
        if self.count == 0:
            return {}
        return {
            "total_logs": self.count,
            "avg_margin": self.totals["margin"] / self.count,
            "avg_delivery_cost": self.totals["delivery_cost"] / self.count,
            "avg_snap_multiplier": self.totals["snap_multiplier"] / self.count,
            "pass_rate": self.pass_count / self.count,
        }

def load_logs():
    agg = LogAggregator()
    for fname in os.listdir(LOG_DIR):
        if fname.endswith(".json") and fname != "log_template.json":
            path = os.path.join(LOG_DIR, fname)
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    agg.add_log(data)
                except json.JSONDecodeError:
                    continue
    return agg.summary()

# Optional LLM summarization using Gemini API

def summarize_with_gemini(metrics: dict) -> str:
    if genai is None:
        return "Gemini SDK not installed."

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY environment variable not set."

    genai.configure(api_key=api_key)

    prompt = (
        "Summarize the following KPI metrics from our log data in a brief, user-"
        "friendly report.\n" + json.dumps(metrics, indent=2)
    )
    model = genai.GenerativeModel("gemini-pro")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Optionally log the exception here, e.g. using logging.error(str(e))
        return f"Failed to generate summary from Gemini API: {str(e)}"

def main():
    metrics = load_logs()
    if not metrics:
        print("No valid log data found.")
        return
    print("Aggregated Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    summary = summarize_with_gemini(metrics)
    print("\nLLM Summary:\n")
    print(summary)

if __name__ == "__main__":
    main()
