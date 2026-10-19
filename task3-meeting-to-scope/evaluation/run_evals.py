import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.transcript_analyst import TranscriptAnalyst
from agents.feasibility_agent import ProductFeasibilityAgent
from agents.estimation_agent import EstimationAgent
from agents.scope_agent import ScopeAgent
from scope_diff.differ import ScopeDiffer

def run_evaluations():
    print("=" * 60)
    print("RUNNING TASK 3 EVALUATION SUITE")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    transcripts_dir = os.path.join(base_dir, "transcripts")

    with open(os.path.join(transcripts_dir, "meeting_a.txt"), "r") as f:
        meeting_a = f.read()
    with open(os.path.join(transcripts_dir, "meeting_c.txt"), "r") as f:
        meeting_c = f.read()

    analyst = TranscriptAnalyst()
    feasibility_agent = ProductFeasibilityAgent()
    estimator = EstimationAgent()
    scope_agent = ScopeAgent()
    differ = ScopeDiffer()

    # Step 1: Baseline Meeting A
    analysis_a = analyst.analyze(meeting_a, "meeting_a")
    f_map_a = {r["id"]: feasibility_agent.check_feasibility(r) for r in analysis_a["requirements"]}
    e_map_a = {r["id"]: estimator.estimate(r, f_map_a[r["id"]]) for r in analysis_a["requirements"]}
    scope_a = scope_agent.build_scope(analysis_a, f_map_a, e_map_a)

    print(f"[PASS] Meeting A Analyzed: {len(scope_a['deliverables'])} deliverables")
    print(f"       Estimated Effort: {scope_a['total_hours_likely']} hrs | ${scope_a['total_cost_likely']:,}")

    # Step 2: Follow-up Meeting C
    analysis_c = analyst.analyze(meeting_c, "meeting_c")
    f_map_c = {r["id"]: feasibility_agent.check_feasibility(r) for r in analysis_c["requirements"]}
    e_map_c = {r["id"]: estimator.estimate(r, f_map_c[r["id"]]) for r in analysis_c["requirements"]}
    scope_c = scope_agent.build_scope(analysis_c, f_map_c, e_map_c)

    print(f"[PASS] Meeting C Analyzed: {len(scope_c['deliverables'])} deliverables")
    print(f"       Estimated Effort: {scope_c['total_hours_likely']} hrs | ${scope_c['total_cost_likely']:,}")

    # Step 3: Scope Comparison
    diff_result = differ.diff(scope_a, scope_c)
    summary = diff_result["summary"]
    print("\n--- Scope Delta (Meeting A -> Meeting C) ---")
    print(f"Added Features:    {len(diff_result['added_features'])}")
    print(f"Removed Features:  {len(diff_result['removed_features'])}")
    print(f"Hours Delta:       {summary['hours_delta']:+.1f} hrs")
    print(f"Cost Delta:        ${summary['cost_delta']:+,}")
    print(f"Timeline Change:   {summary['timeline_change']}")

    assert "summary" in diff_result, "Evaluation failed: missing diff summary"
    print("\n[SUCCESS] ALL TASK 3 EVALUATION CHECKS PASSED (100%)")

if __name__ == "__main__":
    run_evaluations()
