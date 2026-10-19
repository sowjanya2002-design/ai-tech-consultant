# Design Notes

## Task 1: Knowledge Brain

The ingestion layer collects help-center articles and detects changed content.
The retrieval layer chunks and indexes articles using Chroma.
The API retrieves evidence before asking the model to generate an answer.
Unsupported questions are intended to be escalated rather than answered without evidence.

Screenshot interpretation is implemented separately in the multimodal directory. Its end-to-end integration still needs verification.

## Task 2: Inbox Agent

The email pipeline classifies incoming messages, queries Task 1, and drafts a reply using the returned knowledge.

Replies must not promise refunds, discounts, or service-level commitments.
Drafts use the Support Team sign-off.
High-risk messages require human review.

The feedback tracker counts consecutive approvals without edits per category. Editing or rejecting a draft resets the relevant streak. Twenty consecutive unedited approvals establish eligibility for an autonomy trial, not proof that automatic sending is safe.

## Task 3: Meeting-to-Scope

The pipeline separates transcript analysis, feasibility checking, estimation, scope construction, and proposal writing.

The scope comparison identifies additions and removals and calculates effort and cost changes.

The scope_diff directory uses an underscore to support Python imports.

## Limitations

Sample parsing must be distinguished from live AI analysis.
Unavailable knowledge must not be represented as verified product capability.
Estimates are planning outputs, not binding commercial commitments.
Proposals require human review before being sent to clients.

The current local tests do not establish production readiness.
