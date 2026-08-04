from pydantic import BaseModel, Field


class Photo(BaseModel):
    id: int
    src: str
    title: str
    date: str


class PhotoCreate(BaseModel):
    src: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    date: str = Field(..., min_length=1)
