from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

replacements = {
    "openai_agent": "scaffold_policy_aware",
    "openai_naive_agent": "scaffold_naive",
    "OpenAI-based agent baselines": "scaffold LLM agent baselines",
    "OpenAI-based agent baseline": "scaffold LLM agent baseline",
    "OpenAI-based agents": "scaffold LLM agents",
    "OpenAI-based agent": "scaffold LLM agent",
    "regular OpenAI agent": "policy-aware scaffold LLM agent",
}

target_dirs = [
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "results",
]

files = []

for target in target_dirs:
    if target.is_file():
        files.append(target)
    elif target.exists():
        for pattern in ["*.md", "*.csv", "*.json", "*.jsonl", "*.yaml", "*.yml"]:
            files.extend(target.rglob(pattern))

for path in sorted(set(files)):
    text = path.read_text(encoding="utf-8", errors="ignore")
    new_text = text

    for old, new in replacements.items():
        new_text = new_text.replace(old, new)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
