# Lab 7 — Preliminary Fuzz Run Summary

**Target:** `LAB6/marathon_registration.py`  
**Harness:** `fuzz_marathon_registration.py`  
**Random seed:** `4842026`  
**Randomized iterations:** `1000`

## Baseline run

A local baseline run of the harness against the repository's current Lab 6 application exercised **1,459 total inputs** across all three public functions.

| Metric | Observed result |
|---|---:|
| Total inputs | 1,459 |
| Calls to `entry_fee` | 429 |
| Calls to `start_wave` | 385 |
| Calls to `finisher_status` | 645 |
| `ValueError` validation rejections | 304 |
| Other exceptions (primarily `TypeError`) | 537 |
| Calls over 50 ms | 0 |
| Total measured execution time | 0.002330 seconds |
| Average time per call | 1.597 microseconds |
| Maximum single-call time | 0.169 milliseconds |

## Findings and interpretation

- The application rejects several invalid values through `ValueError`; these are validation outcomes and should be checked against the intended input rules.
- The baseline also produced **537 TypeError exceptions** for malformed types such as `None`, strings, lists and dictionaries passed where numeric or string values are expected. These are potential robustness defects because the functions do not consistently validate input types before comparing or performing arithmetic.
- No call exceeded the harness's 50 ms diagnostic threshold in this run. This is a local micro-benchmark, not a formal performance guarantee; results depend on the machine and environment.

## Reproduction

From the `LAB7` folder:

```powershell
python -m pytest -q
python fuzz_marathon_registration.py --iterations 1000 --seed 4842026
```

The harness writes the detailed, reproducible findings to `FUZZ_TEST_REPORT.json` on the machine where it is run. The detailed JSON report is intentionally generated locally and excluded from Git by `.gitignore`; submit it only if the official Lab 7 instructions request it.

**Status:** Preliminary baseline based on the instructor's email. Update this summary after rerunning on the student's machine and after the formal Lab 7 instructions are released.
