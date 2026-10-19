from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys

# Ensure parent path resolution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.transcript_analyst import TranscriptAnalyst
from agents.feasibility_agent import ProductFeasibilityAgent
from agents.estimation_agent import EstimationAgent
from agents.scope_agent import ScopeAgent
from agents.proposal_agent import ProposalAgent
from scope_diff.differ import ScopeDiffer

app = FastAPI(title="Meeting-to-Scope API", version="1.0.0")

class TranscriptInput(BaseModel):
    transcript: str
    meeting_id: str = "meeting_01"

class ScopeDiffInput(BaseModel):
    base_transcript: str
    revised_transcript: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "task3-meeting-to-scope"}

@app.post("/generate-scope")
def generate_scope(data: TranscriptInput):
    analyst = TranscriptAnalyst()
    feasibility_agent = ProductFeasibilityAgent()
    estimator = EstimationAgent()
    scope_agent = ScopeAgent()
    proposal_agent = ProposalAgent()

    analysis = analyst.analyze(data.transcript, data.meeting_id)

    feasibility_map = {}
    estimate_map = {}
    for req in analysis.get("requirements", []):
        feas = feasibility_agent.check_feasibility(req)
        feasibility_map[req["id"]] = feas
        est = estimator.estimate(req, feas)
        estimate_map[req["id"]] = est

    scope = scope_agent.build_scope(analysis, feasibility_map, estimate_map)
    proposal_md = proposal_agent.generate_markdown(scope)

    return {
        "analysis": analysis,
        "scope": scope,
        "proposal_markdown": proposal_md
    }

@app.post("/diff-scope")
def diff_scope(data: ScopeDiffInput):
    analyst = TranscriptAnalyst()
    feasibility_agent = ProductFeasibilityAgent()
    estimator = EstimationAgent()
    scope_agent = ScopeAgent()
    differ = ScopeDiffer()

    def process(transcript, m_id):
        an = analyst.analyze(transcript, m_id)
        f_map = {r["id"]: feasibility_agent.check_feasibility(r) for r in an.get("requirements", [])}
        e_map = {r["id"]: estimator.estimate(r, f_map[r["id"]]) for r in an.get("requirements", [])}
        return scope_agent.build_scope(an, f_map, e_map)

    base = process(data.base_transcript, "base")
    revised = process(data.revised_transcript, "revised")
    return differ.diff(base, revised)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
