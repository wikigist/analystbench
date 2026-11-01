import json
from datetime import datetime, timezone
from pathlib import Path

def save_result(case_id,
                passed=None,
                file_path="runs/evaluations.jsonl",
                run_id=None,
                evaluation_type="reference",
                status=None,):
    if status is None:
        if not isinstance(passed, bool):
            raise ValueError("passed must be a boolean")

        status = "PASS" if passed else "FAIL"

    else:
        if passed is not None:
            raise ValueError("Provide either passed or status, not both")

        if status not in {"PASS", "FAIL", "REJECTED", "ERROR"}:
            raise ValueError("Unsupported evaluation status")


    record = {
        "case_id": case_id,
        "status": status,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "evaluation_type": evaluation_type,
    }

    if run_id is not None:
        record["run_id"] = run_id

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")