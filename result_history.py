import json
from datetime import datetime, timezone
from pathlib import Path


def save_result(case_id, passed, file_path="runs/evaluations.jsonl"):
    record = {
        "case_id": case_id,
        "status": "PASS" if passed else "FAIL",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")