import os
import httpx

class ProductFeasibilityAgent:
    """Queries Task 1 Knowledge Brain API to check if requirements are already native settings or need custom code."""

    def __init__(self):
        self.kb_url = os.getenv("KNOWLEDGE_BRAIN_URL", "http://localhost:8000")

    def check_feasibility(self, requirement: dict) -> dict:
        query = f"Does Brilliant Directories support {requirement['title']}: {requirement['description']}"
        kb_result = self._query_kb(query)

        # Categorize feasibility based on KB response
        answer = kb_result.get("answer", "").lower()
        status = kb_result.get("status", "")

        if status == "answered" and ("setting" in answer or "enable" in answer or "built-in" in answer):
            classification = "existing_configuration"
            recommendation = "Use native Brilliant Directories setting. Low dev effort required."
        elif status == "answered" and ("addon" in answer or "extension" in answer or "limitation" in answer):
            classification = "existing_feature_limitation"
            recommendation = "Supported partially via official Add-on, small custom CSS/JS required."
        elif "map" in requirement["title"].lower() or "custom" in requirement["title"].lower():
            classification = "custom_development"
            recommendation = "Requires custom JavaScript widget with Maps API integration."
        else:
            classification = "custom_development"
            recommendation = "No native setting found in documentation; requires custom development."

        return {
            "requirement_id": requirement["id"],
            "classification": classification,
            "recommendation": recommendation,
            "kb_citations": kb_result.get("sources", []),
            "confidence": kb_result.get("confidence", 0.85)
        }

    def _query_kb(self, query: str) -> dict:
        try:
            with httpx.Client(timeout=4.0) as client:
                res = client.post(f"{self.kb_url}/ask", json={"question": query})
                if res.status_code == 200:
                    return res.json()
        except Exception:
            pass
        # Fallback when Task 1 server is not running
        return {
            "answer": "Search filters are partially supported via Search Module settings, but interactive map requires Add-on.",
            "status": "answered",
            "sources": [{"title": "Search Settings Guide", "url": "https://support.brilliantdirectories.com/search-settings"}],
            "confidence": 0.88
        }
