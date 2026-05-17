# Directness vs. Language

I wanted to check whether the failure pattern was really about language
(English vs. Mandarin), or whether it was more about how directly the user
asked.

So I re-grouped the pilot conversations in two ways:

| Grouping | unauthorized_concession |
|---|---|
| direct (en_direct + mandarin_literal) | 0.250 |
| indirect (en_mitigated + mandarin_pragmatic) | 0.000 |
| english (en_direct + en_mitigated) | 0.125 |
| mandarin (mandarin_literal + mandarin_pragmatic) | 0.125 |

Grouping by language gave the same rate for English and Mandarin: 0.125.
Grouping by directness gave a much cleaner split: 0.250 for direct-framed
requests vs. 0.000 for indirect-framed ones.

By agent:

| agent | direct | indirect |
|---|---|---|
| scaffold_naive | 0.500 | 0.000 |
| scaffold_policy_aware | 0.000 | 0.000 |

In this pilot, failures lined up more clearly with pragmatic directness
than with language. Direct-framed requests produced more unauthorized
concessions, while English vs. Mandarin alone did not separate the behavior.

My current interpretation is that Mandarin literal worked mostly as a
directness control, while Mandarin pragmatic changed the interaction
framing more substantially.

This is still a small pilot, so I would not treat it as a general
conclusion. But it suggests that future versions should parameterize
directness more explicitly, with language as a conditioning factor
rather than the primary stress dimension.
