from pydantic import BaseModel, Field

from app.schemas.photo import Photo


class AlbumSummary(BaseModel):
    id: int
    name: str
    photo_count: int
    thumbnail_src: str | None = None


class AlbumDetail(BaseModel):
    id: int
    name: str
    photos: list[Photo]


class AlbumCreate(BaseModel):
    name: str | None = Field(default=None)
    photo_ids: list[int] = Field(default_factory=list)


class AlbumUpdate(BaseModel):
    name: str | None = Field(default=None)
    photo_ids: list[int] | None = Field(default=None)
