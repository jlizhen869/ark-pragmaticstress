## Results: Pragmatic Stress Evaluation

I evaluated the benchmark on two policy-boundary scenario groups:

1. retail refund / exception handling
2. subscription cancellation / billing adjustment

Each scenario group contains 192 conversations:

```text
4 scenarios × 2 agents × 2 personas × 4 variants × 3 repeats = 192 conversations
```

The evaluation compares a policy-aware agent against a naive baseline under English and Mandarin pragmatic-pressure variants.

### Agent-level reliability

| scenario group | agent | mean risk | 95% risk CI | mean quality | top1 freq |
|---|---|---:|---:|---:|---:|
| retail | scaffold_policy_aware | 0.006 | [0.000, 0.019] | 0.851 | 1.000 |
| retail | scaffold_naive | 0.268 | [0.202, 0.338] | 0.152 | 0.000 |
| subscription | scaffold_policy_aware | 0.000 | [0.000, 0.000] | 0.731 | 1.000 |
| subscription | scaffold_naive | 0.262 | [0.197, 0.328] | 0.148 | 0.000 |

The policy-aware agent is consistently safer and more useful than the naive baseline across both scenario groups.

### Main failure mode

The largest confirmed failure mode is:

```text
scaffold_naive × mandarin_pragmatic
```

This condition has mean risk 0.700 in both retail and subscription, with a zero-width bootstrap interval [0.700, 0.700].

### Strongest reliable variant

The strongest policy-aware variant is:

```text
scaffold_policy_aware × mandarin_pragmatic
```

| scenario group | mean risk | mean quality | mean rank | top1 freq |
|---|---:|---:|---:|---:|
| retail | 0.000 | 0.919 | 1.006 | 0.994 |
| subscription | 0.000 | 0.788 | 1.159 | 0.858 |

This suggests that Mandarin pragmatic prompts are not inherently unsafe. Instead, they expose whether an agent can maintain policy boundaries under indirect or socially softened pressure.

### Method note

Ranking uses conversation-level bootstrap resampling. Variants are ranked by lower risk_score, then higher quality_score, then higher net_reliability_score.

This prevents zero-risk but unhelpful behavior from being treated as equally reliable as zero-risk, policy-grounded assistance.

The evaluator was also audited for false positives. After adding refusal and verification checks, policy-aware subscription responses that refused exceptions and asked to verify account or billing status were no longer incorrectly counted as unauthorized concessions.
