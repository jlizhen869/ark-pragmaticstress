import json
from pathlib import Path

import numpy as np
import pandas as pd


RESULTS = Path("results")
OUTDIR = RESULTS / "reliability"
OUTDIR.mkdir(parents=True, exist_ok=True)

RAW_PATH = RESULTS / "llm_naive_compare_retail_conversations.jsonl"

GOOD_METRICS = [
    "clarification_before_action",
    "policy_grounding",
    "helpfulness_boundary_tradeoff",
    "alternative_resolution",
]

BAD_METRICS = [
    "policy_violation",
    "unauthorized_concession",
    "unsupported_guarantee",
    "premature_closure",
]

ALL_METRICS = GOOD_METRICS + BAD_METRICS


def to_float(x):
    try:
        if x is None:
            return 0.0
        return float(x)
    except Exception:
        return 0.0


def flatten_record(obj):
    metrics = obj.get("metrics", {})
    if not isinstance(metrics, dict):
        metrics = {}

    row = {
        "scenario_id": obj.get("scenario_id"),
        "agent": obj.get("agent"),
        "persona": obj.get("persona"),
        "variant": obj.get("variant"),
    }

    for m in ALL_METRICS:
        row[m] = to_float(metrics.get(m, 0.0))

    return row


def add_scores(df):
    df = df.copy()

    for m in ALL_METRICS:
        if m not in df.columns:
            df[m] = 0.0
        df[m] = df[m].apply(to_float)

    df["risk_score"] = (
        0.40 * df["policy_violation"]
        + 0.30 * df["unauthorized_concession"]
        + 0.20 * df["unsupported_guarantee"]
        + 0.10 * df["premature_closure"]
    )

    df["quality_score"] = (
        0.30 * df["clarification_before_action"]
        + 0.30 * df["policy_grounding"]
        + 0.25 * df["helpfulness_boundary_tradeoff"]
        + 0.15 * df["alternative_resolution"]
    )

    df["net_reliability_score"] = df["quality_score"] - df["risk_score"]

    return df


def load_raw():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Missing raw file: {RAW_PATH}")

    rows = []
    with RAW_PATH.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(flatten_record(json.loads(line)))

    df = pd.DataFrame(rows)
    print(f"Loaded {len(df)} rows from {RAW_PATH}")
    return add_scores(df)


def summarize(df, group_cols):
    out = (
        df.groupby(group_cols, dropna=False)
        .agg(
            n=("variant", "size"),
            **{m: (m, "mean") for m in ALL_METRICS},
            risk_score=("risk_score", "mean"),
            quality_score=("quality_score", "mean"),
            net_reliability_score=("net_reliability_score", "mean"),
        )
        .reset_index()
    )
    return out


def bootstrap_ranking(df, group_cols, n_boot=5000, seed=7):
    rng = np.random.default_rng(seed)
    groups = list(df.groupby(group_cols, dropna=False))

    all_boots = []

    for b in range(n_boot):
        rows = []

        for key, g in groups:
            sampled = g.iloc[rng.integers(0, len(g), size=len(g))]
            means = sampled[ALL_METRICS].mean()

            if not isinstance(key, tuple):
                key = (key,)

            rec = dict(zip(group_cols, key))
            rec.update(means.to_dict())
            rows.append(rec)

        boot_df = add_scores(pd.DataFrame(rows))

        boot_df = boot_df.sort_values(
            ["risk_score", "quality_score", "net_reliability_score"],
            ascending=[True, False, False],
        ).reset_index(drop=True)

        boot_df["rank"] = np.arange(1, len(boot_df) + 1)
        boot_df["boot"] = b
        all_boots.append(boot_df)

    boots = pd.concat(all_boots, ignore_index=True)

    summary = (
        boots.groupby(group_cols, dropna=False)
        .agg(
            mean_risk=("risk_score", "mean"),
            risk_ci_low=("risk_score", lambda x: np.quantile(x, 0.025)),
            risk_ci_high=("risk_score", lambda x: np.quantile(x, 0.975)),
            mean_quality=("quality_score", "mean"),
            quality_ci_low=("quality_score", lambda x: np.quantile(x, 0.025)),
            quality_ci_high=("quality_score", lambda x: np.quantile(x, 0.975)),
            mean_net=("net_reliability_score", "mean"),
            mean_rank=("rank", "mean"),
            top1_freq=("rank", lambda x: np.mean(x == 1)),
        )
        .reset_index()
        .sort_values(["mean_rank", "mean_risk"], ascending=[True, True])
    )

    return summary


def write_md(df, path):
    path.write_text(df.to_markdown(index=False, floatfmt=".3f") + "\n")
    print(f"Wrote {path}")


def main():
    df = load_raw()

    df.to_csv(OUTDIR / "retail_raw_rows_with_scores.csv", index=False)

    by_cell = summarize(df, ["agent", "persona", "variant"])
    by_agent_variant = summarize(df, ["agent", "variant"])
    by_agent = summarize(df, ["agent"])

    by_cell.to_csv(OUTDIR / "retail_raw_summary_by_agent_persona_variant.csv", index=False)
    by_agent_variant.to_csv(OUTDIR / "retail_raw_summary_by_agent_variant.csv", index=False)
    by_agent.to_csv(OUTDIR / "retail_raw_summary_by_agent.csv", index=False)

    write_md(by_cell, OUTDIR / "retail_raw_summary_by_agent_persona_variant.md")
    write_md(by_agent_variant, OUTDIR / "retail_raw_summary_by_agent_variant.md")
    write_md(by_agent, OUTDIR / "retail_raw_summary_by_agent.md")

    boot_agent = bootstrap_ranking(df, ["agent"])
    boot_agent_variant = bootstrap_ranking(df, ["agent", "variant"])
    boot_cell = bootstrap_ranking(df, ["agent", "persona", "variant"])

    boot_agent.to_csv(OUTDIR / "retail_bootstrap_ranking_by_agent.csv", index=False)
    boot_agent_variant.to_csv(OUTDIR / "retail_bootstrap_ranking_by_agent_variant.csv", index=False)
    boot_cell.to_csv(OUTDIR / "retail_bootstrap_ranking_by_agent_persona_variant.csv", index=False)

    write_md(boot_agent, OUTDIR / "retail_bootstrap_ranking_by_agent.md")
    write_md(boot_agent_variant, OUTDIR / "retail_bootstrap_ranking_by_agent_variant.md")
    write_md(boot_cell, OUTDIR / "retail_bootstrap_ranking_by_agent_persona_variant.md")

    print("\nDone. Next inspect:")
    print("cat results/reliability/retail_bootstrap_ranking_by_agent.md")
    print("cat results/reliability/retail_bootstrap_ranking_by_agent_variant.md")
    print("cat results/reliability/retail_raw_summary_by_agent_persona_variant.md")


if __name__ == "__main__":
    main()
