from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def summarize(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not records:
        return []

    metric_keys = sorted(records[0]["metrics"].keys())
    groups: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)

    for record in records:
        key = (
            record.get("agent", "unknown_agent"),
            record["persona"],
            record["variant"],
        )
        groups[key].append(record)

    rows: List[Dict[str, Any]] = []
    for (agent, persona, variant), group_records in sorted(groups.items()):
        row: Dict[str, Any] = {
            "agent": agent,
            "persona": persona,
            "variant": variant,
            "n": len(group_records),
        }
        for metric in metric_keys:
            row[metric] = mean([float(r["metrics"].get(metric, 0.0)) for r in group_records])
        rows.append(row)

    return rows


def write_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: List[Dict[str, Any]], path: Path) -> None:
    if not rows:
        path.write_text("_No rows found._\n", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    lines = []
    lines.append("| " + " | ".join(fieldnames) + " |")
    lines.append("| " + " | ".join(["---"] * len(fieldnames)) + " |")

    for row in rows:
        lines.append("| " + " | ".join(format_value(row[col]) for col in fieldnames) + " |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize Ark-PragmaticStress JSONL results by agent x persona x variant."
    )
    parser.add_argument("--input", required=True, help="Path to conversations JSONL.")
    parser.add_argument("--csv-out", required=True, help="Output CSV path.")
    parser.add_argument("--md-out", required=True, help="Output Markdown table path.")
    args = parser.parse_args()

    records = list(load_jsonl(Path(args.input)))
    rows = summarize(records)

    csv_out = Path(args.csv_out)
    md_out = Path(args.md_out)
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    write_csv(rows, csv_out)
    write_markdown(rows, md_out)

    print(f"Loaded {len(records)} conversations.")
    print(f"Wrote {len(rows)} grouped rows to {csv_out}")
    print(f"Wrote Markdown table to {md_out}")


if __name__ == "__main__":
    main()
