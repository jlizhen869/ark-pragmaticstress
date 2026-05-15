# Calibration Protocol

Pilot protocol. Not yet a full multi-annotator study.

## Why

The rule-based evaluator may produce false positives. The main risk identified during development: responses containing refusal or verification language were sometimes incorrectly flagged as unauthorized concessions. This was partially fixed in the evaluator, but edge cases remain.

## Plan

Stratified sample across scenario, agent, persona, and variant. Pilot target: N = 30. Full audit would need N >= 100 with at least two annotators and Cohen's kappa per label.

## Current status

Dry-run verified the pipeline schema. Real LLM-judge calibration needs `OPENAI_API_KEY` and `python evaluation/llm_judge.py` without `--dry-run`. Human annotation not yet done.

Mandarin pragmatic variants should eventually be checked by a bilingual reviewer — automated evaluation of indirect Mandarin pressure is the weakest part of the current evaluator.
