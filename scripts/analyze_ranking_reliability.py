from pathlib import Path
import argparse
import math
import random
import pandas as pd


def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return float("nan"), float("nan")

    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(
        (p * (1 - p) / n) + (z * z / (4 * n * n))
    ) / denom

    return max(0.0, center - margin), min(1.0, center + margin)


def infer_count_from_rate(rate, n):
    return int(round(float(rate) * int(n)))


def add_counts_and_ci(df, metric_col):
    rows = []

    for _, row in df.iterrows():
        n = int(row["n"])
        rate = float(row[metric_col])
        k = infer_count_from_rate(rate, n)
        lo, hi = wilson_ci(k, n)

        new_row = row.to_dict()
        new_row[f"{metric_col}_count"] = k
        new_row[f"{metric_col}_count_text"] = f"{k}/{n}"
        new_row[f"{metric_col}_ci_low"] = lo
        new_row[f"{metric_col}_ci_high"] = hi
        rows.append(new_row)

    return pd.DataFrame(rows)


def bootstrap_rank_stability(df, metric_col, group_by, n_boot=2000):
    groups = sorted(df[group_by].dropna().unique())

    top1_counts = {g: 0 for g in groups}
    rank_sums = {g: 0.0 for g in groups}

    expanded_by_group = {g: [] for g in groups}

    for _, row in df.iterrows():
        group = row[group_by]
        n = int(row["n"])
        k = infer_count_from_rate(row[metric_col], n)

        expanded_by_group[group].extend([1] * k)
        expanded_by_group[group].extend([0] * (n - k))

    for _ in range(n_boot):
        sampled_rates = {}

        for group in groups:
            ys = expanded_by_group[group]
            if not ys:
                sampled_rates[group] = float("nan")
                continue

            sample = [random.choice(ys) for _ in ys]
            sampled_rates[group] = sum(sample) / len(sample)

        ranked = sorted(groups, key=lambda g: sampled_rates[g])

        for rank, group in enumerate(ranked, start=1):
            rank_sums[group] += rank

        top1_counts[ranked[0]] += 1

    out = []
    for group in groups:
        ys = expanded_by_group[group]
        out.append({
            group_by: group,
            "mean_rank": rank_sums[group] / n_boot,
            "top1_freq": top1_counts[group] / n_boot,
            "observed_rate": sum(ys) / len(ys) if ys else float("nan"),
            "n_total": len(ys),
        })

    return pd.DataFrame(out).sort_values(
        ["mean_rank", "top1_freq"],
        ascending=[True, False],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--metric", required=True)
    parser.add_argument("--group_by", default="agent")
    parser.add_argument("--outdir", default="results/reliability")
    parser.add_argument("--n_boot", type=int, default=2000)
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    print("\nColumns found:")
    for c in df.columns:
        print("-", c)

    for col in ["n", args.metric, args.group_by]:
        if col not in df.columns:
            raise ValueError(
                f"Column {col!r} not found. Available columns: {list(df.columns)}"
            )

    ci_df = add_counts_and_ci(df, args.metric)

    stem = input_path.stem
    ci_csv = outdir / f"{stem}_{args.metric}_counts_ci.csv"
    ci_md = outdir / f"{stem}_{args.metric}_counts_ci.md"

    ci_df.to_csv(ci_csv, index=False)
    ci_df.to_markdown(ci_md, index=False)

    rank_df = bootstrap_rank_stability(
        df=df,
        metric_col=args.metric,
        group_by=args.group_by,
        n_boot=args.n_boot,
    )

    rank_csv = outdir / f"{stem}_{args.metric}_by_{args.group_by}_bootstrap_ranking.csv"
    rank_md = outdir / f"{stem}_{args.metric}_by_{args.group_by}_bootstrap_ranking.md"

    rank_df.to_csv(rank_csv, index=False)
    rank_df.to_markdown(rank_md, index=False)

    print("\nWrote:")
    print(ci_csv)
    print(ci_md)
    print(rank_csv)
    print(rank_md)

    print("\nBootstrap ranking:")
    print(rank_df.to_string(index=False))


if __name__ == "__main__":
    main()
