from pydantic import BaseModel, Field


class Photo(BaseModel):
    id: int
    src: str
    title: str
    date: str
    description: str


class PhotoUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(default="")
