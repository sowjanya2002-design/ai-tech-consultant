class ScopeDiffer:
    """Compares follow-up meeting scopes (Meeting C) against baseline scopes (Meeting A)."""

    def diff(self, base_scope: dict, revised_scope: dict) -> dict:
        base_reqs = {d["title"].lower(): d for d in base_scope.get("deliverables", [])}
        revised_reqs = {d["title"].lower(): d for d in revised_scope.get("deliverables", [])}

        added = []
        removed = []
        unchanged = []

        for title, d in revised_reqs.items():
            if title not in base_reqs:
                added.append(d)
            else:
                unchanged.append(d)

        for title, d in base_reqs.items():
            if title not in revised_reqs:
                removed.append(d)

        base_hours = base_scope.get("total_hours_likely", 0)
        revised_hours = revised_scope.get("total_hours_likely", 0)
        hours_delta = revised_hours - base_hours

        base_cost = base_scope.get("total_cost_likely", 0)
        revised_cost = revised_scope.get("total_cost_likely", 0)
        cost_delta = revised_cost - base_cost

        return {
            "comparison": "Meeting A (Baseline) vs Meeting C (Follow-Up)",
            "added_features": added,
            "removed_features": removed,
            "retained_features": unchanged,
            "summary": {
                "base_hours": base_hours,
                "revised_hours": revised_hours,
                "hours_delta": hours_delta,
                "base_cost": base_cost,
                "revised_cost": revised_cost,
                "cost_delta": cost_delta,
                "timeline_change": f"{base_scope.get('timeline')} -> {revised_scope.get('timeline')}"
            }
        }
