from ark_pragmaticstress.personas import PERSONA_REGISTRY


def test_personas_generate_non_empty_turns():
    for name, cls in PERSONA_REGISTRY.items():
        persona = cls(variant="en_direct", scenario_id="retail_refund")
        turn = persona.generate_turn([])
        assert turn.text
        assert turn.underlying_intent
        assert persona.check_turn(turn)
