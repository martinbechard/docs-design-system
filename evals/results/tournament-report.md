# Documentation Review Model Tournament

## Outcome

`luna-medium` (`gpt-5.6-luna`, medium reasoning) is the supported winner for this local seeded-fixture tournament.

The independent advanced coordinator returned `ACCEPTED`. Its original model-produced output is retained in `coordinator-review.json`. That output predates the cached-input accounting correction described below; the corrected deterministic rescore preserves the same winner.

## Ranking Policy

Candidates were ranked in this order:

1. Strict measured accuracy.
2. Estimated Codex credit cost. Costs within 15 percent of the cheaper candidate were equivalent.
3. Total wall-clock time.

The credit estimates use the current [OpenAI Codex rate card](https://help.openai.com/en/articles/20001106-codex-rate-card). Cached input is subtracted from total input before the uncached-input rate is applied, preventing double charging. GPT-5.3-Codex-Spark remains unpriced because its research-preview rate is not final.

## Tournament

The harness completed 24 model runs.

### Wide Round

Ten candidates reviewed `01-wide.html`. Five advanced:

1. `luna-medium`
2. `gpt55-low`
3. `gpt55-medium`
4. `spark-medium`
5. `terra-low`

### Semifinal

Five candidates reviewed `02-semifinal.html`. Three advanced:

1. `luna-medium`
2. `terra-low`
3. `gpt55-low`

All five achieved perfect semifinal detection. Cost separated the advancing order.

### Final

The final three reviewed two additional defect pages and one clean control. All three achieved precision, recall, F1, verdict accuracy, and aggregate accuracy of 1.0.

| Rank | Candidate | Estimated credits | Wall time |
| --- | --- | ---: | ---: |
| 1 | `luna-medium` | 1.6152 | 28.78 s |
| 2 | `terra-low` | 2.9742 | 23.94 s |
| 3 | `gpt55-low` | 5.1233 | 27.97 s |

Terra was 4.84 seconds faster than Luna. Speed did not override Terra's approximately 1.8-times higher estimated credit cost at equal accuracy.

## Evidence Limits

- The tournament uses five small seeded fixtures, not the full 91-item design-system checklist set.
- The result demonstrates accurate detection of known artificial defects. It does not establish complete conformance-review accuracy on the real `dev-methodology` pages.
- Each candidate ran once per assigned fixture. Repeated-trial variance is not yet measured.
- Spark participated, but its unknown price prevented cost comparison when accuracy tied.

## Decision

Use `luna-medium` as the fixed checklist-runner profile for coordinator experiments. The coordinator tournament is documented separately in `coordinator-tournament-report.md`. Before portable adoption, run the selected profiles against representative real pages with reviewed ground truth and repeat selected fixtures to measure variance.
