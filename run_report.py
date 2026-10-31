import json
from pathlib import Path


def summarize_history(file_path="runs/evaluations.jsonl", run_id=None):
    passed = 0
    failed = 0

    with Path(file_path).open("r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            if run_id is not None and record.get("run_id") != run_id:
                continue

            if record["status"] == "PASS":
                passed += 1
            elif record["status"] == "FAIL":
                failed += 1

    return {
        "total": passed + failed,
        "passed": passed,
        "failed": failed,
    }