# Directness vs. Language Analysis

One way to check whether language or pragmatic directness is driving
the failure patterns is to re-group the conversations along each axis
and compare.

| Grouping | unauthorized_concession |
|---|---|
| direct (en_direct + mandarin_literal) | 0.250 |
| indirect (en_mitigated + mandarin_pragmatic) | 0.000 |
| english (en_direct + en_mitigated) | 0.125 |
| mandarin (mandarin_literal + mandarin_pragmatic) | 0.125 |

Grouping by language gives the same number for both — 0.125 each.
Grouping by directness gives a clean split — 0.250 vs 0.000.

By agent:
- scaffold_naive: direct=0.500, indirect=0.000
- scaffold_policy_aware: direct=0.000, indirect=0.000

All the failure signal comes from the naive agent on direct-framed
requests. Whether the request was in English or Mandarin didn't matter —
what mattered was how directly the user asked.
