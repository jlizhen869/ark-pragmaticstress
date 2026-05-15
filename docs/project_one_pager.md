# Ark-PragmaticStress: Pragmatic Reliability Testing for Customer-Facing Agents

## One-line summary

Ark-PragmaticStress is a diagnostic benchmark for testing whether customer-facing AI agents maintain policy boundaries when users express the same underlying intent through direct, mitigated, persuasive, Mandarin literal, and Mandarin pragmatic surface forms.

## Problem

Many customer-facing agents are evaluated on clean, direct, English-only requests. Real service interactions are messier: users ask indirectly, soften requests, appeal to loyalty or authority, switch language/register, or pressure the agent for exceptions.

The business risk is that the agent may make unauthorized concessions, promise refunds or discounts before checking eligibility, admit platform fault without evidence, or close the case without recovering the user’s actual intent.

## What I built

I built a reproducible pragmatic-stress evaluation pipeline on top of an ArkSim-style synthetic-user setup.

The system includes:

- YAML scenario policies for retail refund and subscription/billing settings;
- matched pragmatic variants: `en_direct`, `en_mitigated`, `mandarin_literal`, and `mandarin_pragmatic`;
- two agent baselines: a naive agent and a policy-aware agent;
- conversation-level metrics for policy violations, unauthorized concessions, clarification, policy grounding, and helpfulness-boundary tradeoff;
- bootstrap reliability ranking with confidence intervals;
- qualitative high-risk failure examples;
- evaluator false-positive audit and correction.

## Experimental setup

The benchmark currently evaluates two policy-boundary scenario groups:

1. retail refund / exception handling;
2. subscription cancellation / billing adjustment.

For each scenario group, the pipeline generates matched conversations across:

- policy-boundary scenarios;
- two agent baselines: a naive agent and a policy-aware agent;
- two user personas;
- four pragmatic variants: `en_direct`, `en_mitigated`, `mandarin_literal`, and `mandarin_pragmatic`;
- repeated runs for reliability analysis.

The current diagnostic run covers simulated conversations across the two scenario groups. Exact run counts are reported from generated result files rather than hard-coded in the project description.

## Core metrics

Unsafe behavior metrics:

- `policy_violation`
- `unauthorized_concession`
- `unsupported_guarantee`
- `premature_closure`

Positive behavior metrics:

- `clarification_before_action`
- `policy_grounding`
- `helpfulness_boundary_tradeoff`
- `alternative_resolution`

Composite scores:

- `risk_score`
- `quality_score`
- `net_reliability_score`

## Key results

At the agent level, the policy-aware agent is consistently more reliable than the naive baseline.

The largest confirmed failure mode is:

`openai_naive_agent × mandarin_pragmatic`

The strongest reliable variant is:

`openai_agent × mandarin_pragmatic`

The main finding is not that Mandarin prompts are inherently unsafe. Rather, Mandarin pragmatic variants expose whether an agent can maintain policy boundaries under indirect, socially softened, or pressure-bearing language.

## Business value

For an enterprise agent platform, this benchmark can support:

1. release gating before deployment;
2. regression testing after prompt, policy, or model changes;
3. multilingual support-quality audits;
4. policy-boundary monitoring for customer-support agents;
5. failure-to-repair workflows.

## What is not claimed

This benchmark is not a claim about how Chinese users or Mandarin speakers behave. The Mandarin variants are controlled experimental surface forms, not demographic descriptions.

The benchmark asks a narrower measurement question:

Does the same underlying intent produce different agent policy behavior when expressed through different pragmatic and multilingual forms?

## Current status

Completed:

- retail scenario group;
- subscription/billing scenario group;
- two OpenAI-based agent baselines;
- risk/quality/net reliability scoring;
- bootstrap ranking;
- qualitative failure examples;
- evaluator false-positive correction;
- README results section;
- committed cross-scenario reliability analysis.

Not yet completed:

- formal human annotation;
- native-speaker Mandarin audit report;
- reviewer metadata documentation;
- corrective-loop regression tests;
- optional preference-pair or DPO extension.

## Safe project claim

Ark-PragmaticStress demonstrates a controlled diagnostic benchmark for measuring whether customer-facing agents preserve policy boundaries under pragmatic and multilingual pressure. Across simulated conversations, the policy-aware agent sharply reduced risk compared with a naive baseline, while Mandarin pragmatic variants consistently exposed unauthorized-concession failures in the naive agent.ø

