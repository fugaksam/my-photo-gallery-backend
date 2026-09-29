from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.photos import _to_photo
from app.db import get_db
from app.models.album import AlbumModel, AlbumPhotoModel
from app.models.photo import PhotoModel
from app.schemas.album import AlbumCreate, AlbumDetail, AlbumSummary, AlbumUpdate

router = APIRouter(prefix="/api/albums", tags=["albums"])


def _next_default_album_name(db: Session) -> str:
    names = set(db.scalars(select(AlbumModel.name)).all())
    n = 1
    while f"アルバム{n}" in names:
        n += 1
    return f"アルバム{n}"


def _resolve_album_name(db: Session, name: str | None) -> str:
    if name is None or not name.strip():
        return _next_default_album_name(db)
    return name.strip()


def _validate_photo_ids(db: Session, photo_ids: list[int]) -> list[int]:
    if not photo_ids:
        return []

    # 入力順を保ちつつ重複を除去
    unique_ids: list[int] = []
    seen: set[int] = set()
    for photo_id in photo_ids:
        if photo_id in seen:
            continue
        seen.add(photo_id)
        unique_ids.append(photo_id)

    rows = db.scalars(select(PhotoModel.id).where(PhotoModel.id.in_(unique_ids))).all()
    existing = set(rows)
    missing = [photo_id for photo_id in unique_ids if photo_id not in existing]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"photos not found: {missing}",
        )
    return unique_ids


def _set_album_photos(album: AlbumModel, photo_ids: list[int]) -> None:
    album.photos.clear()
    for index, photo_id in enumerate(photo_ids):
        album.photos.append(
            AlbumPhotoModel(photo_id=photo_id, position=index)
        )


def _thumbnail_src(album: AlbumModel, request: Request) -> str | None:
    if not album.photos:
        return None
    first = album.photos[0]
    base = str(request.base_url).rstrip("/")
    return f"{base}/api/photos/{first.photo_id}/image"


def _to_summary(album: AlbumModel, request: Request) -> AlbumSummary:
    return AlbumSummary(
        id=album.id,
        name=album.name,
        photo_count=len(album.photos),
        thumbnail_src=_thumbnail_src(album, request),
    )


def _to_detail(album: AlbumModel, request: Request, db: Session) -> AlbumDetail:
    photos: list = []
    for link in album.photos:
        photo = db.get(PhotoModel, link.photo_id)
        if photo is not None:
            photos.append(_to_photo(photo, request))
    return AlbumDetail(id=album.id, name=album.name, photos=photos)


def _get_album_or_404(db: Session, album_id: int) -> AlbumModel:
    album = db.scalar(
        select(AlbumModel)
        .where(AlbumModel.id == album_id)
        .options(selectinload(AlbumModel.photos))
    )
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.get("", response_model=list[AlbumSummary])
def get_albums(request: Request, db: Session = Depends(get_db)) -> list[AlbumSummary]:
    albums = db.scalars(
        select(AlbumModel)
        .options(selectinload(AlbumModel.photos))
        .order_by(AlbumModel.id)
    ).all()
    return [_to_summary(album, request) for album in albums]


@router.get("/{album_id}", response_model=AlbumDetail)
def get_album(
    album_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> AlbumDetail:
    album = _get_album_or_404(db, album_id)
    return _to_detail(album, request, db)


@router.post("", response_model=AlbumDetail, status_code=201)
def post_album(
    body: AlbumCreate,
    request: Request,
    db: Session = Depends(get_db),
) -> AlbumDetail:
    photo_ids = _validate_photo_ids(db, body.photo_ids)
    album = AlbumModel(name=_resolve_album_name(db, body.name))
    _set_album_photos(album, photo_ids)
    db.add(album)
    db.commit()
    db.refresh(album)
    album = _get_album_or_404(db, album.id)
    return _to_detail(album, request, db)


@router.patch("/{album_id}", response_model=AlbumDetail)
def patch_album(
    album_id: int,
    body: AlbumUpdate,
    request: Request,
    db: Session = Depends(get_db),
) -> AlbumDetail:
    album = _get_album_or_404(db, album_id)

    if body.name is not None:
        name = body.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="name is required")
        album.name = name

    if body.photo_ids is not None:
        photo_ids = _validate_photo_ids(db, body.photo_ids)
        _set_album_photos(album, photo_ids)

    db.commit()
    album = _get_album_or_404(db, album_id)
    return _to_detail(album, request, db)


@router.delete("/{album_id}", status_code=204)
def delete_album(album_id: int, db: Session = Depends(get_db)) -> None:
    album = _get_album_or_404(db, album_id)
    db.delete(album)
    db.commit()
