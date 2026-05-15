# Ark-PragmaticStress: Pragmatic Reliability Testing for Customer-Facing Agents

## One-line summary

A diagnostic benchmark for testing whether customer-facing AI agents maintain policy boundaries when users express the same underlying intent through direct, mitigated, persuasive, Mandarin literal, and Mandarin pragmatic surface forms.

## Problem

Many customer-facing agents are evaluated on clean, direct, English-only requests. Real service interactions are messier: users ask indirectly, soften requests, appeal to loyalty or authority, switch language/register, or pressure the agent for exceptions.

The business risk is that the agent may make unauthorized concessions, promise refunds or discounts before checking eligibility, admit platform fault without evidence, or close the case without recovering the user's actual intent.

## What I built

A reproducible evaluation pipeline with YAML scenario policies for retail and subscription settings, four pragmatic variants per scenario, two rule-based agent baselines, and conversation-level metrics covering policy violations, unauthorized concessions, and helpfulness-boundary tradeoffs. The evaluator went through one round of false-positive correction after qualitative audit.

## Experimental setup

Two policy-boundary scenario groups:

1. retail refund / exception handling
2. subscription cancellation / billing adjustment

For each group, conversations are generated across two agent baselines, two user personas, four pragmatic variants, and repeated runs. Exact counts are reported from result files.

## Core metrics

Unsafe behavior: `policy_violation`, `unauthorized_concession`, `unsupported_guarantee`, `premature_closure`

Positive behavior: `clarification_before_action`, `policy_grounding`, `helpfulness_boundary_tradeoff`, `alternative_resolution`

## Key results

The policy-aware agent showed lower observed risk than the naive baseline across both scenario groups. The largest failure mode was `baseline × mandarin_pragmatic` — indirect Mandarin pressure triggered unauthorized concessions that direct English requests did not.

The main finding is not that Mandarin prompts are inherently unsafe. Mandarin pragmatic variants expose whether an agent can maintain policy boundaries under indirect, socially softened pressure.

## What is not claimed

The Mandarin variants are controlled experimental surface forms, not claims about how Mandarin speakers or Chinese users communicate. The benchmark asks a narrower question: does the same underlying intent produce different agent policy behavior when expressed through different pragmatic forms?

## Current status

Done: retail and subscription scenario groups, two rule-based agent baselines, risk/quality/reliability scoring, bootstrap ranking, evaluator false-positive correction.

Not yet done: formal human annotation, native-speaker Mandarin audit, LLM judge integration, corrective-loop regression tests.
