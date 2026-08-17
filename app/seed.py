from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.photo import PhotoModel

SEED_PHOTOS = [
    {"src": "/images/cat1.jpg", "title": "どこかを見つめる猫ちゃん", "date": "2026/06/02"},
    {"src": "/images/cat2.jpg", "title": "こっちを見つめる猫ちゃん", "date": "2026/06/01"},
    {"src": "/images/cat3.jpg", "title": "アップの猫ちゃん", "date": "2026/06/01"},
    {"src": "/images/cat4.jpg", "title": "木の枝に手を伸ばす猫ちゃん", "date": "2026/06/01"},
    {"src": "/images/cat5.jpg", "title": "顔を隠す猫ちゃん", "date": "2026/06/01"},
]


def seed_if_empty(db: Session) -> None:
    if db.scalars(select(PhotoModel)).first() is not None:
        return
    db.add_all([PhotoModel(**photo) for photo in SEED_PHOTOS])
    db.commit()
