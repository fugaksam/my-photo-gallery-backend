from app.schemas.photo import Photo, PhotoCreate

_photos: list[Photo] = [
    Photo(id=1, src="/images/cat1.jpg", title="どこかを見つめる猫ちゃん", date="2026/06/02"),
    Photo(id=2, src="/images/cat2.jpg", title="こっちを見つめる猫ちゃん", date="2026/06/01"),
    Photo(id=3, src="/images/cat3.jpg", title="アップの猫ちゃん", date="2026/06/01"),
    Photo(id=4, src="/images/cat4.jpg", title="木の枝に手を伸ばす猫ちゃん", date="2026/06/01"),
    Photo(id=5, src="/images/cat5.jpg", title="顔を隠す猫ちゃん", date="2026/06/01"),
]
_next_id = 6


def list_photos() -> list[Photo]:
    return list(_photos)


def get_photo(photo_id: int) -> Photo | None:
    for photo in _photos:
        if photo.id == photo_id:
            return photo
    return None


def create_photo(data: PhotoCreate) -> Photo:
    global _next_id
    photo = Photo(id=_next_id, src=data.src, title=data.title, date=data.date)
    _next_id += 1
    _photos.append(photo)
    return photo
