class ProposalAgent:
    """Formats the finalized scope, estimates, and commercial terms into a professional Markdown proposal."""

    def generate_markdown(self, scope: dict) -> str:
        rows = []
        for d in scope.get("deliverables", []):
            rows.append(
                f"| `{d['id']}` | **{d['title']}** | {d['classification']} | {d['hours_likely']} hrs | ${d['cost_likely']:,} |"
            )
        table_content = "\n".join(rows)

        assumptions = "\n".join(f"- {a}" for a in scope.get("assumptions", []))
        exclusions = "\n".join(f"- {e}" for e in scope.get("exclusions", []))
        questions = "\n".join(f"- {q}" for q in scope.get("open_questions", []))

        return f"""# Commercial Proposal & Statement of Work
**Project:** {scope.get('project_title')}
**Client:** {scope.get('client_name')}
**Estimated Timeline:** {scope.get('timeline')}
**Prepared by:** AI Tech Consultant

---

## 1. Executive Summary
This proposal outlines the technical deliverables, architectural feasibility, and estimated effort to modernize and enhance your digital platform. Deliverables are evaluated against existing native platform capabilities to maximize cost efficiency.

## 2. Deliverables & Investment Breakdown

| ID | Deliverable | Feasibility | Effort | Cost (USD) |
|---|---|---|---|---|
{table_content}
| **TOTAL** | | | **{scope.get('total_hours_likely')} hrs** | **${scope.get('total_cost_likely'):,}** |

## 3. Assumptions
{assumptions}

## 4. Explicit Exclusions
{exclusions}

## 5. Open Clarifications
{questions}

## 6. Acceptance & Approval
Client signature authorizes commencement under standard terms.
- **Client Representative:** _________________________ Date: _________
- **Technical Consultant:** _________________________ Date: _________
"""
