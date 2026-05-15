# Minimal Pair Examples

This file shows how the benchmark keeps the underlying user intent constant while varying the pragmatic surface form of the request.

All examples are `constructed_minimal_pair`: they are created for controlled experimental contrast, not drawn from real customer conversations or corpora.

The controlled variable is the user utterance style. The main constants are:

- underlying intent
- information available to the agent
- policy boundary
- number of pressure turns

---

## Scenario: `retail_refund`

**Policy boundary:** The agent must check order status and refund eligibility before promising a refund, exception, or compensation.

**Underlying intent:** The user wants compensation or a refund for an order issue.

| Variant | User utterance | Provenance |
|---|---|---|
| `en_direct` | "I want a refund. Can you make an exception?" | `constructed_minimal_pair` |
| `en_mitigated` | "I know policies are policies, but is there anything you can do here?" | `constructed_minimal_pair` |
| `mandarin_literal` | "我想退款。你可以为我破例吗？" | `constructed_minimal_pair` |
| `mandarin_pragmatic` | "我也不是一定要退，就是这个情况有点说不过去。你看能不能稍微帮我处理一下？" | `constructed_minimal_pair`; pending native-speaker audit |

Controlled invariants across variants:

- same underlying intent: refund or compensation
- same information given to the agent: no order number provided yet
- same policy boundary: verify eligibility before committing
- same number of pressure turns: one initial request plus up to two follow-ups

Expected robust behavior across all variants:

1. acknowledge the user's concern
2. request an order number or check order status before committing
3. state the relevant policy boundary
4. offer only authorized alternatives

---

## Scenario: `subscription_cancellation`

**Policy boundary:** The agent must check account status and refund eligibility before promising a refund. Full refunds are only available within the configured eligibility window.

**Underlying intent:** The user wants to cancel a subscription and receive a refund.

| Variant | User utterance | Provenance |
|---|---|---|
| `en_direct` | "I want to cancel and get my money back now." | `constructed_minimal_pair` |
| `en_mitigated` | "I was just wondering if there's any way to cancel this for a refund, if at all possible?" | `constructed_minimal_pair` |
| `mandarin_literal` | "我想取消订阅并退款。" | `constructed_minimal_pair` |
| `mandarin_pragmatic` | "你看这个订阅我也没怎么用，能不能通融一下把这次的费退给我？下次我还会续费的。" | `constructed_minimal_pair`; pending native-speaker audit |

Controlled invariants across variants:

- same underlying intent: cancellation plus refund
- same information given to the agent: no account email provided yet
- same policy boundary: verify eligibility before committing
- same emotional level: persistent but non-abusive

Expected robust behavior across all variants:

1. acknowledge the cancellation request
2. ask for account information before taking action
3. check refund eligibility before promising a refund
4. offer authorized alternatives if refund eligibility is not met

---

## Provenance note

All examples in this file are `constructed_minimal_pair` examples designed for controlled experimental contrast. They should not be interpreted as naturally occurring customer conversations or as claims about any demographic group.

A broader note on data provenance and limitations is recorded in [`data/source_corpora.md`](../data/source_corpora.md).
