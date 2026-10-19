# AI Tech Consultant

Author: Nimmakayala Sowjanya

## Overview

This repository contains three assignment tasks:

1. Knowledge Brain: Python service for collecting product documentation and answering questions using retrieved evidence.
2. Inbox Agent: TypeScript pipeline for classifying emails, drafting replies through the Knowledge Brain, and tracking reviewer feedback.
3. Meeting-to-Scope: Python pipeline for converting meeting transcripts into requirements, feasibility checks, estimates, proposals, and scope comparisons.

## Repository Structure

ai-tech-consultant/
├── task1-knowledge-brain/
│   ├── app/
│   ├── ingestion/
│   ├── retrieval/
│   ├── multimodal/
│   ├── evaluation/
│   └── tests/
├── task2-inbox-agent/
│   ├── src/
│   │   ├── email/
│   │   ├── knowledge-client/
│   │   ├── drafting/
│   │   ├── feedback/
│   │   └── evaluation/
│   └── tests/
├── task3-meeting-to-scope/
│   ├── app/
│   ├── agents/
│   ├── transcripts/
│   ├── scope_diff/
│   ├── evaluation/
│   └── tests/
├── shared-docs/
├── README.md
├── DESIGN.md
├── EVALS.md
└── AI_LOG.md

The document's scope-diff directory is named scope_diff here because Python imports cannot use a hyphen in a package name.

## Requirements

- Python and pip
- Node.js and npm
- Git
- An Anthropic API key for live AI calls

Configuration templates are provided in each task's .env.example file.
Copy these to .env and configure them locally. Never commit .env files or API keys.

## Task 1: Knowledge Brain

From the repository root:

    cd task1-knowledge-brain
    python -m pip install -r requirements.txt
    Copy-Item .env.example .env

Configure .env, then start the service:

    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

API documentation: http://localhost:8000/docs

Use POST /ingest to collect and index documentation before testing grounded answers.

In another terminal, from task1-knowledge-brain:

    python -m pytest tests
    python evaluation/run_evals.py

## Task 2: Inbox Agent

From the repository root:

    cd task2-inbox-agent
    npm install
    Copy-Item .env.example .env
    npm test

Configure ANTHROPIC_API_KEY and KNOWLEDGE_BRAIN_URL in .env.
Start Task 1 before running the live inbox evaluation:

    npm run eval

This task currently runs through scripts; it is not a deployed email service and does not demonstrate delivery to a real mailbox.

## Task 3: Meeting-to-Scope

From the repository root:

    cd task3-meeting-to-scope
    python -m pip install -r requirements.txt
    Copy-Item .env.example .env

Configure .env as needed, then run:

    python evaluation/run_evals.py
    python -m pytest tests/test_scope.py

Start the API:

    python -m uvicorn app.main:app --host 127.0.0.1 --port 8001

API documentation: http://localhost:8001/docs

The current transcript analyst can fall back to sample parsing when a live AI call is unavailable. Sample-mode success does not verify live AI extraction or product feasibility.

## Verification Status

- Task 2: three feedback tracker tests passed locally.
- Task 3: two tests and the sample evaluation passed locally.
- Task 1: verification pending.
- Live AI and cross-task integration: verification pending.
- Deployment: pending.

See DESIGN.md, EVALS.md, and AI_LOG.md for additional notes.
