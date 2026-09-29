from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class AlbumModel(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    photos: Mapped[list["AlbumPhotoModel"]] = relationship(
        "AlbumPhotoModel",
        back_populates="album",
        cascade="all, delete-orphan",
        order_by="AlbumPhotoModel.position",
    )


class AlbumPhotoModel(Base):
    __tablename__ = "album_photos"
    __table_args__ = (
        UniqueConstraint("album_id", "photo_id", name="uq_album_photo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    album_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("albums.id", ondelete="CASCADE"),
        nullable=False,
    )
    photo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("photos.id", ondelete="CASCADE"),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    album: Mapped["AlbumModel"] = relationship("AlbumModel", back_populates="photos")
