from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

from ark_pragmaticstress.agents import AGENT_REGISTRY
from ark_pragmaticstress.evaluation.metrics import score_conversation
from ark_pragmaticstress.personas import PERSONA_REGISTRY


def load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def should_stop(history: List[Dict[str, Any]], max_turns: int) -> bool:
    """Stop after max user-agent exchanges.

    Later versions should use scenario-specific termination conditions.
    """
    user_turns = [t for t in history if t.get("role") == "user"]
    return len(user_turns) >= max_turns


def run_one(
    scenario_id: str,
    scenario: Dict[str, Any],
    persona_name: str,
    variant: str,
    agent_name: str,
    turns: int,
    repeat_index: int = 0,
) -> Dict[str, Any]:
    persona_cls = PERSONA_REGISTRY[persona_name]
    agent_cls = AGENT_REGISTRY[agent_name]

    seed = 42 + repeat_index
    persona = persona_cls(variant=variant, scenario_id=scenario_id, seed=seed)
    agent = agent_cls(scenario=scenario, seed=seed)

    history: List[Dict[str, Any]] = []
    while not should_stop(history, max_turns=turns):
        user_turn = persona.generate_turn(history)
        if not persona.check_turn(user_turn):
            raise ValueError(f"Persona generated invalid turn: {user_turn}")

        history.append(
            {
                "role": "user",
                "text": user_turn.text,
                "devices": user_turn.devices,
                "underlying_intent": user_turn.underlying_intent,
            }
        )

        agent_turn = agent.respond(user_turn.text, history)
        history.append(agent_turn)

    metrics = score_conversation(history=history, scenario=scenario)
    agent_kind = "llm_api" if hasattr(agent, "model") else "rule_based"
    model_id = getattr(agent, "model", "rule_based")

    return {
        "scenario_id": scenario_id,
        "agent": agent_name,
        "agent_kind": agent_kind,
        "model": model_id,
        "persona": persona_name,
        "variant": variant,
        "turns": history,
        "metrics": metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_yaml(config_path)

    out_dir = Path(config.get("output_dir", "results"))
    out_dir.mkdir(parents=True, exist_ok=True)
    conversation_path = out_dir / config.get("conversation_file", "conversations.jsonl")
    metrics_path = out_dir / config.get("metrics_file", "metrics.json")

    records = []
    for scenario_path_str in config["scenarios"]:
        scenario_path = Path(scenario_path_str)
        scenario = load_yaml(scenario_path)
        scenario_id = scenario["id"]

        for agent_name in config["agents"]:
            for persona_name in config["personas"]:
                for variant in config["variants"]:
                    for repeat_index in range(int(config.get("repeats", 1))):
                        records.append(
                            run_one(
                                scenario_id=scenario_id,
                                scenario=scenario,
                                persona_name=persona_name,
                                variant=variant,
                                agent_name=agent_name,
                                turns=int(config.get("turns", 3)),
                                repeat_index=repeat_index,
                            )
                        )

    with conversation_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    aggregate: Dict[str, float] = {}
    by_agent: Dict[str, Dict[str, float]] = {}
    if records:
        keys = records[0]["metrics"].keys()
        for key in keys:
            aggregate[key] = sum(float(r["metrics"][key]) for r in records) / len(
                records
            )

        agents = sorted(set(r["agent"] for r in records))
        for agent in agents:
            agent_records = [r for r in records if r["agent"] == agent]
            by_agent[agent] = {
                key: sum(float(r["metrics"][key]) for r in agent_records)
                / len(agent_records)
                for key in keys
            }

    metrics_path.write_text(
        json.dumps(
            {
                "num_conversations": len(records),
                "aggregate_metrics": aggregate,
                "by_agent": by_agent,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {len(records)} conversations to {conversation_path}")
    print(f"Wrote aggregate metrics to {metrics_path}")


if __name__ == "__main__":
    main()
