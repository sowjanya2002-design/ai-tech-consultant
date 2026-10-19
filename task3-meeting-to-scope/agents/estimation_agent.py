import os

class EstimationAgent:
    """Produces 3-point estimates (low, likely, high) and costs based on feasibility."""

    def __init__(self):
        self.hourly_rate = float(os.getenv("DEFAULT_HOURLY_RATE", "120"))

    def estimate(self, requirement: dict, feasibility: dict) -> dict:
        classification = feasibility.get("classification", "custom_development")

        if classification == "existing_configuration":
            tasks = [
                {"task": "Admin configuration & testing", "low": 2, "likely": 3, "high": 5},
                {"task": "Documentation & client handover", "low": 1, "likely": 1.5, "high": 2}
            ]
        elif classification == "existing_feature_limitation":
            tasks = [
                {"task": "Add-on configuration", "low": 3, "likely": 4, "high": 6},
                {"task": "Custom CSS styling & responsive tweaks", "low": 4, "likely": 6, "high": 10},
                {"task": "QA across devices", "low": 2, "likely": 3, "high": 5}
            ]
        else:  # custom_development
            tasks = [
                {"task": "Architecture & API integration", "low": 6, "likely": 10, "high": 16},
                {"task": "Frontend UI component implementation", "low": 8, "likely": 14, "high": 22},
                {"task": "Integration testing & edge cases", "low": 4, "likely": 6, "high": 10}
            ]

        total_low = sum(t["low"] for t in tasks)
        total_likely = sum(t["likely"] for t in tasks)
        total_high = sum(t["high"] for t in tasks)

        return {
            "requirement_id": requirement["id"],
            "tasks": tasks,
            "hours": {
                "low": total_low,
                "likely": total_likely,
                "high": total_high
            },
            "cost_usd": {
                "low": round(total_low * self.hourly_rate, 2),
                "likely": round(total_likely * self.hourly_rate, 2),
                "high": round(total_high * self.hourly_rate, 2)
            },
            "hourly_rate": self.hourly_rate
        }
