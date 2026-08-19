from sqlalchemy import Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class PhotoModel(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    # 画像本体を SQLite BLOB で保持する
    image: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    content_type: Mapped[str | None] = mapped_column(String, nullable=True)
