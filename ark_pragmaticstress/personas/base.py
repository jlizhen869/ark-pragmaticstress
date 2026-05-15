from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PersonaTurn:
    """One generated user turn."""
    text: str
    devices: List[str]
    underlying_intent: str


class BasePersona:
    """Base class for reference-gated synthetic users.

    This MVP uses deterministic templates so the pipeline can run without an LLM.
    Later versions can replace `generate_turn` with ArkSim / LLM-backed generation,
    while keeping the same metadata and runtime checks.
    """

    name: str = "base"
    reference_summary: str = "Must be filled by subclass."

    def __init__(self, variant: str, scenario_id: str):
        self.variant = variant
        self.scenario_id = scenario_id
        self.turn_index = 0

    def generate_turn(self, history: List[Dict[str, str]]) -> PersonaTurn:
        raise NotImplementedError

    def _select(self, templates: Dict[str, List[str]]) -> str:
        options = templates.get(self.variant, templates.get("en_mitigated") or next(iter(templates.values())))
        text = options[min(self.turn_index, len(options) - 1)]
        self.turn_index += 1
        return text

    def check_turn(self, turn: PersonaTurn) -> bool:
        return bool(turn.text.strip()) and bool(turn.underlying_intent.strip())
