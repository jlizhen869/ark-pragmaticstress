# Ark-PragmaticStress Project Summary

## Overview

Ark-PragmaticStress is a diagnostic benchmark for evaluating whether customer-facing AI agents preserve policy boundaries when the same underlying user intent is expressed through different pragmatic and multilingual surface forms.

The implemented MVP covers two customer-facing policy-boundary scenario groups: retail refund/exception handling and subscription/billing adjustment. This extends the original retail MVP into a second commercial support setting, while the education/advisory scenario pack remains a planned future extension.

## Motivation

Customer-facing agents are often tested on clean, direct, English-only requests. Real service interactions are more complex: users may soften requests, imply dissatisfaction, appeal to loyalty or authority, ask indirectly for exceptions, or switch between languages and registers.

This creates a policy-boundary risk. An agent may correctly refuse or ask for verification when the user makes a direct request, but make an unauthorized concession when the same intent is expressed indirectly or with pragmatic pressure.

The central research question is:

> Does the same underlying user intent produce different policy behavior when expressed through different pragmatic and multilingual surface forms?

## Method

I built a reproducible evaluation pipeline inspired by ArkSim-style synthetic-user testing.

The pipeline includes:

- YAML-defined scenario policies for retail refund and subscription/billing settings;
- matched pragmatic variants: `en_direct`, `en_mitigated`, `mandarin_literal`, and `mandarin_pragmatic`;
- two OpenAI-based agent baselines: a naive agent and a policy-aware agent;
- simulated conversations across agents, personas, variants, and repeated runs;
- conversation-level metrics for policy violations, unauthorized concessions, unsupported guarantees, clarification-before-action, policy grounding, and helpfulness-boundary tradeoff;
- bootstrap reliability ranking with confidence intervals;
- qualitative high-risk failure examples;
- evaluator false-positive audit and correction.

## Main findings

The policy-aware agent was consistently more reliable than the naive baseline across both scenario groups.

The most salient failure mode was:

`openai_naive_agent × mandarin_pragmatic`

In this condition, the naive agent was more likely to treat indirect, socially softened, or pressure-bearing language as authorization to offer refunds, discounts, exceptions, flexible handling, or other concessions before checking eligibility.

The strongest reliable condition was:

`openai_agent × mandarin_pragmatic`

This indicates that Mandarin pragmatic variants are not inherently unsafe. Rather, they expose whether an agent can maintain policy boundaries when user intent is expressed through controlled pragmatic pressure.

## Contribution

This project contributes a small but complete diagnostic benchmark for agent reliability evaluation. It turns vague concerns such as “the agent may be too easily persuaded” into measurable failure modes, including:

- unauthorized concession rate;
- policy violation rate;
- clarification-before-action rate;
- policy-grounding rate;
- helpfulness-boundary tradeoff.

The benchmark is designed as a measurement instrument, not a cultural or demographic claim. Mandarin variants are controlled experimental stimuli, not claims about how Mandarin speakers or Chinese users behave.

## Current status

Completed:

- retail refund / exception-handling scenario group;
- subscription cancellation / billing-adjustment scenario group;
- naive and policy-aware OpenAI-based agents;
- four matched pragmatic variants;
- risk, quality, and net reliability scoring;
- bootstrap reliability ranking;
- qualitative high-risk examples;
- evaluator false-positive correction;
- project one-pager;
- limitations document;
- reviewer documentation placeholder;
- annotation guidelines.

Not yet completed:

- formal human annotation;
- native-speaker Mandarin audit report;
- education/advisory scenario pack;
- corrective failure-to-repair loop;
- additional framework comparisons;
- optional preference-pair or DPO-style improvement loop.

## Planned next steps

The next immediate step is to prepare the project for research outreach: a concise project summary, resume bullets, and a short email version.

The next technical extension is a controlled failure-to-repair loop. Confirmed high-risk failures can be converted into regression tests, prompt or policy patches, evaluator rubric updates, and optional preference pairs. This extension should be presented as engineering polish on top of the diagnostic benchmark, not as the core research contribution.

## Safe project claim

Ark-PragmaticStress demonstrates a controlled diagnostic benchmark for measuring whether customer-facing agents preserve policy boundaries under pragmatic and multilingual pressure. Across two commercial support scenario groups, the policy-aware agent sharply reduced risk compared with a naive baseline, while Mandarin pragmatic variants consistently exposed unauthorized-concession failures in the naive agent.
