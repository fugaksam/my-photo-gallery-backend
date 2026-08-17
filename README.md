# my-photo-gallery-backend

`my-photo-gallery`（Next.js FE）用の Python API です。

写真メタデータと画像本体（学習用 **SQLite BLOB**）を SQLAlchemy で永続化します（`data/app.db`）。S3 は未導入です。

FE リポジトリ: 別リポ `my-photo-gallery`（`NEXT_PUBLIC_API_BASE_URL` でこの API を向ける）

## 技術スタック

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- SQLite

## セットアップ

```bash
cd my-photo-gallery-backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 起動

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

- API: http://localhost:8000
- Health: http://localhost:8000/health
- Swagger: http://localhost:8000/docs
- DB ファイル: `data/app.db`（初回起動時に作成・シード）

## エンドポイント

| Method | Path | 内容 |
|--------|------|------|
| GET | `/health` | ヘルスチェック |
| GET | `/api/photos` | 写真一覧 |
| GET | `/api/photos/{id}` | 写真詳細（なければ 404） |
| GET | `/api/photos/{id}/image` | 画像本体（BLOB） |
| POST | `/api/photos` | 写真登録（`multipart/form-data`: title, date, file） |

### POST 例（multipart）

```bash
curl -X POST http://localhost:8000/api/photos \
  -F "title=テスト" \
  -F "date=2026/08/12" \
  -F "file=@./sample.jpg"
```

アップロード後の `src` は `http://localhost:8000/api/photos/{id}/image` になります。

## FE 側の接続

`my-photo-gallery` の `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

CORS は `http://localhost:3000` を許可済みです。

## ディレクトリ構成

```
data/
└── app.db              # SQLite（gitignore）
app/
├── main.py             # FastAPI / CORS / lifespan
├── db.py               # engine, Session, get_db
├── seed.py             # 初期データ投入
├── models/
│   └── photo.py        # PhotoModel
├── api/
│   ├── health.py
│   └── photos.py
└── schemas/
    └── photo.py        # Pydantic
```

## スコープ

- 対応: health / photos list・get・create、画像 BLOB 保存・配信、CORS、SQLite 永続化
- 未対応: S3、認証、一時クレデンシャル発行、Alembic

## ローカル確認

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/photos
sqlite3 data/app.db "SELECT id, title FROM photos;"
```
