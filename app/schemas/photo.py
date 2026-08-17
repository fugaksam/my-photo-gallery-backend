from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    src: str
    title: str
    date: str
