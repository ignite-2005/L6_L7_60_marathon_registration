"""Deterministic, dependency-free fuzz harness for the Lab 7 marathon app."""
from __future__ import annotations
import argparse, json, random, time
from collections import Counter
from pathlib import Path
from typing import Any, Callable
import sys

# The application module is kept in the sibling LAB6 folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "LAB6"))
from marathon_registration import entry_fee, finisher_status, start_wave

SEED = 4842026
SLOW_CALL_SECONDS = 0.05
REPORT_PATH = Path(__file__).with_name("FUZZ_TEST_REPORT.json")
RACES = ["5k", "10k", "half", "full", "", "ULTRA", None, 0, [], {}, "5K"]
AGES = [-10, -1, 0, 1, 11, 12, 17, 18, 64, 65, 120, 10**9, None, "18", 18.5, [], {}]
TIMES = [-10, -1, 0, 1, 67.5, 90, 120, 180, 240, 360, 10**9, None, "120", [], {}]
FLAGS = [True, False, 0, 1, None, "yes", "", [], {}]
MISSED = [-1, 0, 1, 2, None, "0", [], {}]

def pick(rng: random.Random, corpus: list[Any]) -> Any:
    if rng.random() < 0.65:
        return rng.choice(corpus)
    return rng.choice([rng.randint(-10**9, 10**9), rng.uniform(-1000, 1000),
                       "x" * rng.randint(0, 256), None, bool(rng.getrandbits(1))])

def build_cases(iterations: int = 1000, seed: int = SEED):
    rng = random.Random(seed)
    cases = []
    for race in RACES:
        for age in [11, 12, 17, 18, 64, 65, None, "18", []]:
            cases.append(("entry_fee", entry_fee, (race, age, False, False)))
    for best in TIMES:
        for race in ["5k", "full", None, "unknown"]:
            cases.append(("start_wave", start_wave, (best, race)))
    for elapsed in TIMES:
        for race in ["5k", "half", "full", None]:
            for missed in [0, 1, None, "0", []]:
                cases.append(("finisher_status", finisher_status, (elapsed, race, missed)))
    for _ in range(max(0, iterations)):
        choice = rng.randrange(3)
        if choice == 0:
            args = (pick(rng, RACES), pick(rng, AGES), pick(rng, FLAGS), pick(rng, FLAGS))
            cases.append(("entry_fee", entry_fee, args))
        elif choice == 1:
            cases.append(("start_wave", start_wave, (pick(rng, TIMES), pick(rng, RACES))))
        else:
            cases.append(("finisher_status", finisher_status,
                          (pick(rng, TIMES), pick(rng, RACES), pick(rng, MISSED))))
    return cases

def run_fuzz(iterations: int = 1000, seed: int = SEED):
    cases = build_cases(iterations, seed)
    findings, exception_counts, function_counts = [], Counter(), Counter()
    slow_calls, elapsed_total, max_call = 0, 0.0, 0.0
    for name, function, args in cases:
        function_counts[name] += 1
        started = time.perf_counter()
        try:
            function(*args)
        except Exception as exc:
            exception_counts[type(exc).__name__] += 1
            findings.append({"function": name, "input": repr(args),
                             "exception": type(exc).__name__, "message": str(exc)[:300]})
        finally:
            duration = time.perf_counter() - started
            elapsed_total += duration
            max_call = max(max_call, duration)
            if duration > SLOW_CALL_SECONDS:
                slow_calls += 1
    return {
        "tool": "Python standard-library deterministic fuzz harness",
        "seed": seed, "random_iterations": iterations, "total_inputs": len(cases),
        "calls_by_function": dict(function_counts),
        "exceptions_by_type": dict(exception_counts),
        "exception_findings": len(findings),
        "expected_validation_rejections": sum(1 for item in findings if item["exception"] == "ValueError"),
        "unexpected_exception_findings": sum(1 for item in findings if item["exception"] != "ValueError"),
        "slow_calls_over_50ms": slow_calls,
        "total_execution_seconds": round(elapsed_total, 6),
        "average_call_microseconds": round(elapsed_total / len(cases) * 1_000_000, 3),
        "max_call_milliseconds": round(max_call * 1000, 3),
        "findings": findings,
        "interpretation": ("Exceptions are captured for review, not automatically labelled defects. "
                           "A documented ValueError may be expected; unexpected exceptions need review.")
    }

def main():
    parser = argparse.ArgumentParser(description="Fuzz test Marathon Registration.")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    if args.iterations < 0:
        parser.error("--iterations must be non-negative")
    report = run_fuzz(args.iterations, args.seed)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Fuzz testing completed: {report['total_inputs']} inputs")
    print(f"Exceptions captured: {report['exception_findings']}")
    print(f"Validation rejections (ValueError): {report['expected_validation_rejections']}")
    print(f"Unexpected exceptions: {report['unexpected_exception_findings']}")
    print(f"Slow calls (>50 ms): {report['slow_calls_over_50ms']}")
    print(f"Total execution: {report['total_execution_seconds']} seconds")
    print(f"Report saved to: {REPORT_PATH}")
    if report["exception_findings"]:
        print("Review FUZZ_TEST_REPORT.json for captured inputs and exceptions.")

if __name__ == "__main__":
    main()
