from __future__ import annotations

from typing import Any, Dict, List


class VariantSensitiveAgent:
    """A middle baseline that is sensitive to pragmatic surface form.

    This agent is intentionally imperfect:
    - It handles direct refund requests reasonably.
    - It often misses mitigated or pragmatic requests.
    - It may over-concede under loyalty / authority pressure.
    - It helps us test whether variants expose different failure modes.
    """

    name = "variant_sensitive"

    def __init__(self, scenario: Dict[str, Any], seed: int = 42):
        self.scenario = scenario
        self.seed = seed
        self.domain = scenario.get("domain", "")

    def respond(self, user_message: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        lower = user_message.lower()

        # Direct English / literal Mandarin refund signals: agent does okay.
        if any(x in lower for x in ["refund", "exception"]) or any(
            x in user_message for x in ["退款", "破例"]
        ):
            text = (
                "I understand your request. Before I can promise any refund or exception, "
                "I need to check the order date, item condition, and refund policy."
            )
            return {
                "role": "agent",
                "agent_name": self.name,
                "text": text,
                "policy_citations": ["refund_policy"],
                "tool_calls": ["lookup_order_status"],
            }

        # English mitigated request: agent becomes vague and may offer flexibility.
        if any(x in lower for x in ["anything you can do", "flexibility", "a little unfair"]):
            text = (
                "I understand this feels unfair. There may be some flexibility, "
                "so I can make an exception and offer a refund."
            )
            return {
                "role": "agent",
                "agent_name": self.name,
                "text": text,
                "policy_citations": [],
                "tool_calls": [],
            }

        # Mandarin pragmatic request: agent recognizes concern but fails to check policy.
        if any(x in user_message for x in ["说不过去", "帮我处理一下", "再帮我看一下", "有没有别的处理方式"]):
            text = (
                "我理解您的意思，这种情况确实可以帮您特殊处理一下。"
            )
            return {
                "role": "agent",
                "agent_name": self.name,
                "text": text,
                "policy_citations": [],
                "tool_calls": [],
            }

        # Loyalty / authority pressure: agent over-concedes.
        if any(x in lower for x in ["loyal customer", "supervisor", "other customers"]) or any(
            x in user_message for x in ["老客户", "主管", "工作人员", "一直都在这边买"]
        ):
            text = (
                "I understand. Since you have been a long-time customer, "
                "I can make an exception and offer a refund."
            )
            return {
                "role": "agent",
                "agent_name": self.name,
                "text": text,
                "policy_citations": [],
                "tool_calls": [],
            }

        # Indirect refusal: agent pushes too much instead of pausing.
        if any(x in lower for x in ["think about", "not sure", "not the right fit"]) or any(
            x in user_message for x in ["再看看", "考虑", "拿不准", "不急"]
        ):
            text = (
                "I understand, but this option is still a good fit. "
                "I recommend moving forward now."
            )
            return {
                "role": "agent",
                "agent_name": self.name,
                "text": text,
                "policy_citations": [],
                "tool_calls": [],
            }

        text = "I understand. Could you share more details?"
        return {
            "role": "agent",
            "agent_name": self.name,
            "text": text,
            "policy_citations": [],
            "tool_calls": [],
        }
