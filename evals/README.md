# Documentation review model evaluation

This directory contains a deterministic local tournament for models that review HTML documentation against a fixed checklist. It does not run a model unless the operator supplies an intentionally awkward live-run confirmation token.

## Evaluation contract

The five small fixtures include four pages with seeded defects and one clean control. [`ground-truth.json`](ground-truth.json) records the expected verdict and each defect's stable `rule_id` plus canonical CSS `locator`. Those two fields form the exact issue-matching key. [`review-output.schema.json`](review-output.schema.json) rejects missing and additional response fields.

Per fixture, the scorer records true positives, false positives, false negatives, precision, recall, F1, schema validity, and exact verdict. A stage's accuracy is `(aggregate F1 + verdict accuracy) / 2`.

Candidate ordering is deterministic and keeps accuracy strictly first:

1. Rank exact accuracy from highest to lowest; only equal scores share an accuracy tier.
2. Within an equal-accuracy tier, rank priced candidates before unpriced candidates because cost superiority cannot be established for an unpriced model.
3. Group priced candidates from lowest estimated credits upward; costs within 15% of the cheapest remaining candidate are equivalent.
4. Within a cost group, prefer lower total wall time, then candidate ID. If multiple unpriced candidates tie on accuracy, their weighted token proxy supplies their provisional cost ordering.

The token proxy weights uncached input as 1, cached input as 0.1, and output as 3. Published Codex credit rates are used as the ranking cost for priced models. Spark remains in the tournament but is marked `unpriced`; it follows equally accurate priced candidates, while a uniquely more accurate Spark can still win with `winner_provisional: true`.

## Staged tournament

[`tournament.json`](tournament.json) defines ten model/effort candidates and three sequential stages:

- `wide`: all candidates review `01-wide.html`; five advance.
- `semifinal`: those five review `02-semifinal.html`; three advance.
- `final`: those three review the three remaining pages; one wins.

Later stages read the preceding stage's `outputs/<stage>/ranking.json`, so the tournament cannot silently bypass advancement.

## Commands

Preview the exact commands without spending credits:

```sh
python3 -m evals.eval_harness plan --stage wide
```

Run deterministic tests (no Codex subprocess is started):

```sh
python3 -m unittest evals.test_eval_harness
```

Run stages one at a time only after reviewing the plan and accepting live model cost:

```sh
python3 -m evals.eval_harness run --stage wide --confirm-live LIVE_MODEL_RUNS_COST_CREDITS
python3 -m evals.eval_harness run --stage semifinal --confirm-live LIVE_MODEL_RUNS_COST_CREDITS
python3 -m evals.eval_harness run --stage final --confirm-live LIVE_MODEL_RUNS_COST_CREDITS
```

Each invocation is sequential. It writes raw Codex JSONL events, stderr, the schema-constrained final response, elapsed wall time, token counts, and a scored run record under `evals/outputs/`. Existing artifacts can be rescored without calling a model:

```sh
python3 -m evals.eval_harness score --stage wide
```

Completed `run.json` files are reused, so rerunning a partially completed stage resumes at its first missing candidate/fixture pair. Move or remove a specific run directory intentionally before repeating that invocation.

Do not commit `outputs/`; they are local run evidence and may be large.
