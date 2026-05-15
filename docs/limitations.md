# Limitations

## 1. Simulated conversations, not real users

The current benchmark uses synthetic users and simulated conversations. Results measure agent behavior under controlled test stimuli, not real-world customer behavior.

## 2. Mandarin variants are controlled stimuli

The Mandarin variants are not claims about how Mandarin speakers or Chinese users communicate. They are controlled pragmatic surface forms designed to test whether an agent preserves policy boundaries when the same underlying intent is expressed differently.

## 3. No full human annotation yet

Current results include qualitative audit and evaluator false-positive correction, but no formal human annotation study, Cohen's kappa, or native-speaker Mandarin audit. A calibration protocol is in `docs/calibration_protocol.md`.

## 4. Metrics are heuristic

The evaluator is rule-based. It was improved after false-positive analysis but should be treated as a diagnostic tool, not a definitive judge of policy compliance.

## 5. Scenario coverage is limited

Currently covers retail refund and subscription/billing. Other domains would require new policies, rubrics, and safety review.

## 6. Agent baselines are limited

Currently compares two rule-based baselines. Does not yet compare LangGraph, CrewAI, AutoGen, or production Arklex agents.

## 7. Results should be interpreted as diagnostic

The benchmark identifies policy-boundary vulnerabilities and regression risks. It does not certify an agent for production deployment.

Earlier pilot runs used a single seed across repeats, producing identical outputs and zero-width bootstrap intervals. This was fixed by using `seed = 42 + repeat_index`. Older reliability reports under `results/reliability/` predate this fix. Even with per-repeat seeds, repeats should be treated as controlled replicates rather than independent observations.
