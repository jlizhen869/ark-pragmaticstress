# Resume Bullets

## Research / AI agent evaluation version

- Built Ark-PragmaticStress, an ArkSim-style diagnostic benchmark for evaluating whether customer-facing AI agents preserve policy boundaries under pragmatic and multilingual pressure across retail refund and subscription/billing scenarios.
- Designed matched English and Mandarin pragmatic variants (`en_direct`, `en_mitigated`, `mandarin_literal`, `mandarin_pragmatic`) to test whether the same underlying user intent produces different policy behavior under indirectness, mitigation, and persuasion pressure.
- Implemented conversation-level reliability metrics including policy violation rate, unauthorized concession rate, clarification-before-action, policy grounding, helpfulness-boundary tradeoff, risk score, quality score, and net reliability score.
- Ran comparative evaluations of naive and policy-aware scaffold LLM agents, identifying `scaffold_naive × mandarin_pragmatic` as the highest-risk failure mode and showing that policy-aware prompting sharply reduced unauthorized concessions.
- Added bootstrap reliability ranking, qualitative failure analysis, evaluator false-positive correction, annotation guidelines, limitations documentation, and reviewer-audit placeholders to support reproducible benchmark reporting.

## Shorter resume version

- Built an ArkSim-style agent reliability benchmark testing whether customer-facing agents maintain policy boundaries under indirect, mitigated, persuasive, and Mandarin pragmatic user requests.
- Implemented matched scenario variants, two agent baselines, policy-boundary metrics, bootstrap reliability ranking, and qualitative failure analysis across retail and subscription support scenarios.
- Identified Mandarin pragmatic pressure as a high-risk condition for a naive support agent while showing that a policy-aware agent preserved boundaries without over-refusing.
