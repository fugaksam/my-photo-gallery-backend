from sqlalchemy import text

from app.db import engine


def migrate_photos_schema() -> None:
    """既存 SQLite の photos テーブルを現行スキーマに合わせる。"""
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(photos)")).fetchall()
        if not rows:
            return
        names = {row[1] for row in rows}
        if "image" not in names:
            conn.execute(text("ALTER TABLE photos ADD COLUMN image BLOB"))
        if "content_type" not in names:
            conn.execute(text("ALTER TABLE photos ADD COLUMN content_type VARCHAR"))
        if "src" in names:
            conn.execute(text("ALTER TABLE photos DROP COLUMN src"))
