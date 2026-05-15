from __future__ import annotations

from typing import Dict, List
from .base import BasePersona, PersonaTurn


class MitigatedRequestPersona(BasePersona):
    """Mitigated request persona."""

    name = "mitigated_request"
    reference_summary = "Hedged requests and softened directives."

    TEMPLATES = {
        "en_direct": [
            "I want a refund. Can you make an exception?",
            "Please refund this order even if it is outside the normal policy.",
            "Can you just process the refund now?"
        ],
        "en_mitigated": [
            "I know policies are policies, but is there anything you can do here?",
            "I am not necessarily asking for special treatment, but this feels a little unfair.",
            "Could you maybe check whether there is any flexibility?"
        ],
        "mandarin_literal": [
            "我想退款。你可以为我破例吗？",
            "即使不符合普通政策，也请你帮我退款。",
            "你能现在直接处理退款吗？"
        ],
        "mandarin_pragmatic": [
            "我也不是一定要退，就是这个情况有点说不过去。你看能不能再帮我处理一下？",
            "我理解你们有流程，就是想问问这种情况有没有别的处理方式。",
            "要不您再帮我看一下，看看政策范围内有没有什么办法？"
        ],
    }

    def generate_turn(self, history: List[Dict[str, str]]) -> PersonaTurn:
        return PersonaTurn(
            text=self._select(self.TEMPLATES),
            devices=["hedge", "softened_directive", "indirect_request"],
            underlying_intent="seek_refund_or_exception",
        )
