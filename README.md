# nft-nenga

## 目次
- [貢献者ガイド(CONTRIBUTING.md)](#貢献者ガイドcontributingmd)
- [動作環境（確認済み）](#動作環境確認済み)
- [動作確認](#動作確認)
- [APIエンドポイント](#apiエンドポイント)
- [ディレクトリ構成](#ディレクトリ構成)
- [ライセンス](#ライセンス)

## 貢献者ガイド(CONTRIBUTING.md)
準備中

## 動作環境（確認済み）
- Ubuntu(WSL2)
  - Docker
- macOS(x86-64, arm64)
  - Docker Desktop もしくは OrbStack

## 動作確認
1. リポジトリのクローンと移動
```
git clone git@github.com:shun-harutaro/nft-nenga.git
cd nft-nenga
```

2. Dockerイメージのビルド
```
sudo docker compose build [--no-cache]
```

3. コンテナ起動
```
sudo docker compose up
# Detachモード
sudo docker compose up -d
```

4. localhost で開いてみましょう <br>
frontend: http://localhost:3000 <br>
backend: http://localhost:8000

6. コンテナの停止
```
sudo docker compose down
```

## APIエンドポイント
未定義

## ディレクトリ構成
- api (application - FastAPI)
- nginx (web-server)
```
.
├── LICENSE
├── README.md
├── backend
│   ├── Dockerfile
│   ├── main.py
│   ├── pyproject.toml
│   └── uv.lock
├── docker-compose.yml
└── frontend
    ├── Dockerfile
    ├── README.md
    ├── eslint.config.js
    ├── index.html
    ├── jsconfig.json
    ├── package-lock.json
    ├── package.json
    ├── public
    │   └── favicon.ico
    ├── src
    │   ├── App.vue
    │   ├── assets
    │   │   ├── base.css
    │   │   └── main.css
    │   ├── components
    │   │   └── Test.vue
    │   └── main.js
    └── vite.config.js
```
ami
## ライセンス
本リポジトリはMITライセンスです。
