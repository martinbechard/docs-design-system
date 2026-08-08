# Coordinator Evidence Review

Act as the local `documentation-design-system-review-coordinator` defined in `agents/documentation-design-system-review-coordinator.role.yaml`.

Review these retained artifacts:

- `evals/tournament.json`
- `evals/ground-truth.json`
- `evals/outputs/wide/ranking.json`
- `evals/outputs/semifinal/ranking.json`
- `evals/outputs/final/ranking.json`
- Every `run.json` below `evals/outputs/`

Confirm that advancement followed the configured top-five and top-three boundaries. Confirm that the final ranking applies strict accuracy first, estimated Codex credit cost second with a 15 percent equivalence band, and wall time third. Do not rescore from intuition or change the ranking policy.

Return only JSON matching `evals/coordinator-output.schema.json`. Accept a winner only if the retained evidence supports it. State limitations, including fixture breadth and the difference between seeded-fixture performance and real-page conformance review.
