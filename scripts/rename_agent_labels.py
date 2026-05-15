from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

replacements = {
    "ScaffoldNaiveAgent": "ScaffoldNaiveAgent",
    "ScaffoldPolicyAwareAgent": "ScaffoldPolicyAwareAgent",
    "scaffold_naive_agent": "scaffold_naive_agent",
    "scaffold_policy_aware_agent": "scaffold_policy_aware_agent",
    "scaffold LLM agent baselines": "scaffold LLM agent baselines",
    "scaffold LLM agent baseline": "scaffold LLM agent baseline",
    "scaffold LLM agents": "scaffold LLM agents",
    "scaffold LLM agent": "scaffold LLM agent",
    "policy-aware scaffold LLM agent": "policy-aware scaffold LLM agent",
}

target_dirs = [
    ROOT / "README.md",
    ROOT / "REFERENCES.md",
    ROOT / "docs",
    ROOT / "results",
    ROOT / "ark_pragmaticstress",
    ROOT / "scripts",
    ROOT / "tests",
]

files = []
for target in target_dirs:
    if target.is_file():
        files.append(target)
    elif target.exists():
        for pattern in ["*.md", "*.csv", "*.json", "*.jsonl", "*.yaml", "*.yml", "*.py"]:
            files.extend(target.rglob(pattern))

for path in sorted(set(files)):
    if "__pycache__" in path.parts or "egg-info" in str(path):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    new_text = text
    for old, new in replacements.items():
        new_text = new_text.replace(old, new)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
