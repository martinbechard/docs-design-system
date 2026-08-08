#!/usr/bin/env python3
"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Run deterministic coordinator-model evaluations over seeded reconciliation cases.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from evals import eval_harness as shared


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
CONFIRMATION = "LIVE_COORDINATOR_MODEL_RUNS"
SCORE_FIELDS = ("status", "dispatches", "coverage_required", "coverage_completed", "coverage_missing", "finding_ids", "conflict_ids", "model_ranking")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cases() -> list[dict[str, Any]]:
    catalog = read_json(ROOT / "cases.json")
    if catalog.get("runner_candidate") != "luna-medium" or catalog.get("runner_reports_are_frozen") is not True:
        raise ValueError("coordinator cases must freeze luna-medium runner reports")
    for case in catalog["cases"]:
        for report in case["runner_reports"]:
            if report.get("runner_candidate") != "luna-medium":
                raise ValueError(f'{case["id"]} changes the runner candidate')
    return catalog["cases"]


def validate_frozen_runner_reports() -> None:
    manifest = read_json(ROOT / "frozen-runner-reports.json")
    if manifest.get("runner_candidate") != "luna-medium":
        raise ValueError("frozen runner manifest must use luna-medium")
    project_root = ROOT.parents[1]
    for report in manifest["reports"]:
        path = project_root / report["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != report["sha256"]:
            raise ValueError(f"frozen runner report digest mismatch: {path}")


def candidates() -> list[dict[str, str]]:
    return read_json(ROOT / "tournament.json")["candidates"]


def prompt(case: dict[str, Any]) -> str:
    template = (ROOT / "prompt.txt").read_text(encoding="utf-8")
    return template.replace("{{case_json}}", json.dumps(case, indent=2))


def command(candidate: dict[str, str], response_path: Path) -> list[str]:
    return [
        "codex", "exec", "--model", candidate["model"],
        "-c", f'model_reasoning_effort="{candidate["effort"]}"',
        "--sandbox", "read-only", "--skip-git-repo-check", "--ephemeral",
        "--output-schema", str(ROOT / "output.schema.json"),
        "--output-last-message", str(response_path), "--json", "-C", str(ROOT), "-",
    ]


def score(response: Any, expected: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(response, dict):
        return {"schema_valid": False, "correct": 0, "total": len(SCORE_FIELDS), "accuracy": 0.0, "field_results": {field: False for field in SCORE_FIELDS}}
    required = {"status", "dispatches", "coverage", "finding_ids", "conflict_ids", "model_ranking", "rationale"}
    schema_valid = set(response) == required and isinstance(response.get("coverage"), dict)
    observed = {
        "status": response.get("status"),
        "dispatches": response.get("dispatches"),
        "coverage_required": response.get("coverage", {}).get("required"),
        "coverage_completed": response.get("coverage", {}).get("completed"),
        "coverage_missing": response.get("coverage", {}).get("missing"),
        "finding_ids": response.get("finding_ids"),
        "conflict_ids": response.get("conflict_ids"),
        "model_ranking": response.get("model_ranking"),
    }
    wanted = {
        "status": expected["status"],
        "dispatches": expected["dispatches"],
        "coverage_required": expected["coverage"]["required"],
        "coverage_completed": expected["coverage"]["completed"],
        "coverage_missing": expected["coverage"]["missing"],
        "finding_ids": expected["finding_ids"],
        "conflict_ids": expected["conflict_ids"],
        "model_ranking": expected["model_ranking"],
    }
    field_results = {field: schema_valid and observed[field] == wanted[field] for field in SCORE_FIELDS}
    correct = sum(field_results.values())
    return {"schema_valid": schema_valid, "correct": correct, "total": len(SCORE_FIELDS), "accuracy": correct / len(SCORE_FIELDS), "field_results": field_results}


def run_one(candidate: dict[str, str], case: dict[str, Any]) -> dict[str, Any]:
    run_dir = OUTPUTS / candidate["id"] / case["id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    response_path = run_dir / "response.json"
    started = time.monotonic()
    completed = subprocess.run(command(candidate, response_path), input=prompt(case), text=True, capture_output=True, check=False)
    wall_seconds = time.monotonic() - started
    (run_dir / "events.jsonl").write_text(completed.stdout, encoding="utf-8")
    (run_dir / "stderr.log").write_text(completed.stderr, encoding="utf-8")
    try:
        response = read_json(response_path)
    except (OSError, ValueError, json.JSONDecodeError):
        response = None
    expected = read_json(ROOT / "ground-truth.json")[case["id"]]
    record = {"candidate": candidate, "case": case["id"], "exit_code": completed.returncode, "wall_seconds": wall_seconds, "usage": shared._usage_from_jsonl(completed.stdout), "score": score(response, expected)}
    write_json(run_dir / "run.json", record)
    return record


def aggregate(candidate: dict[str, str], rows: list[dict[str, Any]]) -> dict[str, Any]:
    config = read_json(ROOT / "tournament.json")
    usage = {key: sum(row["usage"][key] for row in rows) for key in shared._TOKEN_KEYS}
    correct = sum(row["score"]["correct"] for row in rows)
    total = sum(row["score"]["total"] for row in rows)
    rates = config["credit_rates_per_million_tokens"].get(candidate["model"])
    credits = shared._estimated_credits(usage, rates)
    return {"candidate_id": candidate["id"], "model": candidate["model"], "effort": candidate["effort"], "accuracy": correct / total, "correct_fields": correct, "total_fields": total, "usage": usage, "estimated_credits": credits, "token_cost_proxy": usage["input_tokens"] + 0.1 * usage["cached_input_tokens"] + 3 * usage["output_tokens"], "pricing_status": "unpriced" if credits is None else "priced", "wall_seconds": sum(row["wall_seconds"] for row in rows)}


def execute() -> dict[str, Any]:
    validate_frozen_runner_reports()
    all_cases = cases()
    summaries = []
    for candidate in candidates():
        rows = []
        for case in all_cases:
            run_path = OUTPUTS / candidate["id"] / case["id"] / "run.json"
            prior = read_json(run_path) if run_path.exists() else None
            if prior is not None and prior.get("exit_code") == 0 and prior.get("score", {}).get("schema_valid") is True:
                rows.append(prior)
            else:
                rows.append(run_one(candidate, case))
        summaries.append(aggregate(candidate, rows))
    ranking = shared._rank(summaries, {"accuracy_equivalence_band": 0.0, "cost_equivalence_band": 0.15})
    report = {"case_count": len(all_cases), "candidate_count": len(summaries), "ranking_policy": "strict field accuracy, then priced before unpriced, then 15% credit-cost band, then wall time", "ranking": ranking, "winner": ranking[0]["candidate_id"], "winner_provisional": ranking[0]["pricing_status"] == "unpriced"}
    write_json(OUTPUTS / "ranking.json", report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["plan", "run", "score"])
    parser.add_argument("--confirm-live", default="")
    args = parser.parse_args(argv)
    if args.action == "plan":
        print(json.dumps([{"candidate": candidate, "case": case["id"]} for candidate in candidates() for case in cases()], indent=2))
        return 0
    if args.action == "run" and args.confirm_live != CONFIRMATION:
        parser.error(f"live runs require --confirm-live {CONFIRMATION}")
    print(json.dumps(execute(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
