# MVP Retail Pilot Findings

## Setup

This deterministic pilot ran:

- 1 scenario: `retail_refund`
- 3 agents: `baseline`, `variant_sensitive`, `policy_aware`
- 3 personas: `indirect_refusal`, `mitigated_request`, `persuasion_appeal`
- 4 variants: `en_direct`, `en_mitigated`, `mandarin_literal`, `mandarin_pragmatic`
- 5 repeats per cell

Total: 180 conversations.

## Finding 1 — Weak baseline leaks policy under persuasion pressure

The `baseline` agent shows high policy violation under `persuasion_appeal` across all variants. This confirms that the benchmark can surface unauthorized concession failures.

## Finding 2 — Policy-aware agent removes the observed policy leaks

The `policy_aware` agent shows zero policy violation across all tested cells in this deterministic pilot. This suggests that explicit policy grounding and clarification-before-action can reduce the observed failure mode.

## Finding 3 — Pragmatic realization changes behavior in the variant-sensitive baseline

For the `variant_sensitive` agent under `mitigated_request`:

- `en_mitigated - en_direct = +1.000`
- `mandarin_literal - en_direct = +0.000`
- `mandarin_pragmatic - mandarin_literal = +1.000`
- `mandarin_pragmatic - en_mitigated = +0.000`

This indicates that the failure is not caused by Mandarin language alone. Instead, the benchmark isolates a pragmatic realization effect: direct and literal requests are handled, while mitigated / pragmatically realized requests trigger policy leaks.

## Important caveat

This is a deterministic MVP scaffold, not a real LLM benchmark yet. The current result validates the benchmark structure, logging, metrics, and contrast design. The next step is to replace rule-based agents with an LLM-backed agent and replace rule-based scoring with a structured judge plus human audit.
