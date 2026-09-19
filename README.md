# Documentation Design System Review Experiment

This project contains a local, approval-gated experiment for reviewing HTML documentation against the Documentation Design System. It does not modify or install artifacts into `dev-methodology`.

## Live Documentation

Browse the [Documentation Design System](https://martinbechard.github.io/docs-design-system/).

The `Deploy documentation to GitHub Pages` workflow publishes `docs/design-system/` on every push to `main`. It can also be run manually from the repository's Actions tab. GitHub Pages uses GitHub Actions as its publishing source.

## Review Architecture

The review system separates checklist execution from acceptance decisions:

1. `documentation-design-system-checklist-runner` receives one page and one checklist. Luna medium is the fixed local runner control.
2. The runner applies `review-documentation-design-system` and returns item-level evidence without making a suite-wide decision.
3. `documentation-design-system-review-coordinator` validates checklist coverage, reconciles runner evidence, and owns final acceptance. Terra low is the current local coordinator selection.

Detailed review procedure belongs to the skill and its page-specific checklists. The runner definition remains intentionally small.

## Local Artifacts

- `docs/design-system/`: the HTML design system.
- `skills/review-documentation-design-system/`: review method and ten page-specific checklists.
- `agents/`: local conceptual definitions for the runner and coordinator.
- `evals/`: deterministic fixtures, scoring, model matrix, and staged tournament runner.

## Evaluation Policy

The tournament ranks candidates in this order:

1. Accuracy.
2. Estimated Codex credit cost, with costs within 15 percent treated as equivalent.
3. Wall-clock speed.

GPT-5.3-Codex-Spark is a research preview with no final credit rate. The harness records its token usage and speed, but marks a unique-accuracy Spark winner as provisional.

## Portability Boundary

These definitions are local test candidates. After the user approves the selected design and evidence, prepare a request for the `dev-methodology` owner to implement a portable source definition, generated adapters, validation, and regression coverage. Do not copy these files into that project before approval.
