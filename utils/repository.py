
from __future__ import annotations
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

class ResumeRepository:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS versions (
                    id TEXT PRIMARY KEY,
                    resume_id TEXT NOT NULL,
                    version_num INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            connection.commit()

    def save_resume(self, resume_id: str, name: str, data: dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            existing = connection.execute("SELECT id FROM resumes WHERE id = ?", (resume_id,)).fetchone()
            if existing:
                version_num = connection.execute("SELECT MAX(version_num) FROM versions WHERE resume_id = ?", (resume_id,)).fetchone()
                version_num = (version_num[0] or 0) + 1 if version_num else 1
                connection.execute(
                    "INSERT INTO versions (id, resume_id, version_num, data, created_at) VALUES (?, ?, ?, ?, ?)",
                    (f"{resume_id}_v{version_num}", resume_id, version_num, json.dumps(data, ensure_ascii=False), now)
                )
                connection.execute(
                    "UPDATE resumes SET name = ?, data = ?, updated_at = ? WHERE id = ?",
                    (name, json.dumps(data, ensure_ascii=False), now, resume_id)
                )
            else:
                connection.execute(
                    "INSERT INTO resumes (id, name, data, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (resume_id, name, json.dumps(data, ensure_ascii=False), now, now)
                )
            connection.commit()

    def get_resume(self, resume_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,)).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["data"] = json.loads(result["data"])
        return result

    def list_resumes(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute("SELECT id, name, created_at, updated_at FROM resumes ORDER BY updated_at DESC").fetchall()
        return [dict(row) for row in rows]

    def delete_resume(self, resume_id: str) -> bool:
        with self._connect() as connection:
            connection.execute("DELETE FROM versions WHERE resume_id = ?", (resume_id,))
            cursor = connection.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
            connection.commit()
        return cursor.rowcount > 0

    def get_versions(self, resume_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, version_num, data, created_at FROM versions WHERE resume_id = ? ORDER BY version_num DESC",
                (resume_id,)
            ).fetchall()
        return [{**dict(row), "data": json.loads(row["data"])} for row in rows]
