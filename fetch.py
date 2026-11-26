"""Дневные итоги и последняя цена юаня на Московской бирже (CNYRUB_TOM) — в файлы data/.

Только стандартная библиотека Python. Запуск: python fetch.py
- data/moex_cny.csv — дневные итоги торгов с 2013 года: открытие, максимум, минимум, закрытие,
  средневзвешенная цена, число сделок (дописываются последние дни);
- data/latest.json — последняя цена и время обновления.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ISS = "https://iss.moex.com/iss"
SECURITY = "engines/currency/markets/selt/boards/CETS/securities/CNYRUB_TOM"
COLUMNS = ["date", "open", "high", "low", "close", "waprice", "numtrades"]
ISS_COLUMNS = ["TRADEDATE", "OPEN", "HIGH", "LOW", "CLOSE", "WAPRICE", "NUMTRADES"]
START = dt.date(2013, 1, 1)
OVERLAP = dt.timedelta(days=14)  # заново берём последние две недели — биржа иногда уточняет итоги
DATA = Path(__file__).resolve().parent / "data"
HISTORY = DATA / "moex_cny.csv"
LATEST = DATA / "latest.json"
USER_AGENT = "moex-feed/1.0 (public market data mirror)"


def get_json(path: str, params: dict) -> dict:
    url = f"{ISS}/{path}.json?" + urllib.parse.urlencode({**params, "iss.meta": "off"})
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except OSError:
            if attempt == 3:
                raise
            time.sleep(5 * 2**attempt)
    raise RuntimeError("unreachable")


def read_history() -> dict[str, list[str]]:
    if not HISTORY.exists():
        return {}
    with HISTORY.open(newline="") as f:
        return {row[0]: row for row in csv.reader(f) if row and row[0] != "date"}


def fetch_history(start: dt.date, end: dt.date) -> dict[str, list[str]]:
    rows, offset = {}, 0
    while True:
        block = get_json(
            f"history/{SECURITY}",
            {"from": start.isoformat(), "till": end.isoformat(), "start": offset, "iss.only": "history"},
        )["history"]
        if not block["data"]:
            return rows
        index = [block["columns"].index(c) for c in ISS_COLUMNS]
        for record in block["data"]:
            values = [record[i] for i in index]
            if values[4] in (None, 0):  # день без сделок
                continue
            rows[values[0]] = ["" if v is None else str(v) for v in values]
        offset += len(block["data"])


def update_history(today: dt.date) -> int:
    rows = read_history()
    last = max((dt.date.fromisoformat(d) for d in rows), default=None)
    start = START if last is None else last - OVERLAP
    rows.update(fetch_history(start, today))
    DATA.mkdir(exist_ok=True)
    tmp = HISTORY.with_suffix(".tmp")
    with tmp.open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(COLUMNS)
        writer.writerows(rows[d] for d in sorted(rows))
    tmp.replace(HISTORY)
    return len(rows)


def update_latest() -> dict:
    data = get_json(SECURITY, {"iss.only": "marketdata", "marketdata.columns": "LAST,UPDATETIME,SYSTIME"})["marketdata"]
    row = dict(zip(data["columns"], data["data"][0])) if data["data"] else {}
    latest = {"last": row.get("LAST"), "updatetime": row.get("UPDATETIME"), "systime": row.get("SYSTIME")}
    LATEST.write_text(json.dumps(latest, ensure_ascii=False) + "\n")
    return latest


if __name__ == "__main__":
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).date()
    print("Дней в истории:", update_history(today))
    print("Последняя цена:", update_latest())
