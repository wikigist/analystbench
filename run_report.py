import json
from pathlib import Path


def summarize_history(file_path="runs/evaluations.jsonl", run_id=None, evaluation_type=None,):
    passed = 0
    failed = 0

    with Path(file_path).open("r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            if run_id is not None and record.get("run_id") != run_id:
                continue


            if (
                evaluation_type is not None
                and record.get("evaluation_type", "reference") != evaluation_type
                ):
                continue

            if record["status"] == "PASS":
                passed += 1
            elif record["status"] == "FAIL":
                failed += 1


    total = passed + failed

    if total > 0:
        pass_rate_pct = (passed / total) * 100
    else:
        pass_rate_pct = 0.0

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate_pct": pass_rate_pct,
    }