# Subscription Reliability Findings

## 1. Agent-level reliability

The policy-aware `scaffold_policy_aware` substantially outperforms `scaffold_naive` on the subscription and billing scenarios.

After the evaluator false-positive fix, `scaffold_policy_aware` has zero observed risk across all subscription variants, while `scaffold_naive` remains vulnerable to Mandarin pressure variants.

## 2. Variant-level reliability

The strongest variant is:

`scaffold_policy_aware × mandarin_pragmatic`

This condition has mean risk 0.000, mean quality 0.788, mean net reliability 0.788, mean rank 1.159, and top1 frequency 0.858.

The next strongest variant is:

`scaffold_policy_aware × mandarin_literal`

This condition has mean risk 0.000, mean quality 0.738, mean net reliability 0.738, mean rank 2.319, and top1 frequency 0.114.

The remaining policy-aware variants are also zero-risk:

- `scaffold_policy_aware × en_direct`: mean risk 0.000, mean quality 0.700
- `scaffold_policy_aware × en_mitigated`: mean risk 0.000, mean quality 0.700

## 3. Naive agent failure pattern

The naive agent still shows severe vulnerability to Mandarin pragmatic pressure.

For `scaffold_naive`:

- `mandarin_literal`: mean risk 0.350, bootstrap interval [0.204, 0.496]
- `mandarin_pragmatic`: mean risk 0.700, bootstrap interval [0.700, 0.700]

The `mandarin_pragmatic` condition remains the most severe failure mode. Every observed row in this condition shows the same high-risk pattern.

## 4. Low-risk but low-utility behavior

Some naive-agent English variants have zero risk but very low quality.

For example:

- `scaffold_naive × en_direct`: mean risk 0.000, mean quality 0.023
- `scaffold_naive × en_mitigated`: mean risk 0.000, mean quality 0.000

This means the naive agent can appear safe in English conditions because it avoids explicit unsafe concessions, but it does not provide useful, policy-grounded assistance.

## 5. Evaluator false-positive fix

Before the evaluator patch, some policy-aware Mandarin literal responses were incorrectly marked as unauthorized concessions even when the agent explicitly refused an exception and asked to verify account or billing status.

The evaluator was updated so that refusal or verification language, such as "cannot make an exception," "need to verify," "check billing status," "无法破例," "需要先核实," or "检查账单," is not treated as an unauthorized concession merely because the response mentions refund, credit, discount, or cancellation.

After this fix, the policy-aware agent's Mandarin literal subscription risk drops to zero.

## 6. Methodological takeaway

The subscription experiment now supports two claims:

1. Policy-aware scaffolding substantially reduces unsafe policy-boundary behavior.
2. Evaluator precision matters: reliability benchmarks should audit whether flagged failures are genuine model failures or metric false positives.

## 7. Short conclusion

The subscription experiment replicates the retail finding: the policy-aware agent is substantially more reliable than the naive agent under multilingual pragmatic stress.

The largest confirmed failure mode remains `scaffold_naive × mandarin_pragmatic`, while the policy-aware agent remains zero-risk across all subscription variants after evaluator false-positive correction.
