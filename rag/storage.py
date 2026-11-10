import json
from pathlib import Path


def save_index(indexed_records, file_path):
    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(indexed_records, file)


def load_index(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        indexed_records = json.load(file)

    return indexed_records