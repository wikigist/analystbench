from result_history import save_result
from run_report import summarize_history


def test_summarize_history_counts_passes_and_failures(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result("Q001", True, file_path)
    save_result("Q002", False, file_path)
    save_result("Q003", True, file_path)

    summary = summarize_history(file_path)

    assert summary["total"] == 3
    assert summary["passed"] == 2
    assert summary["failed"] == 1


def test_summarize_empty_history(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"
    file_path.touch()

    summary = summarize_history(file_path)

    assert summary["total"] == 0
    assert summary["passed"] == 0
    assert summary["failed"] == 0
    assert summary["pass_rate_pct"] == 0.0


def test_summarize_history_filters_by_run_id(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result("Q001", True, file_path, run_id="run-001")
    save_result("Q002", False, file_path, run_id="run-001")

    save_result("Q001", True, file_path, run_id="run-002")
    save_result("Q002", True, file_path, run_id="run-002")

    summary = summarize_history(file_path, run_id="run-002")

    assert summary["total"] == 2
    assert summary["passed"] == 2
    assert summary["failed"] == 0



def test_summarize_history_calculates_run_pass_rate(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result("Q001", True, file_path, run_id="run-001")
    save_result("Q002", False, file_path, run_id="run-001")
    save_result("Q003", True, file_path, run_id="run-002")

    summary = summarize_history(file_path, run_id="run-001")

    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["pass_rate_pct"] == 50.0


def test_summarize_history_filters_evaluation_type(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result("Q001", True, file_path, evaluation_type="reference")
    save_result("Q001", False, file_path, evaluation_type="model")
    save_result("Q002", True, file_path, evaluation_type="model")

    summary = summarize_history(file_path, evaluation_type="model")

    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["pass_rate_pct"] == 50.0



def test_summarize_history_filters_run_and_type(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result("Q001", True, file_path, run_id="run-001", evaluation_type="model")
    save_result("Q002", False, file_path, run_id="run-001", evaluation_type="model")

    save_result("Q003", True, file_path, run_id="run-001", evaluation_type="reference")
    save_result("Q004", True, file_path, run_id="run-002", evaluation_type="model")

    summary = summarize_history(
        file_path,
        run_id="run-001",
        evaluation_type="model",
    )

    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["pass_rate_pct"] == 50.0



def test_summarize_history_counts_all_model_outcomes(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    outcomes = [
        ("Q001", "PASS"),
        ("Q002", "FAIL"),
        ("Q003", "REJECTED"),
        ("Q004", "ERROR"),
    ]

    for case_id, status in outcomes:
        save_result(
            case_id,
            file_path=file_path,
            run_id="run-mixed",
            evaluation_type="model",
            status=status,
        )

    summary = summarize_history(
        file_path,
        run_id="run-mixed",
        evaluation_type="model",
    )

    assert summary["total"] == 4
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["rejected"] == 1
    assert summary["errors"] == 1
    assert summary["completed"] == 2
    assert summary["pass_rate_pct"] == 50.0
    assert summary["overall_success_rate_pct"] == 25.0



def test_summarize_history_with_no_completed_evaluations(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result(
        "Q001",
        file_path=file_path,
        evaluation_type="model",
        status="REJECTED",
    )

    save_result(
        "Q002",
        file_path=file_path,
        evaluation_type="model",
        status="ERROR",
    )

    summary = summarize_history(
        file_path,
        evaluation_type="model",
    )

    assert summary["total"] == 2
    assert summary["completed"] == 0
    assert summary["rejected"] == 1
    assert summary["errors"] == 1
    assert summary["pass_rate_pct"] == 0.0
    assert summary["overall_success_rate_pct"] == 0.0