# Reviewer Notes

## Current test status

The project installs successfully in editable development mode and the test suite passes.

Command run locally:

```bash
pip install -e ".[dev]" && pytest -q
```

Result:

```text
Successfully installed ark-pragmaticstress-0.1.0
......                                                                   [100%]
6 passed in 0.02s
```

## Notes on reported results

Quantitative result files under `results/reliability/` are retained as pre-fix pilot artifacts. They are explicitly marked with stale-results warnings and should be regenerated before being cited as current findings.
