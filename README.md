# LR2IR Player Profile Display

LR2IR(LR2 Rating)サイトからプレイヤー情報を取得して、美しく表示するWebアプリケーションです。

## ✨ 新機能：GitHub Pages での自動更新

このプロジェクトは **サーバーレス** で動作します：

- 🌐 **GitHub Pages** でホスト（カスタムドメイン対応）
- ⚙️ **GitHub Actions** で毎日自動更新
- 📱 クライアントサイド JavaScript で動的表示
- 🔐 プライベート情報は JSON データのみ保存

## 機能

- **プレイヤー基本情報**：プレイヤー名、LR2ID、段位認定、自己紹介、ホームページ
- **プレイ統計**：プレイした曲数、プレイした回数、クリア曲数統計
- **ライバル表示**：登録しているライバルプレイヤーの一覧
- **よくプレイする曲**：Top 10リスト（クリア状態、プレイ回数、ランキング付き）
- **最近プレイした曲**：最新でプレイした曲の記録
- **最近プレイしたコース**：プレイしたコース情報
- **一行BBS**：プレイヤーのコメント欄

## セットアップ

### GitHub Pages への配置

1. **リポジトリをクローン**
```bash
git clone https://github.com/veryslowstarter/veryslowstarter.github.io.git
```

2. **このプロジェクトを `docs/` フォルダにコピー**
   - `docs/index.html`
   - `docs/css/`
   - `docs/js/`
   - `docs/data/`
   - `.github/workflows/`
   - `scraper.py`
   - `fetch_player_data.py`
   - `requirements.txt`

3. **ローカルテスト（オプション）**
```bash
# Python 依存パッケージをインストール
pip install -r requirements.txt

# データを手動で取得
python fetch_player_data.py

# 簡単な HTTP サーバーで確認
python -m http.server 8000 --directory docs
# ブラウザで http://localhost:8000 にアクセス
```

### ローカル開発環境（旧構成）

1. リポジトリをクローン（またはプロジェクトフォルダをコピー）

2. 仮想環境を作成：
```bash
python -m venv venv
```

3. 仮想環境を有効化：
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

4. 依存パッケージをインストール：
```bash
pip install -r requirements.txt
```

## 使用方法

### GitHub Pages での自動更新

- **自動実行**: 毎日 UTC 0:00（日本時間 9:00）
- **手動実行**: GitHub リポジトリの Actions タブ → `Update LR2IR Player Data` → `Run workflow`

### ローカルサーバーの起動（開発用）

```bash
python app.py
```

ブラウザで `http://localhost:5000/` を開く

### プレイヤープロフィールの表示

#### GitHub Pages 版
```
https://old.veryslowstarter.com/
```

#### ローカル版
1. ホームページでプレイヤーIDを入力
2. または直接入力：`http://localhost:5000/player/[プレイヤーID]`

例：
```
http://localhost:5000/player/185532
```

### API（JSON 形式）

```
http://localhost:5000/api/player/[プレイヤーID]
```

JSON 形式でプレイヤーデータを取得できます。

## ファイル構成

### GitHub Pages 版（推奨）
```
veryslowstarter.github.io/
├── docs/
│   ├── index.html              # メインページ
│   ├── css/
│   │   └── style.css           # スタイルシート
│   ├── js/
│   │   └── app.js              # クライアント側ロジック
│   ├── data/
│   │   └── player.json         # プレイヤーデータ（自動更新）
│   ├── _config.yml             # GitHub Pages設定
│   └── CNAME                   # カスタムドメイン設定
├── .github/
│   └── workflows/
│       └── update-player-data.yml    # 毎日実行するワークフロー
├── scraper.py              # スクレイピング機能
├── fetch_player_data.py    # JSON データ生成スクリプト
├── requirements.txt        # Python依存パッケージ
└── README.md
```

### ローカル開発版
```
LR2IR_Player_Profile/
├── app.py                 # Flask アプリケーション
├── scraper.py             # スクレイビング機能
├── requirements.txt       # 依存パッケージリスト
├── docs/                  # GitHub Pages用フォルダ
├── static/                # 静的ファイル（開発用）
├── templates/             # HTMLテンプレート（開発用）
└── venv/                  # Python仮想環境
```

