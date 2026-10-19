# Evaluation Results

## Task 1

Status: not yet verified.

Commands:

    python -m pytest tests
    python evaluation/run_evals.py

The API must be running and documentation indexed before evaluating grounded answers.

## Task 2

Command:

    npm test

Observed result: one test file passed, three tests passed.

Verified cases:

- An unedited approval increments the feedback streak.
- Editing a draft resets the streak.
- Twenty consecutive unedited approvals establish autonomy eligibility.

Live classification, grounding, human-review routing, rejection handling, and actual email delivery are not established by these three tests.

## Task 3

Commands:

    python evaluation/run_evals.py
    python -m pytest tests/test_scope.py

Observed result: the sample evaluation completed successfully and two tests passed.

Observed sample output:

| Measurement | Meeting A | Meeting C |
| --- | --- | --- |
| Deliverables | 2 | 3 |
| Estimated hours | 9.0 | 13.5 |
| Estimated cost | $1,080 | $1,620 |
| Timeline | 3 weeks | 5 weeks |

Reported comparison:

- Added features: 2
- Removed features: 1
- Hours change: +4.5
- Cost change: +$540

These values describe the current sample run, not validated client quotes.
The evaluation's success message applies only to its implemented checks; it is not a claim of 100% overall accuracy.

## Remaining Verification

- Task 1 tests and grounded-answer evaluation.
- Live AI calls with valid credentials.
- Task 2 live evaluation against Task 1.
- Task 3 live extraction and knowledge-backed feasibility.
- Review whether modified requirements are represented correctly in scope comparisons.
- Dependency security review.
- Hosted-service checks after deployment.
