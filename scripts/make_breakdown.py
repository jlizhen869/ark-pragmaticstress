import argparse
import json
from pathlib import Path

import pandas as pd


METRICS = [
    "alternative_resolution",
    "clarification_before_action",
    "helpfulness_boundary_tradeoff",
    "policy_grounding",
    "policy_violation",
    "premature_closure",
    "unauthorized_concession",
    "unsupported_guarantee",
]


def load_rows(path: Path):
    rows = []
    with path.open() as f:
        for line in f:
            obj = json.loads(line)
            row = {
                "scenario_id": obj.get("scenario_id"),
                "agent": obj.get("agent"),
                "persona": obj.get("persona"),
                "variant": obj.get("variant"),
            }
            metrics = obj.get("metrics", {})
            for m in METRICS:
                row[m] = float(metrics.get(m, 0))
            rows.append(row)
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    outdir = Path(args.output_dir)
    df = load_rows(Path(args.input))

    grouped = (
        df.groupby(["agent", "persona", "variant"], dropna=False)
        .agg(
            n=("scenario_id", "size"),
            **{m: (m, "mean") for m in METRICS},
        )
        .reset_index()
    )

    csv_path = outdir / f"{args.output_prefix}_breakdown.csv"
    md_path = outdir / f"{args.output_prefix}_breakdown.md"

    grouped.to_csv(csv_path, index=False)
    md_path.write_text(grouped.to_markdown(index=False, floatfmt=".3f") + "\n")

    print(f"Wrote {len(grouped)} grouped rows to {csv_path}")
    print(f"Wrote Markdown table to {md_path}")


if __name__ == "__main__":
    main()
