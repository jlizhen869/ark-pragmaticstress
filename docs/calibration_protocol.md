# Calibration Protocol

## Status

Pilot protocol. This document describes how Ark-PragmaticStress calibrates rule-based evaluator labels against an external judge or human annotation. It is not yet a full multi-annotator validation study.

## Motivation

The benchmark currently computes automatic labels such as:

- `policy_violation`
- `unauthorized_concession`
- `refund_promised_before_check`
- `admitted_fault_without_evidence`
- `quality_ok`

These labels are useful for scalable evaluation, but they may contain false positives or false negatives. Calibration is required before making strong claims about model behavior.

## Sampling plan

Use a stratified sample of conversations across:

- scenario group
- agent
- persona
- variant
- risk level

Recommended pilot size:

```text
N = 30 conversations
