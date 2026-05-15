from __future__ import annotations

import random
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

    This MVP uses seeded template sampling so the pipeline can run without an LLM.
    Later versions can replace `generate_turn` with ArkSim / LLM-backed generation,
    while keeping the same metadata and runtime checks.
    """

    name: str = "base"
    reference_summary: str = "Must be filled by subclass."

    def __init__(self, variant: str, scenario_id: str, seed: int = 42):
        self.variant = variant
        self.scenario_id = scenario_id
        self.turn_index = 0
        self.seed = seed
        self._rng = random.Random(seed)

    def generate_turn(self, history: List[Dict[str, str]]) -> PersonaTurn:
        raise NotImplementedError

    def _select(self, templates: Dict[str, List[str]]) -> str:
        options = templates.get(self.variant, templates.get("en_mitigated") or next(iter(templates.values())))
        self.turn_index += 1
        return self._rng.choice(options)

    def check_turn(self, turn: PersonaTurn) -> bool:
        return bool(turn.text.strip()) and bool(turn.underlying_intent.strip())
