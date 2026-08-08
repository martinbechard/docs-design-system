"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Verify deterministic scoring, usage parsing, ranking, and live-run safety.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import unittest

from evals import eval_harness as harness


class EvaluationHarnessTests(unittest.TestCase):
    """Exercise the harness without invoking Codex or using network services."""

    def test_exact_scoring_penalizes_duplicate_predictions(self) -> None:
        response = {
            "verdict": "FAIL",
            "issues": [
                {"rule_id": "DOC-LANG", "locator": "html", "severity": "major", "evidence": "missing"},
                {"rule_id": "DOC-LANG", "locator": "html", "severity": "major", "evidence": "missing"},
            ],
        }
        expected = {"verdict": "FAIL", "defects": [{"rule_id": "DOC-LANG", "locator": "html"}]}
        score = harness._score_response(response, expected)
        self.assertEqual((score["true_positive"], score["false_positive"], score["false_negative"]), (1, 1, 0))
        self.assertAlmostEqual(score["precision"], 0.5)
        self.assertTrue(score["verdict_exact"])

    def test_clean_page_scores_perfectly(self) -> None:
        score = harness._score_response({"verdict": "PASS", "issues": []}, {"verdict": "PASS", "defects": []})
        self.assertEqual(score["precision"], 1.0)
        self.assertEqual(score["recall"], 1.0)
        self.assertEqual(score["f1"], 1.0)
        self.assertTrue(score["verdict_exact"])

    def test_usage_parser_uses_last_cumulative_event(self) -> None:
        events = '\n'.join([
            '{"usage":{"input_tokens":10,"cached_input_tokens":2,"output_tokens":3}}',
            '{"type":"turn.completed","usage":{"input_tokens":20,"cached_input_tokens":5,"output_tokens":7}}',
        ])
        self.assertEqual(harness._usage_from_jsonl(events), {"input_tokens": 20, "cached_input_tokens": 5, "output_tokens": 7})

    def test_ranking_uses_strict_accuracy_then_credit_band_and_speed(self) -> None:
        config = {"accuracy_equivalence_band": 0.0, "cost_equivalence_band": 0.15}
        rows = [
            {"candidate_id": "fast-near-cost", "accuracy": 1.0, "estimated_credits": 110.0, "token_cost_proxy": 500.0, "wall_seconds": 1.0},
            {"candidate_id": "slow-cheapest", "accuracy": 1.0, "estimated_credits": 100.0, "token_cost_proxy": 400.0, "wall_seconds": 4.0},
            {"candidate_id": "too-expensive", "accuracy": 1.0, "estimated_credits": 116.0, "token_cost_proxy": 300.0, "wall_seconds": 0.5},
            {"candidate_id": "unpriced-spark", "accuracy": 1.0, "estimated_credits": None, "token_cost_proxy": 1.0, "wall_seconds": 0.1},
            {"candidate_id": "lower-accuracy", "accuracy": 0.99, "estimated_credits": 0.01, "token_cost_proxy": 1.0, "wall_seconds": 0.1},
        ]
        ranked = harness._rank(rows, config)
        self.assertEqual(
            [row["candidate_id"] for row in ranked],
            ["fast-near-cost", "slow-cheapest", "too-expensive", "unpriced-spark", "lower-accuracy"],
        )
        self.assertEqual(ranked[0]["ranking_cost_basis"], "estimated_credits")
        self.assertEqual(ranked[3]["ranking_cost_basis"], "unpriced_token_proxy")

    def test_uniquely_more_accurate_unpriced_candidate_wins(self) -> None:
        config = {"accuracy_equivalence_band": 0.0, "cost_equivalence_band": 0.15}
        rows = [
            {"candidate_id": "spark", "accuracy": 1.0, "estimated_credits": None, "token_cost_proxy": 100.0, "wall_seconds": 2.0},
            {"candidate_id": "priced", "accuracy": 0.99, "estimated_credits": 0.01, "token_cost_proxy": 1.0, "wall_seconds": 1.0},
        ]
        self.assertEqual(harness._rank(rows, config)[0]["candidate_id"], "spark")

    def test_plan_contains_all_wide_candidates_without_execution(self) -> None:
        planned = harness._plan_stage("wide")
        self.assertEqual(len(planned), 10)
        self.assertTrue(all(item["fixture"] == "01-wide.html" for item in planned))
        self.assertTrue(all("--json" in item["command"] for item in planned))

    def test_fixture_catalog_and_truth_are_complete(self) -> None:
        config = harness._config()
        truth = harness._truth()["fixtures"]
        staged = [name for stage in config["stages"] for name in stage["fixtures"]]
        self.assertEqual(set(staged), set(truth))
        self.assertEqual(len(staged), 5)
        self.assertEqual(sum(bool(item["defects"]) for item in truth.values()), 4)
        for fixture, expected in truth.items():
            html = (Path(harness.__file__).parent / "fixtures" / fixture).read_text(encoding="utf-8")
            for defect in expected["defects"]:
                if defect["locator"].startswith("#"):
                    self.assertIn(f'id="{defect["locator"][1:]}"', html)

    def test_credit_estimate_and_unpriced_spark_status(self) -> None:
        config = harness._config()
        row = {
            "score": {"true_positive": 1, "false_positive": 0, "false_negative": 0, "verdict_exact": True},
            "usage": {"input_tokens": 1_000_000, "cached_input_tokens": 0, "output_tokens": 0},
            "wall_seconds": 2.0,
        }
        priced = harness._aggregate({"id": "luna", "model": "gpt-5.6-luna", "effort": "low"}, [row], config)
        unpriced = harness._aggregate({"id": "spark", "model": "gpt-5.3-codex-spark", "effort": "low"}, [row], config)
        self.assertEqual(priced["estimated_credits"], 25.0)
        self.assertEqual(priced["pricing_status"], "priced")
        self.assertIsNone(unpriced["estimated_credits"])
        self.assertEqual(unpriced["pricing_status"], "unpriced")

    def test_credit_estimate_does_not_double_count_cached_input(self) -> None:
        rates = {"input_tokens": 25.0, "cached_input_tokens": 2.5, "output_tokens": 150.0}
        usage = {"input_tokens": 1_000_000, "cached_input_tokens": 400_000, "output_tokens": 0}
        self.assertEqual(harness._estimated_credits(usage, rates), 16.0)

    def test_run_refuses_without_explicit_live_confirmation(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            harness.main(["run", "--stage", "wide"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("live runs require", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
