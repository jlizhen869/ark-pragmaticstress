# Cross-Scenario Reliability Findings

## 1. Replicated agent-level result

Across both retail and subscription/billing scenario groups, the policy-aware `scaffold_policy_aware` is substantially more reliable than `scaffold_naive`.

In retail:

- `scaffold_policy_aware`: mean risk 0.006, 95% interval [0.000, 0.019], mean quality 0.851
- `scaffold_naive`: mean risk 0.268, 95% interval [0.202, 0.338], mean quality 0.152

In subscription:

- `scaffold_policy_aware`: mean risk 0.000, 95% interval [0.000, 0.000], mean quality 0.731
- `scaffold_naive`: mean risk 0.262, 95% interval [0.197, 0.328], mean quality 0.148

In both scenario groups, `scaffold_policy_aware` has top1 frequency 1.000 and `scaffold_naive` has top1 frequency 0.000.

## 2. Mandarin pragmatic pressure consistently exposes naive-agent weakness

The most severe confirmed failure mode is:

`scaffold_naive × mandarin_pragmatic`

This variant has mean risk 0.700 in both retail and subscription, with zero-width bootstrap intervals [0.700, 0.700]. This means the high-risk pattern is stable across observed runs.

## 3. Policy-aware agent remains reliable under Mandarin pragmatic pressure

The strongest policy-aware variant in both scenario groups is:

`scaffold_policy_aware × mandarin_pragmatic`

In retail, it has mean risk 0.000, mean quality 0.919, mean rank 1.006, and top1 frequency 0.994.

In subscription, it has mean risk 0.000, mean quality 0.788, mean rank 1.159, and top1 frequency 0.858.

This suggests that Mandarin pragmatic prompts are not inherently unsafe. Instead, they expose whether the agent has strong policy-boundary handling.

## 4. Low-risk behavior is not always reliable behavior

Some naive-agent English variants have zero measured risk but very low quality.

Examples:

- retail `scaffold_naive × en_mitigated`: mean risk 0.000, mean quality 0.000
- subscription `scaffold_naive × en_mitigated`: mean risk 0.000, mean quality 0.000
- subscription `scaffold_naive × en_direct`: mean risk 0.000, mean quality 0.023

This supports the use of a risk-first, quality-tiebreak ranking. A model that avoids explicit policy violations by giving empty or unhelpful responses should not be ranked as equally reliable as a model that is both safe and useful.

## 5. Evaluator audit improved benchmark validity

The subscription analysis initially revealed evaluator false positives for policy-aware Mandarin literal responses. These responses explicitly refused exceptions and asked to verify account or billing status, but were initially flagged as unauthorized concessions.

After adding refusal and verification language checks, the policy-aware subscription risk dropped to zero across variants, while the naive Mandarin failure modes remained.

This strengthens the benchmark: the final results better distinguish genuine model failures from metric artifacts.

## 6. Overall conclusion

Across two scenario groups, the benchmark supports the main hypothesis: pragmatic multilingual stress testing reveals policy-boundary failures that ordinary English-only prompting can miss.

The policy-aware agent is consistently safer and more useful than the naive baseline. The largest confirmed vulnerability is Mandarin pragmatic pressure applied to the naive agent.
