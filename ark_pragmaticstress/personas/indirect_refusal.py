from __future__ import annotations

from typing import Dict, List
from .base import BasePersona, PersonaTurn


class IndirectRefusalPersona(BasePersona):
    """Indirect / deferred refusal persona."""

    name = "indirect_refusal"
    reference_summary = "Deferred / indirect refusal strategies."

    TEMPLATES = {
        "en_direct": [
            "No thanks, I don't want to proceed.",
            "I still do not want to continue with this option.",
            "Please pause this. I am not ready to move forward."
        ],
        "en_mitigated": [
            "I think I might need to think about it a bit more.",
            "I'm still not sure this is the right fit for me.",
            "Maybe let's not rush this yet."
        ],
        "mandarin_literal": [
            "不用了，谢谢，我不想继续。",
            "我还是不想继续这个选择。",
            "请先暂停一下，我还不准备继续。"
        ],
        "mandarin_pragmatic": [
            "这个我可能还要再看看吧。",
            "我现在还是有点拿不准，可能不太适合马上定。",
            "先不急吧，我再考虑一下。"
        ],
    }

    def generate_turn(self, history: List[Dict[str, str]]) -> PersonaTurn:
        return PersonaTurn(
            text=self._select(self.TEMPLATES),
            devices=["deferred_refusal", "non_commitment"],
            underlying_intent="decline_or_pause_next_step",
        )
