# Reviewer Notes

## Current test status

The project installs successfully in editable development mode and the test suite passes.

Command run locally:

~~~bash
pip install -e ".[dev]" && pytest -q
~~~

Result:

~~~text
Successfully installed ark-pragmaticstress-0.1.0
......                                                                   [100%]
6 passed in 0.02s
~~~

## Notes on result files

The current README reports the final 192-conversation LLM evaluation.

Older exploratory reliability files under `results/reliability/` are retained for transparency and are marked as stale pilot artifacts. They should not be cited as the current headline results.

For the current headline numbers, use the README results table and the final LLM evaluation outputs under `results/llm_full/`.
