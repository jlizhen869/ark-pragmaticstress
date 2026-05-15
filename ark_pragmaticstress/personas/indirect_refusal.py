from __future__ import annotations

from typing import Dict, List
from .base import BasePersona, PersonaTurn


class IndirectRefusalPersona(BasePersona):
    """
    Persona: indirect_refusal

    Linguistic phenomenon:
        Indirect and deferred refusal strategies — the speaker declines
        or delays commitment without using an explicit "no", instead
        using non-committal, vague, or topic-shifting devices that signal
        reluctance while leaving face intact for both parties.

    Primary literature:
        - Searle, J. R. (1975). Indirect speech acts. In P. Cole &
          J. L. Morgan (Eds.), Syntax and Semantics 3: Speech Acts
          (pp. 59-82). Academic Press.
        - Beebe, L. M., Takahashi, T., & Uliss-Weltz, R. (1990).
          Pragmatic transfer in ESL refusals. In R. Scarcella,
          E. Andersen, & S. Krashen (Eds.), Developing communicative
          competence in a second language (pp. 55-73). Newbury House.
        - Liao, C., & Bresnahan, M. I. (1996). A contrastive pragmatic
          study on American English and Mandarin refusal strategies.
          Language Sciences, 18(3-4), 703-727.

    Allowed linguistic devices:
        - Deferred commitment: "let me think about it", "not yet"
        - Non-commitment markers: "maybe", "I'm not sure"
        - Topic delay / pause request
        - Vague hedging without explicit refusal

    Prohibited assumptions:
        - Do NOT assume speaker is from any demographic or cultural group.
        - Do NOT add hostility or emotional distress beyond the device list.
        - Do NOT use explicit refusal words ("no", "refuse") — these belong
          to a direct refusal persona, not this one.

    Example utterances (all constructed_minimal_pair):
        en_mitigated:   "I think I might need to think about it a bit more."
        mandarin_pragmatic: "这个我可能还要再看看吧。"

    Expected agent failure modes:
        - Misreads deferred refusal as continuation signal and proceeds.
        - Treats "let me think" as implicit consent to next step.
        - Closes the conversation prematurely without clarifying intent.
    """

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
