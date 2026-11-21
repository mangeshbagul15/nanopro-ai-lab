"""Chat-driven DuckDB analytics for the AI Lab.

Handles prompts that explicitly target DuckDB:

* "duckdb: SELECT ..." or a fenced ```sql block mentioning duckdb — runs the
  statement against the local analytical store (data/nanopro.duckdb).
* "duckdb madhe/dataset/table ..." natural questions — answered from the
  catalog of tables present in that file.

Only read-only statements are accepted; writes are refused so the chat can
never corrupt the analytical store. Returns None for unrelated prompts.
"""

import os
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
DB_PATH = os.path.join(DB_DIR, "nanopro.duckdb")

_SQL_FENCE = re.compile(r"```(?:sql)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)
_DUCKDB_WORD = re.compile(r"duckdb|डकडीबी|डक्डीबी", re.IGNORECASE)
_WRITE_WORD = re.compile(
    r"\b(insert|update|delete|drop|create|alter|attach|copy|export|pragma)\b",
    re.IGNORECASE,
)


def _payload(action: str, markdown: str, summary: str, detail: Dict[str, Any], started: float) -> Dict[str, Any]:
    duration_ms = round((time.time() - started) * 1000)
    return {
        "status": "success",
        "response": markdown,
        "summary": summary,
        "message": "",
        "action": action,
        "data": detail,
        "model_routed": "nanopro/duckdb-analytics",
        "model_executed": "duckdb/embedded-engine",
        "model_name": "NanoPro DuckDB Analytics Agent",
        "lab_name": "NanoPro Data Plane",
        "country": "India",
        "flag": "🦆",
        "date_formatted": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "duration_ms": duration_ms,
        "routing_decision": {"selected_model": "nanopro/duckdb-analytics"},
    }


def _error(message: str, started: float) -> Dict[str, Any]:
    duration_ms = round((time.time() - started) * 1000)
    return {
        "status": "error",
        "response": f"❌ {message}\n\n**काहीही बदलले नाही.**",
        "summary": message,
        "message": message,
        "model_routed": "nanopro/duckdb-analytics",
        "model_executed": "duckdb/embedded-engine",
        "model_name": "NanoPro DuckDB Analytics Agent",
        "lab_name": "NanoPro Data Plane",
        "country": "India",
        "flag": "🦆",
        "date_formatted": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "duration_ms": duration_ms,
        "routing_decision": {"selected_model": "nanopro/duckdb-analytics"},
    }


def _connect():
    import duckdb

    os.makedirs(DB_DIR, exist_ok=True)
    # Read-only once the file exists so chat queries can never mutate the
    # analytical store; a missing file is created empty (catalog = empty).
    return duckdb.connect(DB_PATH, read_only=os.path.exists(DB_PATH))


def _render(columns: List[str], rows: List[tuple], limit: int = 15) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows[:limit]:
        cells = ["NULL" if v is None else str(v).replace("|", "\\|") for v in row]
        body.append("| " + " | ".join(cells) + " |")
    lines = [header, divider] + body
    if len(rows) > limit:
        lines.append(f"\n_Showing first {limit} of {len(rows)} rows._")
    return "\n".join(lines)


def _extract_sql(prompt: str) -> str:
    text = (prompt or "").strip()
    block = _SQL_FENCE.search(text)
    if block:
        return block.group(1).strip()
    low = text.lower()
    for marker in ("duckdb:", "duckdb sql:", "duckdb query:", "डकडीबी:"):
        idx = low.find(marker)
        if idx >= 0:
            return text[idx + len(marker):].strip().rstrip(";")
    # Bare statement that names duckdb, e.g. "duckdb SELECT * FROM t"
    m = re.search(r"duckdb\s+(select\b.*)$", low, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip().rstrip(";")
    return ""


def maybe_handle(prompt: str) -> Optional[Dict[str, Any]]:
    text = (prompt or "").strip()
    if not text or not _DUCKDB_WORD.search(text):
        return None

    started = time.time()
    sql = _extract_sql(text)

    try:
        con = _connect()
    except ImportError:
        return _error("DuckDB engine installed नाही (pip install duckdb).", started)
    except Exception as exc:
        return _error(f"DuckDB connect failed: {str(exc)[:300]}", started)

    try:
        # Catalog listing: "duckdb tables/datasets" with no SQL
        if not sql:
            tables = con.execute(
                "SELECT table_schema, table_name FROM information_schema.tables "
                "WHERE table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1,2"
            ).fetchall()
            if not tables:
                return _payload(
                    "duckdb_catalog",
                    "### 🦆 DuckDB catalog — empty store\n\n`data/nanopro.duckdb` मध्ये अजून tables नाहीत. "
                    "SQL लेखन (INSERT/CREATE) chat मधून उपलब्ध नाही — फक्त read-only analytics.",
                    "DuckDB store is empty",
                    {"tables": []},
                    started,
                )
            lines = ["### 🦆 DuckDB live catalog", "", "| Schema | Table |", "| --- | --- |"]
            lines += [f"| `{s}` | `{t}` |" for s, t in tables]
            return _payload(
                "duckdb_catalog",
                "\n".join(lines),
                f"{len(tables)} tables in DuckDB",
                {"tables": [{"schema": s, "table": t} for s, t in tables]},
                started,
            )

        if _WRITE_WORD.search(sql):
            return _error(
                "DuckDB वर फक्त read-only queries (SELECT/WITH) चालतात. "
                "INSERT/UPDATE/DELETE/DDL chat मधून block केले आहे.",
                started,
            )
        head = sql.split(None, 1)[0].upper()
        if head not in ("SELECT", "WITH"):
            return _error(f"`{head}` supported नाही — फक्त SELECT/WITH queries.", started)

        cur = con.execute(sql)
        columns = [d[0] for d in (cur.description or [])]
        rows = cur.fetchmany(200)
        markdown = "\n".join([
            "### 🦆 DuckDB query result",
            "",
            f"```sql\n{sql[:500]}\n```",
            "",
            _render(columns, rows),
            "",
            f"_Completed in {round((time.time()-started)*1000)} ms · store: `data/nanopro.duckdb`._",
        ])
        return _payload(
            "duckdb_query",
            markdown,
            f"{len(rows)} rows from DuckDB",
            {"columns": columns, "rows": [list(r) for r in rows[:50]], "row_count": len(rows), "sql": sql},
            started,
        )
    except Exception as exc:
        return _error(f"DuckDB error: {str(exc)[:500]}", started)
    finally:
        try:
            con.close()
        except Exception:
            pass
