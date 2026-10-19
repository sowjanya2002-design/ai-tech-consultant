import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.estimation_agent import EstimationAgent
from agents.scope_agent import ScopeAgent
from scope_diff.differ import ScopeDiffer

def test_estimation_calculation():
    estimator = EstimationAgent()
    req = {"id": "REQ-001", "title": "Test Filter"}
    feasibility = {"classification": "existing_configuration"}
    res = estimator.estimate(req, feasibility)

    assert res["hours"]["likely"] > 0
    assert res["cost_usd"]["likely"] == res["hours"]["likely"] * estimator.hourly_rate

def test_scope_diff_add_and_remove():
    differ = ScopeDiffer()
    base_scope = {
        "deliverables": [{"title": "Search Filter", "hours_likely": 10, "cost_likely": 1200}],
        "total_hours_likely": 10,
        "total_cost_likely": 1200,
        "timeline": "3 weeks"
    }
    revised_scope = {
        "deliverables": [
            {"title": "Search Filter", "hours_likely": 10, "cost_likely": 1200},
            {"title": "Google Map View", "hours_likely": 20, "cost_likely": 2400}
        ],
        "total_hours_likely": 30,
        "total_cost_likely": 3600,
        "timeline": "5 weeks"
    }

    diff = differ.diff(base_scope, revised_scope)
    assert len(diff["added_features"]) == 1
    assert diff["added_features"][0]["title"] == "Google Map View"
    assert diff["summary"]["hours_delta"] == 20
    assert diff["summary"]["cost_delta"] == 2400
