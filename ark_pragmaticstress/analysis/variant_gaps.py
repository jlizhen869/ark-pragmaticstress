from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


def read_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(x: Any) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute simple variant gaps from a breakdown CSV."
    )
    parser.add_argument(
        "--input", required=True, help="Breakdown CSV from summarize_results.py"
    )
    parser.add_argument(
        "--metric", default="policy_violation", help="Metric to compare."
    )
    parser.add_argument("--out", required=True, help="Output Markdown path.")
    args = parser.parse_args()

    rows = read_csv(Path(args.input))
    groups = defaultdict(dict)

    for row in rows:
        key = (row["agent"], row["persona"])
        groups[key][row["variant"]] = to_float(row.get(args.metric, 0.0))

    lines = [
        f"# Variant gaps for `{args.metric}`",
        "",
        "| agent | persona | en_mitigated - en_direct | mandarin_literal - en_direct | mandarin_pragmatic - mandarin_literal | mandarin_pragmatic - en_mitigated |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for (agent, persona), vals in sorted(groups.items()):
        en_direct = vals.get("en_direct", 0.0)
        en_mitigated = vals.get("en_mitigated", 0.0)
        mandarin_literal = vals.get("mandarin_literal", 0.0)
        mandarin_pragmatic = vals.get("mandarin_pragmatic", 0.0)

        lines.append(
            f"| {agent} | {persona} | "
            f"{en_mitigated - en_direct:.3f} | "
            f"{mandarin_literal - en_direct:.3f} | "
            f"{mandarin_pragmatic - mandarin_literal:.3f} | "
            f"{mandarin_pragmatic - en_mitigated:.3f} |"
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote variant gaps to {out}")


if __name__ == "__main__":
    main()
