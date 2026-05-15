# Limitations

## 1. Simulated conversations, not real users

The current benchmark uses synthetic users and simulated conversations. The results measure agent behavior under controlled test stimuli, not real-world customer behavior.

## 2. Mandarin variants are controlled stimuli

The Mandarin variants are not claims about how all Mandarin speakers, Chinese users, or any demographic group communicates. They are controlled pragmatic surface forms designed to test whether an agent preserves policy boundaries when the same underlying intent is expressed differently.

## 3. No full human annotation yet

The current results include qualitative audit and evaluator false-positive correction, but do not yet include a formal human annotation study, Cohen’s kappa, or a full Mandarin native-speaker audit report.

## 4. Metrics are heuristic

The evaluator is rule-based and heuristic. It was improved after false-positive analysis, but it should still be treated as a diagnostic tool rather than a definitive judge of policy compliance.

## 5. Scenario coverage is limited

The current implementation covers retail refund/exception handling and subscription/billing adjustment. Other domains, such as education/advisory or healthcare-like support, would require new policies, rubrics, and stronger safety review.

## 6. Agent baselines are limited

The benchmark currently compares a naive OpenAI-based agent and a policy-aware OpenAI-based agent. It does not yet compare multiple agent frameworks such as LangGraph, CrewAI, AutoGen, or production Arklex agents.

## 7. Results should be interpreted as diagnostic

The benchmark is best understood as a stress-test and release-gating tool. It identifies policy-boundary vulnerabilities and regression risks; it does not claim to fully certify an agent for production deployment.
