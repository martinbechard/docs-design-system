"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Tests deterministic scoring for the coordinator-model evaluation.
"""

import unittest

from evals.coordinator import eval_coordinators as subject


class CoordinatorEvaluationTests(unittest.TestCase):
    def test_ground_truth_scores_all_fields(self) -> None:
        expected = subject.read_json(subject.ROOT / "ground-truth.json")["accept-complete"]
        response = {**expected, "rationale": "Complete evidence."}
        result = subject.score(response, expected)
        self.assertEqual(result["accuracy"], 1.0)
        self.assertTrue(result["schema_valid"])

    def test_wrong_status_loses_one_field(self) -> None:
        expected = subject.read_json(subject.ROOT / "ground-truth.json")["block-conflict"]
        response = {**expected, "status": "ACCEPTED", "rationale": "Wrong."}
        result = subject.score(response, expected)
        self.assertEqual(result["correct"], len(subject.SCORE_FIELDS) - 1)

    def test_plan_has_twenty_runs(self) -> None:
        self.assertEqual(len(subject.candidates()) * len(subject.cases()), 20)

    def test_luna_runner_reports_are_frozen(self) -> None:
        subject.validate_frozen_runner_reports()
        for case in subject.cases():
            self.assertTrue(all(report["runner_candidate"] == "luna-medium" for report in case["runner_reports"]))


if __name__ == "__main__":
    unittest.main()
