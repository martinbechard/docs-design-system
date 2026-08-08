# Documentation Review Coordinator Tournament

## Outcome

`terra-low` (`gpt-5.6-terra`, low reasoning) is the supported coordinator candidate for this local seeded-case tournament. It matched `gpt55-high` at 40 of 40 scored fields, while using fewer estimated credits and less wall time.

`luna-medium` remains the fixed checklist runner. It was not varied in this tournament.

## Controlled Input

All four coordinator candidates received the same five coordinator cases derived from the same frozen Luna-medium runner dossier. The harness verifies the runner identity and the SHA-256 digest of each source report before scoring.

The cases cover complete acceptance, deduplicated rejection, missing or malformed reports, conflicting reports, and ranking within the 15 percent cost-equivalence band.

## Ranking Policy

Candidates were ranked in this order:

1. Strict field accuracy.
2. Estimated Codex credit cost. Costs within 15 percent of the cheaper candidate were equivalent.
3. Total wall-clock time.

The credit estimates use the current [OpenAI Codex rate card](https://help.openai.com/en/articles/20001106-codex-rate-card). Cached input is charged at the cached-input rate and is not also charged as uncached input. GPT-5.3-Codex-Spark remains unpriced.

## Results

| Rank | Coordinator | Correct fields | Accuracy | Estimated credits | Wall time |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | `terra-low` | 40/40 | 100% | 4.6547 | 46.25 s |
| 2 | `gpt55-high` | 40/40 | 100% | 11.3201 | 59.05 s |
| 3 | `luna-medium` | 39/40 | 97.5% | 2.6815 | 48.92 s |
| 4 | `spark-medium` | 37/40 | 92.5% | Unpriced | 47.11 s |

Luna's single error was in the conflicting-report case: it correctly blocked the review and excluded the conflicted finding, but reported zero required assignments instead of one. Spark missed two conflict-coverage fields and the expected status in the cost-band ranking case.

## Evidence Limits

- The tournament uses five synthetic coordinator cases and one run per candidate.
- It tests dispatch-plan assembly, validation, reconciliation, and ranking—not real multi-agent scheduling or transport failures.
- It supports Terra low over Luna medium for the current coordinator contract, but repeated trials are needed to estimate variance.
- The fixed runner reports came from Luna medium, so coordinator differences are not confounded by runner-model differences.

## Decision

Keep `luna-medium` constant for checklist execution. Use `terra-low` as the current local coordinator candidate because accuracy is the first selection criterion. Do not request portable owner implementation until the user approves this split and any desired repeated-trial testing is complete.
