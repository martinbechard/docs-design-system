#!/usr/bin/env python3
"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Run and score deterministic staged evaluations of documentation-review models.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Iterable


_ROOT = Path(__file__).resolve().parent
_FIXTURES = _ROOT / "fixtures"
_OUTPUTS = _ROOT / "outputs"
_LIVE_CONFIRMATION = "LIVE_MODEL_RUNS_COST_CREDITS"
_TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _config() -> dict[str, Any]:
    return _read_json(_ROOT / "tournament.json")


def _truth() -> dict[str, Any]:
    return _read_json(_ROOT / "ground-truth.json")


def _stage(config: dict[str, Any], stage_id: str) -> dict[str, Any]:
    for stage in config["stages"]:
        if stage["id"] == stage_id:
            return stage
    raise ValueError(f"unknown stage: {stage_id}")


def _render_prompt(fixture_name: str) -> str:
    template = (_ROOT / "prompt.txt").read_text(encoding="utf-8")
    html = (_FIXTURES / fixture_name).read_text(encoding="utf-8")
    return template.replace("{{fixture_name}}", fixture_name).replace("{{fixture_html}}", html)


def _validate_response(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["response must be an object"]
    if set(value) != {"verdict", "issues"}:
        errors.append("response keys must be exactly verdict and issues")
    if value.get("verdict") not in {"PASS", "FAIL"}:
        errors.append("verdict must be PASS or FAIL")
    issues = value.get("issues")
    if not isinstance(issues, list):
        errors.append("issues must be an array")
        return errors
    allowed_rules = set(_read_json(_ROOT / "review-output.schema.json")["properties"]["issues"]["items"]["properties"]["rule_id"]["enum"])
    for index, issue in enumerate(issues):
        prefix = f"issues[{index}]"
        if not isinstance(issue, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if set(issue) != {"rule_id", "locator", "severity", "evidence"}:
            errors.append(f"{prefix} has missing or extra keys")
        if issue.get("rule_id") not in allowed_rules:
            errors.append(f"{prefix}.rule_id is invalid")
        if not isinstance(issue.get("locator"), str) or not issue.get("locator"):
            errors.append(f"{prefix}.locator must be a non-empty string")
        if issue.get("severity") not in {"minor", "major"}:
            errors.append(f"{prefix}.severity is invalid")
        if not isinstance(issue.get("evidence"), str) or not issue.get("evidence"):
            errors.append(f"{prefix}.evidence must be a non-empty string")
    return errors


def _usage_from_jsonl(text: str) -> dict[str, int]:
    last_usage: dict[str, int] | None = None
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        candidates = [event.get("usage")]
        result = event.get("result")
        if isinstance(result, dict):
            candidates.append(result.get("usage"))
        for candidate in candidates:
            if isinstance(candidate, dict) and any(key in candidate for key in _TOKEN_KEYS):
                last_usage = {
                    key: max(0, int(candidate.get(key, 0)))
                    for key in _TOKEN_KEYS
                }
    return last_usage or {key: 0 for key in _TOKEN_KEYS}


def _score_response(response: Any, expected: dict[str, Any]) -> dict[str, Any]:
    errors = _validate_response(response)
    issues = response.get("issues", []) if not errors else []
    predicted = Counter((item["rule_id"], item["locator"]) for item in issues)
    actual = Counter((item["rule_id"], item["locator"]) for item in expected["defects"])
    true_positive = sum((predicted & actual).values())
    false_positive = sum(predicted.values()) - true_positive
    false_negative = sum(actual.values()) - true_positive
    precision = true_positive / (true_positive + false_positive) if predicted else (1.0 if not actual else 0.0)
    recall = true_positive / (true_positive + false_negative) if actual else (1.0 if not predicted else 0.0)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    verdict_exact = not errors and response["verdict"] == expected["verdict"]
    return {
        "schema_valid": not errors,
        "schema_errors": errors,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "verdict_exact": verdict_exact,
    }


def _codex_command(candidate: dict[str, str], result_path: Path) -> list[str]:
    return [
        "codex", "exec", "--model", candidate["model"],
        "-c", f'model_reasoning_effort="{candidate["effort"]}"',
        "--sandbox", "read-only", "--skip-git-repo-check", "--ephemeral",
        "--output-schema", str(_ROOT / "review-output.schema.json"),
        "--output-last-message", str(result_path), "--json", "-C", str(_ROOT), "-",
    ]


def _run_one(candidate: dict[str, str], fixture_name: str, run_dir: Path) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    response_path = run_dir / "response.json"
    start = time.monotonic()
    completed = subprocess.run(
        _codex_command(candidate, response_path),
        input=_render_prompt(fixture_name), text=True, capture_output=True, check=False,
    )
    wall_seconds = time.monotonic() - start
    (run_dir / "events.jsonl").write_text(completed.stdout, encoding="utf-8")
    (run_dir / "stderr.log").write_text(completed.stderr, encoding="utf-8")
    response: Any = None
    parse_error: str | None = None
    try:
        response = _read_json(response_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parse_error = str(error)
    expected = _truth()["fixtures"][fixture_name]
    score = _score_response(response, expected)
    if parse_error:
        score["schema_errors"] = [parse_error]
    record = {
        "candidate": candidate,
        "fixture": fixture_name,
        "command": _codex_command(candidate, response_path),
        "exit_code": completed.returncode,
        "wall_seconds": wall_seconds,
        "usage": _usage_from_jsonl(completed.stdout),
        "score": score,
    }
    _write_json(run_dir / "run.json", record)
    return record


def _input_candidates(config: dict[str, Any], stage_id: str) -> list[dict[str, str]]:
    index = next(index for index, item in enumerate(config["stages"]) if item["id"] == stage_id)
    if index == 0:
        return config["candidates"]
    previous = config["stages"][index - 1]
    ranking = _read_json(_OUTPUTS / previous["id"] / "ranking.json")
    advancing_ids = {item["candidate_id"] for item in ranking["ranking"][: previous["advance"]]}
    return [candidate for candidate in config["candidates"] if candidate["id"] in advancing_ids]


def _estimated_credits(usage: dict[str, int], rates: dict[str, float] | None) -> float | None:
    if rates is None:
        return None
    uncached_input = max(usage["input_tokens"] - usage["cached_input_tokens"], 0)
    return (
        uncached_input * rates["input_tokens"]
        + usage["cached_input_tokens"] * rates["cached_input_tokens"]
        + usage["output_tokens"] * rates["output_tokens"]
    ) / 1_000_000


def _aggregate(candidate: dict[str, str], records: Iterable[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    rows = list(records)
    total_tp = sum(row["score"]["true_positive"] for row in rows)
    total_fp = sum(row["score"]["false_positive"] for row in rows)
    total_fn = sum(row["score"]["false_negative"] for row in rows)
    precision = total_tp / (total_tp + total_fp) if total_tp + total_fp else 1.0
    recall = total_tp / (total_tp + total_fn) if total_tp + total_fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    verdict_accuracy = sum(bool(row["score"]["verdict_exact"]) for row in rows) / len(rows)
    accuracy = (f1 + verdict_accuracy) / 2
    usage = {key: sum(row["usage"][key] for row in rows) for key in _TOKEN_KEYS}
    weights = config["cost_proxy_weights"]
    token_proxy = sum(usage[key] * weights[key] for key in _TOKEN_KEYS)
    rates = config["credit_rates_per_million_tokens"].get(candidate["model"])
    credits = _estimated_credits(usage, rates)
    return {
        "candidate_id": candidate["id"], "model": candidate["model"], "effort": candidate["effort"],
        "fixture_count": len(rows), "precision": precision, "recall": recall, "f1": f1,
        "verdict_accuracy": verdict_accuracy, "accuracy": accuracy,
        "usage": usage, "token_cost_proxy": token_proxy, "estimated_credits": credits,
        "pricing_status": "unpriced" if rates is None else "priced",
        "wall_seconds": sum(row["wall_seconds"] for row in rows),
    }


def _rank(summaries: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    remaining = list(summaries)
    ranked: list[dict[str, Any]] = []
    cost_band = config["cost_equivalence_band"]
    accuracy_tier = 0
    while remaining:
        accuracy_tier += 1
        best_accuracy = max(row["accuracy"] for row in remaining)
        peers = [row for row in remaining if row["accuracy"] == best_accuracy]
        remaining = [row for row in remaining if row not in peers]
        priced = [row for row in peers if row["estimated_credits"] is not None]
        unpriced = [row for row in peers if row["estimated_credits"] is None]
        for pricing_class, cost_key, pricing_peers in (
            ("priced", "estimated_credits", priced),
            ("unpriced", "token_cost_proxy", unpriced),
        ):
            cost_group = 0
            while pricing_peers:
                cost_group += 1
                cheapest = min(row[cost_key] for row in pricing_peers)
                ceiling = cheapest * (1 + cost_band)
                cost_peers = [row for row in pricing_peers if row[cost_key] <= ceiling]
                pricing_peers = [row for row in pricing_peers if row not in cost_peers]
                cost_peers.sort(key=lambda row: (row["wall_seconds"], row["candidate_id"]))
                for row in cost_peers:
                    ranked.append({
                        **row,
                        "accuracy_tier": accuracy_tier,
                        "cost_band": cost_group,
                        "ranking_cost_basis": "estimated_credits" if pricing_class == "priced" else "unpriced_token_proxy",
                    })
    return ranked


def _score_stage(stage_id: str) -> dict[str, Any]:
    config = _config()
    stage = _stage(config, stage_id)
    summaries = []
    for candidate in _input_candidates(config, stage_id):
        records = [_read_json(_OUTPUTS / stage_id / candidate["id"] / Path(name).stem / "run.json") for name in stage["fixtures"]]
        summaries.append(_aggregate(candidate, records, config))
    ranking = _rank(summaries, config)
    winner = ranking[0]
    report = {
        "stage": stage_id,
        "ranking_policy": "strict accuracy, then priced before unpriced, then 15% credit-cost band, then wall time",
        "accuracy_equivalence_band": config["accuracy_equivalence_band"],
        "cost_equivalence_band": config["cost_equivalence_band"],
        "ranking": ranking,
        "winner": winner["candidate_id"],
        "winner_provisional": winner["pricing_status"] == "unpriced",
    }
    _write_json(_OUTPUTS / stage_id / "ranking.json", report)
    return report


def _plan_stage(stage_id: str) -> list[dict[str, Any]]:
    config = _config()
    stage = _stage(config, stage_id)
    planned = []
    for candidate in _input_candidates(config, stage_id):
        for fixture in stage["fixtures"]:
            result = _OUTPUTS / stage_id / candidate["id"] / Path(fixture).stem / "response.json"
            planned.append({"candidate": candidate, "fixture": fixture, "command": _codex_command(candidate, result)})
    return planned


def _execute_stage(stage_id: str) -> dict[str, Any]:
    config = _config()
    stage = _stage(config, stage_id)
    for candidate in _input_candidates(config, stage_id):
        for fixture in stage["fixtures"]:
            run_dir = _OUTPUTS / stage_id / candidate["id"] / Path(fixture).stem
            run_record = run_dir / "run.json"
            if not run_record.exists():
                _run_one(candidate, fixture, run_dir)
    return _score_stage(stage_id)


def main(argv: list[str] | None = None) -> int:
    """Plan, execute, or rescore tournament stages; live execution requires an exact confirmation token."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    plan = subparsers.add_parser("plan", help="print invocations without running models")
    plan.add_argument("--stage", choices=["wide", "semifinal", "final"], default="wide")
    run = subparsers.add_parser("run", help="run one stage sequentially and score it")
    run.add_argument("--stage", choices=["wide", "semifinal", "final"], required=True)
    run.add_argument("--confirm-live", default="", help=argparse.SUPPRESS)
    score = subparsers.add_parser("score", help="rescore existing stage artifacts")
    score.add_argument("--stage", choices=["wide", "semifinal", "final"], required=True)
    args = parser.parse_args(argv)
    if args.action == "plan":
        print(json.dumps(_plan_stage(args.stage), indent=2))
        return 0
    if args.action == "run":
        if args.confirm_live != _LIVE_CONFIRMATION:
            parser.error(f"live runs require --confirm-live {_LIVE_CONFIRMATION}")
        print(json.dumps(_execute_stage(args.stage), indent=2))
        return 0
    print(json.dumps(_score_stage(args.stage), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
