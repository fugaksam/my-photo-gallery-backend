from fastapi import APIRouter, HTTPException

from app import store
from app.schemas.photo import Photo, PhotoCreate

router = APIRouter(prefix="/api/photos", tags=["photos"])


@router.get("", response_model=list[Photo])
def get_photos() -> list[Photo]:
    return store.list_photos()


@router.get("/{photo_id}", response_model=Photo)
def get_photo(photo_id: int) -> Photo:
    photo = store.get_photo(photo_id)
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.post("", response_model=Photo, status_code=201)
def post_photo(data: PhotoCreate) -> Photo:
    return store.create_photo(data)
