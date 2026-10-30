import json

from result_history import save_result


def test_save_result_keeps_history(tmp_path):
    file_path = tmp_path / "evaluations.jsonl"

    save_result("Q001", True, file_path)
    save_result("Q002", False, file_path)

    with file_path.open("r", encoding="utf-8") as file:
        records = [json.loads(line) for line in file]

    assert len(records) == 2
    assert records[0]["status"] == "PASS"
    assert records[1]["status"] == "FAIL"
    assert records[0]["case_id"] == "Q001"
    assert records[1]["case_id"] == "Q002"
    assert "recorded_at" in records[0]