from sqlalchemy import text

from app.db import engine


def ensure_blob_columns() -> None:
    """既存 SQLite テーブルに BLOB 列が無ければ追加する。"""
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(photos)")).fetchall()
        if not rows:
            return
        names = {row[1] for row in rows}
        if "image" not in names:
            conn.execute(text("ALTER TABLE photos ADD COLUMN image BLOB"))
        if "content_type" not in names:
            conn.execute(text("ALTER TABLE photos ADD COLUMN content_type VARCHAR"))
