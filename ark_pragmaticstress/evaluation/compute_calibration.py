"""
Compute pilot calibration statistics between rule-based metrics and judge labels.

Example:
    python evaluation/compute_calibration.py \
        --input results/calibration_judge_labels_dry_run.jsonl \
        --output results/calibration_report.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

LABELS = [
    "policy_violation",
    "unauthorized_concession",
    "refund_promised_before_check",
    "admitted_fault_without_evidence",
    "quality_ok",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def as_bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    return bool(value)


def get_rule_label(row: dict[str, Any], label: str) -> bool | None:
    metrics = row.get("rule_metrics") or {}
    if label in metrics:
        return as_bool_or_none(metrics[label])
    return None


def get_judge_label(row: dict[str, Any], label: str) -> bool | None:
    judge = row.get("judge_labels") or {}
    if judge.get("dry_run"):
        return None
    if label in judge:
        return as_bool_or_none(judge[label])
    return None


def binary_stats(pairs: list[tuple[bool, bool]]) -> dict[str, float | int | None]:
    if not pairs:
        return {
            "n": 0,
            "tp": 0,
            "tn": 0,
            "fp": 0,
            "fn": 0,
            "accuracy": None,
            "precision": None,
            "recall": None,
            "f1": None,
            "kappa": None,
        }

    tp = sum(1 for r, j in pairs if r and j)
    tn = sum(1 for r, j in pairs if not r and not j)
    fp = sum(1 for r, j in pairs if r and not j)
    fn = sum(1 for r, j in pairs if not r and j)

    n = len(pairs)
    accuracy = (tp + tn) / n

    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None

    if precision is not None and recall is not None and precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = None

    rule_pos = (tp + fp) / n
    rule_neg = (tn + fn) / n
    judge_pos = (tp + fn) / n
    judge_neg = (tn + fp) / n
    expected = rule_pos * judge_pos + rule_neg * judge_neg
    kappa = (accuracy - expected) / (1 - expected) if expected != 1 else None

    return {
        "n": n,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "kappa": kappa,
    }


def fmt(value: Any) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Judge-label JSONL")
    parser.add_argument("--output", required=True, help="Markdown report path")
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))

    label_stats = {}
    for label in LABELS:
        pairs: list[tuple[bool, bool]] = []
        for row in rows:
            rule = get_rule_label(row, label)
            judge = get_judge_label(row, label)
            if rule is None or judge is None:
                continue
            pairs.append((rule, judge))
        label_stats[label] = binary_stats(pairs)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as out:
        out.write("# Calibration Report\n\n")
        out.write(
            "**Status:** Pilot calibration report. This dry-run report verifies the calibration pipeline structure, but does not contain external judge labels. It is not a final human-validation study.\n\n"
        )

        out.write("## Input\n\n")
        out.write(f"- Source: `{args.input}`\n")
        out.write(f"- Rows loaded: {len(rows)}\n\n")

        out.write("## Label agreement summary\n\n")
        out.write(
            "| label | n | accuracy | precision | recall | F1 | kappa | TP | TN | FP | FN |\n"
        )
        out.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")

        for label, stats in label_stats.items():
            out.write(
                f"| {label} | {fmt(stats.get('n'))} | {fmt(stats.get('accuracy'))} | "
                f"{fmt(stats.get('precision'))} | {fmt(stats.get('recall'))} | "
                f"{fmt(stats.get('f1'))} | {fmt(stats.get('kappa'))} | "
                f"{fmt(stats.get('tp'))} | {fmt(stats.get('tn'))} | "
                f"{fmt(stats.get('fp'))} | {fmt(stats.get('fn'))} |\n"
            )

        out.write("\n## Interpretation\n\n")
        out.write(
            "Because the current checked-in judge-label file is a dry run, agreement values are reported as `NA`. To compute real agreement, run `evaluation/llm_judge.py` without `--dry-run` after setting `OPENAI_API_KEY`, or replace the judge labels with human annotations.\n\n"
        )

        out.write("## Limitations\n\n")
        out.write("- This report depends on the quality of the judge labels.\n")
        out.write("- Dry-run labels are excluded from agreement statistics.\n")
        out.write(
            "- A full study should use larger stratified samples and multiple human annotators.\n"
        )
        out.write(
            "- Variant-level and bilingual review are recommended for Mandarin pragmatic cases.\n"
        )

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
