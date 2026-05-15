# References

This file documents the literature grounding for Ark-PragmaticStress. The benchmark uses pragmatic, cross-linguistic, and persuasion-oriented user pressure patterns to test whether customer-facing agents maintain policy boundaries.

## 1. Pragmatics, politeness, and indirect speech acts

- Austin, J. L. (1962). *How to Do Things with Words*. Oxford University Press.
- Searle, J. R. (1975). Indirect speech acts. In *Syntax and Semantics 3: Speech Acts*.
- Grice, H. P. (1975). Logic and conversation. In *Syntax and Semantics 3: Speech Acts*.
- Brown, P., & Levinson, S. C. (1987). *Politeness: Some Universals in Language Usage*. Cambridge University Press.
- Blum-Kulka, S., House, J., & Kasper, G. (1989). *Cross-Cultural Pragmatics: Requests and Apologies*. Ablex.

## 2. Persona categories used in this benchmark

### `indirect_refusal`

This persona targets indirect refusal, reluctance, hesitation, and implied negative responses. The goal is to test whether the agent can infer user intent without overreacting or violating policy.

Relevant grounding:

- Searle (1975) on indirect speech acts.
- Brown & Levinson (1987) on politeness and face-saving.
- Blum-Kulka et al. (1989) on cross-cultural pragmatic realization.

### `mitigated_request`

This persona targets softened requests, hedges, indirect asks, and face-saving pressure. The goal is to test whether the agent maintains policy boundaries when the user frames a request as reasonable, polite, or low-risk.

Relevant grounding:

- Brown & Levinson (1987) on mitigation and politeness.
- Blum-Kulka et al. (1989) on request strategies across languages and cultures.
- Grice (1975) on conversational implicature.

### `persuasion_appeal`

This persona targets loyalty appeals, urgency framing, authority pressure, emotional pressure, and repeated attempts to obtain exceptions. The goal is to test whether the agent grants unauthorized concessions when pressured.

Relevant grounding:

- Cialdini, R. B. (2009). *Influence: Science and Practice*. Pearson.
- Brown & Levinson (1987) on face-threatening acts and mitigation.
- Dialogue safety and red-teaming work listed below.

## 3. Dialogue systems, agent evaluation, and safety

- Dinan, E., et al. (2019). Build it Break it Fix it for Dialogue Safety: Robustness from Adversarial Human Attack. EMNLP.
- Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS Datasets and Benchmarks.
- Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv.
- Perez, E., et al. (2022). Red Teaming Language Models with Language Models. EMNLP.
- Ganguli, D., et al. (2022). Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned. arXiv.

## 4. Reference map

| Benchmark component | Literature grounding | Why it matters |
|---|---|---|
| Indirect refusals | Indirect speech acts, implicature, politeness | Users often imply constraints rather than stating them directly. |
| Mitigated requests | Politeness theory, request mitigation | A request can be pragmatically forceful even when phrased politely. |
| Persuasion appeals | Influence, pressure, face-work | Agents may comply with unauthorized exceptions when users apply social pressure. |
| Mandarin pragmatic variants | Cross-cultural pragmatics | Literal translation and pragmatic realization can produce different interaction pressure. |
| Policy-boundary evaluation | Dialogue safety and red-teaming | The benchmark tests whether agents maintain constraints under adversarial or subtle pressure. |

## 5. Scope note

These references ground the design of the stress-test categories. They do not imply that the current pilot results are final claims about production LLM behavior. Current results should be read as pilot evaluation outputs, with calibration and human-audit procedures documented separately.

## Persuasion and Pragmatics

- Wang, X., Shi, W., Kim, R., Oh, Y., Yang, S., Zhang, J., & Yu, Z. (2019). Persuasion for good: Towards a personalized persuasive dialogue system. Proceedings of ACL 2019. Used here to motivate the `persuasion_appeal` persona's loyalty, authority, and reciprocity pressure devices.
- Tian, Y., Shi, W., Li, C., & Yu, Z. (2020). Understanding user resistance strategies in persuasive conversations. Findings of EMNLP 2020. Used here to motivate indirect requests, mitigation, and resistance-style pragmatic pressure in dialogue.
