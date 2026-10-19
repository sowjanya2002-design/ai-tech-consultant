# AI Technical Consultant Suite

An end-to-end multi-agent AI system designed for technical consulting, featuring automated knowledge retrieval, intelligent customer support triage, and automated project scoping with contract diffing.

---

## 🌐 Live Deployment & Links

| Resource | URL |
| :--- | :--- |
| **Live Web Application** | [https://ai-tech-consultant-0mci.onrender.com/](https://ai-tech-consultant-0mci.onrender.com/) |
| **Interactive API Docs** | [https://ai-tech-consultant-0mci.onrender.com/docs](https://ai-tech-consultant-0mci.onrender.com/docs) |
| **GitHub Repository** | [https://github.com/sowjanya2002-design/ai-tech-consultant](https://github.com/sowjanya2002-design/ai-tech-consultant) |
| **Deployment Platform** | Render Cloud Web Service |
| **Production Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

---

## 🚀 Architecture Overview

This project consists of three core tasks integrated into a unified web application:

### Task 1: Knowledge Brain (`task1-knowledge-brain`)
- **Web Crawler & Sitemap Sync**: Automatically crawls sitemaps (e.g., Brilliant Directories documentation), tracks SHA-256 hashes to detect content updates, and stores content in SQLite.
- **Vector Search Engine**: Powered by ChromaDB with 1000-character chunks and 200-character overlap for high-precision semantic retrieval.
- **Strict Evidence-Grounded Q&A**: Uses Claude 3.5 Sonnet to generate answers strictly from cited sources. Returns citations, status, and confidence scores. Automatically logs unanswered queries into an escalation queue.
- **Multimodal Support**: Claude Vision integration for analyzing technical screenshots and visual error reports.

### Task 2: AI Inbox Agent (`task2-inbox-agent`)
- **Triage & Classification**: Categorizes incoming customer inquiries into 8 distinct categories (`how_to`, `troubleshooting`, `project_request`, `refund_cancellation`, `complaint`, `quote_request`, `follow_up`, `other`).
- **Risk Assessment**: Automatically flags queries with `low`, `medium`, or `high` risk. High-risk requests (e.g., complaints or refund demands) are held for human review.
- **Knowledge-Grounded Drafting**: Queries the Task 1 Knowledge Brain API (`POST /ask`) to produce compliant, professional responses signed off as "Support Team".
- **Autonomy Progression Tracker**: Tracks agent reliability. After 20 consecutive unedited human approvals, the system automatically unlocks autonomous dispatch for that category.

### Task 3: Meeting-to-Scope Agent (`task3-meeting-to-scope`)
- **Multi-Agent Pipeline**:
  1. *Transcript Analyst*: Extracts client requirements, budget constraints, timeline expectations, and tech stack requirements from meeting transcripts.
  2. *Feasibility Agent*: Cross-checks requirements against the knowledge base for technical viability.
  3. *Estimation Agent*: Computes development hours and pricing per deliverable based on complexity.
  4. *Scope Agent*: Drafts a clear technical scope with explicit deliverables, milestones, assumptions, and out-of-scope boundaries.
  5. *Proposal Agent*: Produces client-ready executive proposals.
- **Scope Differ**: Compares initial project scopes against follow-up meeting transcripts to compute deltas in hours, costs, timeline changes, added deliverables, and removed features.

---

## 🛠️ Project Structure

```text
ai-tech-consultant/
├── task1-knowledge-brain/
│   ├── app/                 # FastAPI server & unified web suite
│   ├── ingestion/           # Async sitemap crawler & SHA-256 change detection
│   ├── retrieval/           # ChromaDB chunking, indexing, and vector search
│   ├── multimodal/          # Claude Vision image analysis
│   ├── evaluation/          # Golden evaluation set & benchmarking runner
│   └── tests/               # Pytest test suite
│
├── task2-inbox-agent/
│   ├── src/
│   │   ├── email/           # Email schemas & test dataset
│   │   ├── knowledge-client/# Client connector to Task 1 Knowledge Brain API
│   │   ├── drafting/        # Classification & response drafting pipeline
│   │   ├── feedback/        # 20-streak autonomy progression tracker
│   │   └── evaluation/      # Dataset evaluation runner
│   └── tests/               # Vitest test suite
│
├── task3-meeting-to-scope/
│   ├── app/                 # Scope generation & diffing API
│   ├── agents/              # 5-agent scoping & feasibility pipeline
│   ├── transcripts/         # Meeting transcripts (Meeting A, B, and C)
│   ├── scope_diff/          # Automated scope change detection engine
│   ├── evaluation/          # Scope evaluation script
│   └── tests/               # Pytest test suite
│
├── shared-docs/             # Architectural specifications
├── README.md                # System documentation
├── DESIGN.md                # System design & architecture decisions
├── EVALS.md                 # Evaluation benchmarks & metrics
├── AI_LOG.md                # AI engineering journey & audit log
└── .gitignore               # Ignored environments & dependencies
