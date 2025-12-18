from future import annotations
from csv import DictReader
from pathlib import Path

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf8") as file:
        rows.extend(DictReader(file))
    return rows