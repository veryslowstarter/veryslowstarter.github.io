# GitHub Pages へのセットアップガイド

このドキュメントは、LR2IR Player Profile Display を `https://old.veryslowstarter.com` で公開するための手順を説明します。

## ステップ 1: ファイルの配置

### 既存リポジトリへの追加

`veryslowstarter.github.io` リポジトリの構成：

```
veryslowstarter.github.io/
├── docs/
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   ├── data/
│   │   └── player.json
│   ├── _config.yml
│   └── CNAME
├── .github/
│   └── workflows/
│       └── update-player-data.yml
├── scraper.py
├── fetch_player_data.py
├── requirements.txt
└── README.md
```

### 配置方法

1. 本プロジェクトのファイルをコピー：
   - `docs/` フォルダ全体
   - `.github/workflows/` フォルダ
   - `scraper.py`
   - `fetch_player_data.py`
   - `requirements.txt`

2. 既存ファイルとの競合注意：
   - 本プロジェクトの README.md は別途のプロジェクトドキュメント
   - リポジトリのメイン README.md は保持する

## ステップ 2: GitHub Pages 設定

### リポジトリ Settings

1. **Settings → Pages**
   - Source: "Deploy from a branch"
   - Branch: "main" + "/docs" を選択
   - Save

2. **Settings → Environments**
   - Deployment branch restrictions を確認

## ステップ 3: カスタムドメイン設定

### DNS 設定（ドメイン管理者画面）

```
CNAME レコード:
Hostname: old.veryslowstarter.com
Points to: veryslowstarter.github.io
```

### GitHub Pages カスタムドメイン設定

1. リポジトリの **Settings → Pages**
2. **Custom domain** に `old.veryslowstarter.com` を入力
3. "Save"

**注意**：CNAME ファイルが `docs/CNAME` に自動生成されます。

## ステップ 4: GitHub Actions 認可設定

### Actions 権限の設定

**Settings → Actions → General**

1. **Workflow permissions**
   - ✅ "Read and write permissions" を選択
   - ✅ "Allow GitHub Actions to create and approve pull requests" をチェック

2. **Actions permissions**
   - "Allow all actions and reusable workflows" を選択

## ステップ 5: 初回実行

### 手動で GitHub Actions を実行

1. **Actions** タブを開く
2. **Update LR2IR Player Data** をクリック
3. **Run workflow** ボタンをクリック
4. ワークフロー実行を確認

### 実行結果確認

- `docs/data/player.json` が更新されているか確認
- 約 1-2 分後、ページが更新される

## ステップ 6: 自動実行スケジュール確認

### ワークフロー実行スケジュール

`.github/workflows/update-player-data.yml` の設定：

```yaml
on:
  schedule:
    # 毎日 UTC 0:00 に実行（日本時間 9:00）
    - cron: '0 0 * * *'
```

**実行時刻**：
- UTC 0:00 (世界協定時)
- JST 9:00 (日本標準時)

### スケジュール変更

別の時刻に変更する場合：

```yaml
  schedule:
    - cron: '0 12 * * *'  # UTC 12:00 = JST 21:00
```

Cron フォーマット：`分 時 日 月 曜日`

## ステップ 7: トラブルシューティング

### ページが表示されない

1. **GitHub Pages デプロイ確認**：
   - Settings → Pages
   - "Your site is published at" が表示されているか確認

2. **DNS 設定確認**：
   ```bash
   nslookup old.veryslowstarter.com
   # 応答: veryslowstarter.github.io のアドレスが返る
   ```

3. **HTTPS 強制リダイレクト**：
   - Settings → Pages
   - "Enforce HTTPS" がオンになっているか確認（推奨）

### GitHub Actions が実行されない

1. **Workflow permissions 確認**：
   - Settings → Actions → General
   - "Read and write permissions" が選択されているか

2. **ワークフロー構文エラー**：
   - Actions タブで実行ログを確認
   - エラーメッセージから問題を特定

3. **Python パッケージ不足**：
   - Workflow ログで pip install エラーを確認
   - `requirements.txt` が適切に配置されているか確認

### player.json が更新されない

1. **LR2IR サイトへの接続**：
   - workflow ログで "Error" を検索
   - 通常の HTTP 接続が可能か確認

2. **エンコーディング問題**：
   - workflow ログで「decode」や「encoding」エラーを確認

## 監視と保守

### ワークフロー実行状況の確認

1. **Actions** タブ → **Update LR2IR Player Data**
2. 実行履歴から最新実行を確認
3. 成功（✓）と失敗（✕）をチェック

### 月次確認

- 毎月 1 日に最新実行を確認
- エラーが続いていないか確認
- GitHub からの通知メール確認

## 参考リンク

- [GitHub Pages ドキュメント](https://docs.github.com/en/pages)
- [GitHub Actions ドキュメント](https://docs.github.com/en/actions)
- [カスタムドメインの設定](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## サポートが必要な場合

- GitHub Issues で質問する
- GitHub Support に連絡するだけでなく、ログを確認する

---

**最終確認チェックリスト**：

- [ ] ファイル配置完了
- [ ] GitHub Pages 設定完了
- [ ] DNS CNAME レコード設定完了
- [ ] GitHub Actions 権限設定完了
- [ ] 初回手動実行完了
- [ ] `docs/data/player.json` が更新されたことを確認
- [ ] ブラウザで `https://old.veryslowstarter.com` にアクセスして動作確認

すべ�チェックボックスが完了すれば、システムは正常に稼働しています！
