# Calibration Report

**Status:** Pilot calibration report. This dry-run report verifies the calibration pipeline structure, but does not contain external judge labels. It is not a final human-validation study.

## Input

- Source: `results/calibration_judge_labels_dry_run.jsonl`
- Rows loaded: 30

## Label agreement summary

| label | n | accuracy | precision | recall | F1 | kappa | TP | TN | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| policy_violation | 0 | NA | NA | NA | NA | NA | 0 | 0 | 0 | 0 |
| unauthorized_concession | 0 | NA | NA | NA | NA | NA | 0 | 0 | 0 | 0 |
| refund_promised_before_check | 0 | NA | NA | NA | NA | NA | 0 | 0 | 0 | 0 |
| admitted_fault_without_evidence | 0 | NA | NA | NA | NA | NA | 0 | 0 | 0 | 0 |
| quality_ok | 0 | NA | NA | NA | NA | NA | 0 | 0 | 0 | 0 |

## Interpretation

Because the current checked-in judge-label file is a dry run, agreement values are reported as `NA`. To compute real agreement, run `evaluation/llm_judge.py` without `--dry-run` after setting `OPENAI_API_KEY`, or replace the judge labels with human annotations.

## Limitations

- This report depends on the quality of the judge labels.
- Dry-run labels are excluded from agreement statistics.
- A full study should use larger stratified samples and multiple human annotators.
- Variant-level and bilingual review are recommended for Mandarin pragmatic cases.
