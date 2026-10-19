class ScopeAgent:
    """Assembles deliverables, acceptance criteria, assumptions, and exclusions."""

    def build_scope(self, analysis: dict, feasibility_map: dict, estimate_map: dict) -> dict:
        deliverables = []
        for req in analysis.get("requirements", []):
            req_id = req["id"]
            feas = feasibility_map.get(req_id, {})
            est = estimate_map.get(req_id, {})

            deliverables.append({
                "id": req_id,
                "title": req["title"],
                "description": req["description"],
                "classification": feas.get("classification", "custom_development"),
                "hours_likely": est.get("hours", {}).get("likely", 8),
                "cost_likely": est.get("cost_usd", {}).get("likely", 960),
                "acceptance_criteria": [
                    f"Verified on desktop and mobile viewports.",
                    f"Matches design specifications approved by {analysis.get('client_name', 'Client')}.",
                    "Passes automated regression checks with zero console errors."
                ]
            })

        total_likely_hours = sum(d["hours_likely"] for d in deliverables)
        total_likely_cost = sum(d["cost_likely"] for d in deliverables)

        return {
            "project_title": analysis.get("project_title", "Consulting Engagement"),
            "client_name": analysis.get("client_name", "Valued Client"),
            "timeline": analysis.get("timeline", "4 weeks"),
            "deliverables": deliverables,
            "total_hours_likely": total_likely_hours,
            "total_cost_likely": total_likely_cost,
            "assumptions": [
                "Client provides admin credentials and necessary third-party API keys.",
                "UAT turnaround from client within 3 business days per milestone.",
                "Brilliant Directories standard hosting performance remains constant."
            ],
            "exclusions": analysis.get("exclusions", [
                "Third-party API licensing costs (e.g. Google Maps or Twilio)",
                "Content migration outside of the agreed scope"
            ]),
            "open_questions": analysis.get("open_questions", [])
        }
