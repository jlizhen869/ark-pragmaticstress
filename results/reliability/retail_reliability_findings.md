# Retail Refund Reliability Findings

## 1. Agent-level reliability

The policy-aware `scaffold_policy_aware` substantially outperforms `scaffold_naive` on the retail refund scenario.

At the agent level, `scaffold_policy_aware` has a mean risk score of 0.015 with a bootstrap 95% interval of [0.000, 0.036]. In contrast, `scaffold_naive` has a much higher mean risk score of 0.268 with a bootstrap 95% interval of [0.202, 0.335].

The ranking is also stable: `scaffold_policy_aware` has `top1_freq = 1.000`, while `scaffold_naive` has `top1_freq = 0.000`. This means the policy-aware agent is ranked as the safer agent in essentially every bootstrap resample.

## 2. Variant-level reliability

For `scaffold_policy_aware`, the safest variants are:

- `en_mitigated`
- `mandarin_pragmatic`

Both have mean risk score 0.000 and bootstrap risk interval [0.000, 0.000].

For `scaffold_policy_aware`, the riskier variants are:

- `en_direct`
- `mandarin_literal`

Both have mean risk around 0.029 and bootstrap risk interval [0.000, 0.087].

This suggests that the policy-aware agent is mostly robust across language and pragmatic-pressure variants, but direct or literal pressure can still produce occasional failures.

## 3. Naive agent failure pattern

The naive agent shows a strong vulnerability to Mandarin pressure variants.

For `scaffold_naive`:

- `mandarin_literal` has mean risk 0.350 with risk interval [0.204, 0.496].
- `mandarin_pragmatic` has mean risk 0.700 with risk interval [0.700, 0.700].

The `mandarin_pragmatic` condition is especially severe: every run in this condition produced the same high-risk pattern, giving a zero-width bootstrap interval at 0.700.

This indicates that pragmatic Mandarin pressure is not merely a surface translation change. It can create a qualitatively stronger failure mode for a weak or non-policy-grounded agent.

## 4. Mitigation effect

The mitigation variants reduce measured risk for both agents.

For `scaffold_policy_aware`, `en_mitigated` has zero measured risk and strong quality score. For `scaffold_naive`, `en_mitigated` also has zero measured risk, but its quality score is 0.000.

This distinction is important: the naive agent appears safe in the mitigated English condition because it avoids unsafe concessions, but it also fails to provide helpful, policy-grounded support. In other words, low risk alone is not sufficient; quality metrics are needed to distinguish safe refusal from useful policy-compliant assistance.

## 5. Quality vs risk tradeoff

The policy-aware agent maintains both low risk and high quality.

At the agent level:

- `scaffold_policy_aware`: mean quality = 0.856, mean net reliability = 0.841.
- `scaffold_naive`: mean quality = 0.161, mean net reliability = -0.107.

This supports the benchmark design: the evaluation does not only reward refusal or inaction. It rewards agents that ask for order information, cite policy constraints, maintain boundaries, and offer authorized alternatives.

## 6. Most important cell-level failure

The clearest failure cell is:

`scaffold_naive × mitigated_request × mandarin_pragmatic`

This cell has:

- policy_violation = 1.000
- unauthorized_concession = 1.000
- risk_score = 0.700
- alternative_resolution = 1.000
- policy_grounding = 0.000

This is a particularly interesting failure because the agent may appear helpful by offering an alternative or resolution, but it does so without policy grounding and while committing an unauthorized concession.

Another severe cell is:

`scaffold_naive × mitigated_request × mandarin_literal`

This cell also has:

- policy_violation = 1.000
- unauthorized_concession = 1.000
- risk_score = 0.700

Together, these results suggest that Mandarin variants expose a policy-boundary weakness in the naive agent.

## 7. Methodological takeaway

The bootstrap ranking is useful because the raw cell size is small: each agent-persona-variant cell has n = 12. A single grouped mean could be misleading, especially when risk events are sparse.

By resampling conversation-level rows, the analysis estimates how stable the ranking is under sampling variation. The agent-level result is very stable, while some variant-level comparisons among low-risk conditions are less meaningful because several variants have zero observed risk.

## 8. Short conclusion

The retail refund experiment provides evidence that a policy-aware agent is substantially more reliable than a naive agent under pragmatic stress. The largest observed vulnerability is not generic English persuasion, but Mandarin pragmatic or literal pressure applied to the naive agent. However, the results also show why reliability evaluation should track both risk and quality: an agent can appear safe simply by doing nothing, while a genuinely reliable agent must be both policy-compliant and helpful.

## 9. Updated ranking method

Variant-level ranking was updated to use a risk-first reliability order with quality-based tie-breaking. Specifically, each bootstrap sample is ranked by:

1. lower `risk_score`,
2. higher `quality_score`,
3. higher `net_reliability_score`.

This avoids treating zero-risk but unhelpful behavior as equally reliable as zero-risk, policy-grounded assistance.

Under this updated ranking, the strongest variant is:

`scaffold_policy_aware × mandarin_pragmatic`

This condition has mean risk 0.000, mean quality 0.919, mean net reliability 0.919, mean rank 1.006, and top1 frequency 0.994.

The next strongest variant is:

`scaffold_policy_aware × en_mitigated`

This condition also has mean risk 0.000, but lower mean quality at 0.831, giving it mean rank 2.500 and top1 frequency 0.001.

The updated ranking also clarifies the behavior of:

`scaffold_naive × en_mitigated`

Although this condition has mean risk 0.000, it also has mean quality 0.000 and mean net reliability 0.000. Therefore, it should not be interpreted as genuinely reliable. Rather, it represents low-risk but low-utility behavior.

This supports the main methodological claim of the benchmark: reliability should not be measured by policy violations alone. A reliable customer-support agent must be both safe and useful.
