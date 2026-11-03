from fuzz_marathon_registration import build_cases, run_fuzz

def test_corpus_covers_all_application_functions():
    names = {name for name, _function, _args in build_cases(25, 1234)}
    assert names == {"entry_fee", "start_wave", "finisher_status"}

def test_results_are_reproducible_for_same_seed():
    first = run_fuzz(30, 99)
    second = run_fuzz(30, 99)
    assert first["total_inputs"] == second["total_inputs"]
    assert first["findings"] == second["findings"]
    assert first["exceptions_by_type"] == second["exceptions_by_type"]

def test_report_contains_exception_and_performance_metrics():
    report = run_fuzz(20, 484)
    assert report["total_inputs"] > 20
    assert set(report["calls_by_function"]) == {"entry_fee", "start_wave", "finisher_status"}
    assert "total_execution_seconds" in report
    assert "average_call_microseconds" in report
    assert "max_call_milliseconds" in report
    assert "exceptions_by_type" in report
    assert isinstance(report["findings"], list)
