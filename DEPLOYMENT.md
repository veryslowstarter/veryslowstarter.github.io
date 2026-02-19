# デプロイメント手順

このドキュメントは、プロジェクトを GitHub リポジトリ `veryslowstarter.github.io` にアップロードするための手順です。

## 前提条件

- Git がインストールされている
- GitHub に git ログイン済み（または SSH キー設定済み）
- `veryslowstarter.github.io` リポジトリにプッシュ権限がある

## デプロイメント手順

### 1. リポジトリをクローン

```bash
# リポジトリをクローン
git clone https://github.com/veryslowstarter/veryslowstarter.github.io.git

# ディレクトリに移動
cd veryslowstarter.github.io
```

### 2. ファイルをコピー

現在のプロジェクトから以下のファイルをコピーします：

```bash
# 相対パスで説明（C:\Users\s23t331\LR2IR_Player_Profile から）

# Python スクリプト
copy scraper.py ..\veryslowstarter.github.io\
copy fetch_player_data.py ..\veryslowstarter.github.io\
copy requirements.txt ..\veryslowstarter.github.io\

# docs フォルダ全体
xcopy docs ..\veryslowstarter.github.io\docs /I /Y /E

# .gitignore と README
copy .gitignore ..\veryslowstarter.github.io\
# 注: README.md は既存の内容を保持し、必要に応じてマージ

# .github フォルダ
xcopy .github ..\veryslowstarter.github.io\.github /I /Y /E
```

### 3. ファイル構造確認

```bash
# リポジトリディレクトリで実行
dir /s

# 以下の構造が見える：
# docs/
#   index.html
#   css/style.css
#   js/app.js
#   data/player.json
#   _config.yml
# .github/workflows/
#   update-player-data.yml
# scraper.py
# fetch_player_data.py
# requirements.txt
```

### 4. Git に追加

```bash
# リポジトリルートディレクトリで実行
git add docs/
git add .github/
git add scraper.py
git add fetch_player_data.py
git add requirements.txt
git add .gitignore

# 追加内容を確認
git status
```

### 5. コミット

```bash
git commit -m "feat: add LR2IR player profile auto-update system

- Add scraper.py for LR2IR data fetching
- Add fetch_player_data.py for daily updates
- Add static site to docs/ folder
- Add GitHub Actions workflow for automatic updates
- Configure to display player かぐや (ID: 185532)
- Daily updates at UTC 0:00 (JST 9:00)"
```

### 6. プッシュ

```bash
git push origin main
```

## 設定後の確認

### GitHub Pages 設定確認

1. リポジトリを GitHub で開く：https://github.com/veryslowstarter/veryslowstarter.github.io
2. **Settings** → **Pages** に移動
3. 以下を確認：
   - Source: "Deploy from a branch"
   - Branch: "main" + "/docs" を選択
   - Custom domain: "old.veryslowstarter.com"

### GitHub Actions 設定確認

1. **Settings** → **Actions** → **General** に移動
2. **Workflow permissions**
   - ✅ "Read and write permissions" を選択

### 動作確認

1. **Actions** タブをクリック
2. **Update LR2IR Player Data** ワークフローを確認
3. **Run workflow** をクリックして手動実行
4. 実行完了後、ブラウザで https://old.veryslowstarter.com にアクセス

## トラブルシューティング

### GitHub Pages が動作しない

**DNS キャッシュをクリア：**
```bash
ipconfig /flushdns
```

**ブラウザキャッシュをクリア：**
Ctrl + Shift + Delete で履歴を削除

**強制更新：**
Ctrl + Shift + R

### GitHub Actions ワークフローが失敗

1. Actions タブでエラーログを確認
2. エラーメッセージの内容を読む
3. よくある原因：
   - `requirements.txt` が見つからない
   - ワークフロー権限が不足している
   - LR2IR サイトが一時的に利用不可

### player.json が更新されない

1. `docs/data/player.json` が git で追跡されているか確認
2. コミット時に含まれているか確認
3. `_config.yml` が正しく設定されているか確認

## ローカルテスト（オプション）

GitHub Pages にプッシュする前にローカルでテストする場合：

```bash
# Python 仮想環境を作成
python -m venv venv
venv\Scripts\activate

# パッケージをインストール
pip install -r requirements.txt

# データを取得
python fetch_player_data.py

# Flask サーバーを起動（オプション）
python app.py
```

ブラウザで `http://localhost:5000` にアクセス

## デプロイメント完了

以下が確認できれば、デプロイメントは成功しています：

- [ ] GitHub リポジトリにファイルがプッシュされた
- [ ] GitHub Pages が `https://old.veryslowstarter.com` で起動している
- [ ] page に player profile が表示されている
- [ ] GitHub Actions ワークフローが手動実行で成功した

---

## よくある質問

### Q: 定期更新の時間を変更したい

A: `.github/workflows/update-player-data.yml` の `cron` 値を変更：

```yaml
on:
  schedule:
    - cron: '0 12 * * *'  # UTC 12:00 に変更
```

### Q: 別のプレイヤーを表示したい

A: `fetch_player_data.py` の `player_id` を変更：

```python
scraper = LR2IRScraper(player_id=12345)  # 別の ID に変更
```

その後 push すると、次の自動更新から反映されます。

### Q: 手動でもう一度更新したい

A: GitHub Actions の **Run workflow** ボタンをクリック

### Q: ドメインを変更したい

A: 
1. DNS の CNAME レコードを変更
2. GitHub Pages のカスタムドメイン設定を更新
3. `docs/CNAME` ファイルを更新（GitHub が自動生成する場合は不要）

---

**次のステップ：** `GITHUB_PAGES_SETUP.md` も併せてご覧ください。