## トラブルシューティング

### GitHub Pages での自動更新が実行されない

1. **リポジトリの Settings を確認**：
   - Code and automation → Actions → General
   - "Workflow permissions" が "Read and write permissions" に設定されているか確認

2. **ワークフロー実行ログを確認**：
   - Actions タブ → `Update LR2IR Player Data` → 実行履歴を確認

3. **手動実行でテスト**：
   - Actions タブ → Workflows → `Update LR2IR Player Data`
   - "Run workflow" をクリック

### GitHub Pages がデプロイされない

1. **リポジトリの Settings を確認**：
   - Pages セクション
   - Source が "Deploy from a branch" に設定
   - Branch が "main" / "docs folder" に設定されているか確認

2. **カスタムドメインの設定**：
   - Settings → Pages → Custom domain
   - `old.veryslowstarter.com` を入力
   - DNS CNAME レコードで `veryslowstarter.github.io` を指定

### モジュールが見つからないエラー
仮想環境が有効になっているか確認し、以下を実行：
```bash
pip install -r requirements.txt
```

### エンコーディングエラー
CP932 エンコーディングをサポートする Python 環境が必要です。

### サーバーが起動しない
ポート 5000 が使用中でないか確認してください。別のポートで起動：
```python
# app.py内の最後の行を編集
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # ポートを 8000 に変更
```

## GitHub Pages設定の詳細

### 1. リポジトリ設定

**Settings → Pages**：
- Source: "Deploy from a branch"
- Branch: "main" + "/docs"

### 2. カスタムドメイン設定

**Settings → Pages → Custom domain**：
```
old.veryslowstarter.com
```

**DNS 設定**（ドメイン管理者画面）：
```
CNAME レコード：
www.old.veryslowstarter.com → veryslowstarter.github.io
```

### 3. GitHub Actions の設定

**Settings → Actions → General**：
- Workflow permissions: "Read and write permissions" ✓
- Allow GitHub Actions to create and approve pull requests: チェック（必要に応じて）

## 主な機能コンポーネント

### scraper.py
- `LR2IRScraper` クラス：LR2IR サイトからデータを取得
- CP932 エンコーディング対応
- テーブル構造を解析してプレイヤー情報を抽出

### fetch_player_data.py
- Python スクリプト：定期実行用
- LR2IR からデータを取得
- JSON ファイルとして `docs/data/player.json` に保存

### app.py
- Flask Web アプリケーション（ローカル開発用）
- ルート：
  - `GET /` - ホームページ
  - `GET /player/<id>` - プレイヤープロフィール表示
  - `POST /search` - プレイヤー検索
  - `GET /api/player/<id>` - JSON API

### /docs フォルダ
- `index.html` - 静的 HTML クライアント
- `js/app.js` - クライアント側ロジック（JSON 読み込み・表示）
- `css/style.css` - スタイルシート

## 備考

- このアプリケーションは教育目的で作成されています
- LR2IR サイトのスクレイピングについては、サイトの利用規約に従ってください
- CP932 エンコーディングは Windows 日本語環境に対応しています
- GitHub Pages は静的コンテンツのみの配信のため、サーバー側の処理は GitHub Actions で実行されます

## 機能

- **プレイヤー基本情報**：プレイヤー名、LR2ID、段位認定、自己紹介、ホームページ
- **プレイ統計**：プレイした曲数、プレイした回数、クリア曲数統計
- **ライバル表示**：登録しているライバルプレイヤーの一覧
- **よくプレイする曲**：Top 10 リスト（クリア状態、プレイ回数、ランキング付き）
- **最近プレイした曲**：最新でプレイした曲の記録
- **最近プレイしたコース**：プレイしたコース情報
- **一行 BBS**：プレイヤーのコメント欄
- **自動更新**：毎日 UTC 0:00 に GitHub Actions で自動更新
- **カスタムドメイン**：`old.veryslowstarter.com` で配信
