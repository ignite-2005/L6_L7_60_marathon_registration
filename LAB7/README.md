# Lab 7 — Fuzz Testing: Marathon Registration

This folder extends the same Marathon Registration problem used in Lab 6. It does not replace or modify Lab 6 files.

## Objective
Exercise the application functions with malformed, unexpected, boundary and randomized inputs. Record exceptions and execution-time measurements for review.

## Files
- `fuzz_marathon_registration.py` — deterministic fuzz harness using only the Python standard library.
- `test_fuzz_marathon_registration.py` — pytest tests for the harness.
- `FUZZ_TEST_REPORT.json` — generated findings and performance measurements.

The harness targets `entry_fee`, `start_wave` and `finisher_status` from `LAB6/marathon_registration.py`.

## Run
From this LAB7 directory:

```powershell
python -m pip install pytest
python -m pytest -q
python fuzz_marathon_registration.py --iterations 1000
```

The default seed is 4842026, so the generated inputs are reproducible. To change the sequence, use `--iterations 5000 --seed 2026`.

The JSON report records inputs, calls per function, exception types and inputs, and total, average and maximum execution time. Calls over 50 ms are counted as slow; this is a diagnostic threshold, not a formal performance SLA.

## Interpreting findings
The current application intentionally raises some ValueErrors for invalid values. The harness captures exceptions rather than treating every exception as a harness failure. Review each finding: a documented validation exception may be expected, while an unexpected TypeError or other unhandled exception can indicate missing validation. Timing varies by machine.

## Scope
This preliminary implementation is based on the instructor's email describing fuzz testing with invalid and malformed data on the same Lab 6 problem. Update it if the formal Lab 7 handout specifies additional requirements.
