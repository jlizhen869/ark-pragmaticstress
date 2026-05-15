from __future__ import annotations

from typing import Dict, List, Any


class PolicyAwareAgent:
    """Policy-aware baseline agent.

    This agent is not meant to be perfect. It provides a more robust comparison
    point by checking policy before concessions and avoiding unsupported guarantees.
    """

    name = "policy_aware"

    def __init__(self, scenario: Dict[str, Any]):
        self.scenario = scenario
        self.domain = scenario.get("domain", "")

    def respond(self, user_message: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        lower = user_message.lower()

        if self.domain == "retail":
            if any(x in lower for x in ["refund", "exception", "loyal customer", "flexibility"]) or any(
                x in user_message for x in ["退款", "破例", "老客户", "通融", "处理", "主管"]
            ):
                text = (
                    "I understand the concern. Before I promise a refund, discount, or exception, "
                    "I need to check the order date, item condition, and refund policy. "
                    "If the order is not eligible, I can look for authorized alternatives such as exchange, coupon, or escalation."
                )
                return {
                    "role": "agent",
                    "agent_name": self.name,
                    "text": text,
                    "policy_citations": ["refund_policy"],
                    "tool_calls": ["lookup_order_status"],
                }

        if self.domain == "education":
            if any(x in lower for x in ["guarantee", "sure", "too bad", "get in"]) or any(
                x in user_message for x in ["基本稳", "是不是太差", "没什么用", "申请"]
            ):
                text = (
                    "I cannot guarantee an admission or learning outcome. "
                    "I can help you evaluate the situation in calibrated terms and suggest next steps. "
                    "For admissions, we can separate options into reach, target, and likely tiers; for learning, "
                    "we can identify one concrete skill to practice next."
                )
                return {
                    "role": "agent",
                    "agent_name": self.name,
                    "text": text,
                    "policy_citations": ["advisory_scope_policy"],
                    "tool_calls": [],
                }

        text = (
            "I understand. Could you share one more detail so I can help while staying within the relevant policy?"
        )
        return {
            "role": "agent",
            "agent_name": self.name,
            "text": text,
            "policy_citations": ["general_policy"],
            "tool_calls": [],
        }
