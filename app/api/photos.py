from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.photo import PhotoModel
from app.schemas.photo import Photo

router = APIRouter(prefix="/api/photos", tags=["photos"])


def _to_photo(row: PhotoModel, request: Request) -> Photo:
    base = str(request.base_url).rstrip("/")
    src = f"{base}/api/photos/{row.id}/image"
    return Photo(id=row.id, src=src, title=row.title, date=row.date)


@router.get("", response_model=list[Photo])
def get_photos(request: Request, db: Session = Depends(get_db)) -> list[Photo]:
    rows = db.scalars(select(PhotoModel).order_by(PhotoModel.id)).all()
    return [_to_photo(row, request) for row in rows]


@router.get("/{photo_id}", response_model=Photo)
def get_photo(photo_id: int, request: Request, db: Session = Depends(get_db)) -> Photo:
    row = db.get(PhotoModel, photo_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return _to_photo(row, request)


@router.get("/{photo_id}/image")
def get_photo_image(photo_id: int, db: Session = Depends(get_db)) -> Response:
    row = db.get(PhotoModel, photo_id)
    if row is None or row.image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    media_type = row.content_type or "application/octet-stream"
    return Response(content=row.image, media_type=media_type)


@router.post("", response_model=Photo, status_code=201)
async def post_photo(
    request: Request,
    title: str = Form(...),
    date: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Photo:
    if not title.strip():
        raise HTTPException(status_code=400, detail="title is required")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="file must be an image")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty file")

    row = PhotoModel(
        title=title.strip(),
        date=date.strip(),
        image=data,
        content_type=file.content_type,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_photo(row, request)
