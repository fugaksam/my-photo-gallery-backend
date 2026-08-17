from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.photo import PhotoModel

SEED_DIR = Path(__file__).resolve().parent.parent / "seed_images"

SEED_PHOTOS = [
    {
        "filename": "cat1.jpg",
        "legacy_src": "/images/cat1.jpg",
        "title": "どこかを見つめる猫ちゃん",
        "date": "2026/06/02",
    },
    {
        "filename": "cat2.jpg",
        "legacy_src": "/images/cat2.jpg",
        "title": "こっちを見つめる猫ちゃん",
        "date": "2026/06/01",
    },
    {
        "filename": "cat3.jpg",
        "legacy_src": "/images/cat3.jpg",
        "title": "アップの猫ちゃん",
        "date": "2026/06/01",
    },
    {
        "filename": "cat4.jpg",
        "legacy_src": "/images/cat4.jpg",
        "title": "木の枝に手を伸ばす猫ちゃん",
        "date": "2026/06/01",
    },
    {
        "filename": "cat5.jpg",
        "legacy_src": "/images/cat5.jpg",
        "title": "顔を隠す猫ちゃん",
        "date": "2026/06/01",
    },
]


def _read_seed_image(filename: str) -> bytes:
    path = SEED_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"seed image not found: {path}")
    return path.read_bytes()


def seed_photos(db: Session) -> None:
    """初期画像を SQLite BLOB として投入する。既存の public パス行もバックフィルする。"""
    rows = list(db.scalars(select(PhotoModel)).all())
    by_src = {row.src: row for row in rows if row.src}
    by_title = {row.title: row for row in rows}

    changed = False
    for photo in SEED_PHOTOS:
        row = by_src.get(photo["legacy_src"]) or by_title.get(photo["title"])
        if row is not None and row.image is not None:
            continue

        image = _read_seed_image(photo["filename"])
        if row is None:
            db.add(
                PhotoModel(
                    src="",
                    title=photo["title"],
                    date=photo["date"],
                    image=image,
                    content_type="image/jpeg",
                )
            )
        else:
            row.image = image
            row.content_type = "image/jpeg"
            row.src = ""
        changed = True

    if changed:
        db.commit()
