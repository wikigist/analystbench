import benchmark_reporting


def test_report_result_prints_and_saves(monkeypatch, capsys):
    saved_results = []

    def fake_save_result(case_id, passed, run_id=None):
        saved_results.append((case_id, passed, run_id))

    monkeypatch.setattr(
        benchmark_reporting,
        "save_result",
        fake_save_result,
    )

    benchmark_reporting.report_result(
        "Q001", 7, 7, True, run_id="run-001"
    )

    benchmark_reporting.report_result(
        "Q002", 4, 3, False, run_id="run-001"
    )

    output = capsys.readouterr().out

    assert "Q001" in output
    assert "PASS" in output
    assert "Q002" in output
    assert "FAIL" in output

    assert saved_results == [
        ("Q001", True, "run-001"),
        ("Q002", False, "run-001"),
    ]