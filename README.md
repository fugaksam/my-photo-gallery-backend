# my-photo-gallery-backend

`my-photo-gallery`（Next.js FE）用の Python API です。

Phase 1 では S3 / DB 未使用で、写真データはプロセス内メモリに保持します（再起動で初期データに戻ります）。

FE リポジトリ: 別リポ `my-photo-gallery`（`NEXT_PUBLIC_API_BASE_URL` でこの API を向ける）

## 技術スタック

- Python 3.11+
- FastAPI
- Uvicorn

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

## エンドポイント

| Method | Path | 内容 |
|--------|------|------|
| GET | `/health` | ヘルスチェック |
| GET | `/api/photos` | 写真一覧 |
| GET | `/api/photos/{id}` | 写真詳細（なければ 404） |
| POST | `/api/photos` | 写真登録 |

### POST ボディ例

```json
{
  "src": "/images/cat1.jpg",
  "title": "テスト",
  "date": "2026/07/28"
}
```

## FE 側の接続

`my-photo-gallery` の `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

CORS は `http://localhost:3000` を許可済みです。

## ディレクトリ構成

```
app/
├── main.py           # FastAPI app / CORS
├── store.py          # インメモリ写真 store
├── api/
│   ├── health.py
│   └── photos.py
└── schemas/
    └── photo.py
```

## スコープ（Phase 1）

- 対応: health / photos CRUD のうち list・get・create、CORS
- 未対応: S3、DB、認証、一時クレデンシャル発行

## ローカル確認

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/photos
```
