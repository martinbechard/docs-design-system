# Portable Documentation Design-System Review Proposal

## Approval Status

Not approved for owner implementation. This document is a local handoff draft only. It describes the original catalog-review experiment. Version 0.2.0 adds consumer review and an authoring skill; any future integration must explicitly scope those additions and verify them separately from the historical tournament evidence.

## Proposed Portable Artifacts

Ask the `dev-methodology` owner to implement these source-owned artifacts after user approval:

- One portable `review-documentation-design-system` skill with shared and page-specific checklist references.
- One simple, read-only checklist-runner conceptual agent that receives exactly one page and one checklist.
- One read-only review-coordinator conceptual agent that dispatches runners, validates coverage, reconciles evidence, and owns final acceptance.
- Generated runtime adapters for every supported runtime.
- Schema, generator, catalog, documentation, and regression-test updates required by the owner's methodology.
- Evaluation scenarios that preserve the local ranking policy and evidence contract without copying local model identifiers into conceptual agent definitions.

## Selected Local Profiles

The local seeded-fixture tournament selected `gpt-5.6-luna` with medium reasoning as the fixed checklist runner. A separate controlled coordinator tournament held those Luna reports constant and selected `gpt-5.6-terra` with low reasoning: Terra and GPT-5.5 high both scored 40 of 40 fields, while Luna medium scored 39 of 40.

The portable conceptual definitions should use owner-approved semantic model profiles rather than hardcoding provider model IDs. The owner may need to introduce or select a semantic coordinator profile that preserves the tested capability and cost intent.

## Required Owner Verification

The owner implementation should verify:

1. Every checklist ID remains unique and resolves from the skill.
2. The runner loads only the review skill, cannot mutate, cannot delegate, and returns every assigned checklist item exactly once.
3. The coordinator depends on the runner, does not perform checklist work itself, and applies accuracy, cost tolerance, then speed when ranking evaluation candidates.
4. Every generated adapter preserves agent dependencies, mutation authority, skill assignment, output contracts, and semantic model profiles.
5. Regression tests cover malformed reports, missing checklist items, conflicting evidence, unavailable runners, unpriced candidates, and the 15 percent cost-equivalence boundary.

## Evidence To Supply

- `skills/review-documentation-design-system/`
- `agents/documentation-design-system-checklist-runner.role.yaml`
- `agents/documentation-design-system-review-coordinator.role.yaml`
- `evals/results/tournament-report.md`
- `evals/results/coordinator-tournament-report.md`
- `evals/results/coordinator-review.json` (original runner-tournament review evidence; its cost figures predate the cached-input accounting correction, but its accepted winner is unchanged)

The local files are design candidates and evidence, not authoritative source files for `dev-methodology`.
