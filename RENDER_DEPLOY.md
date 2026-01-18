# Render.com デプロイガイド

## 🚀 Render.comで永続的に公開する方法

Render.comは無料プランでFlaskアプリを永続的にホスティングできます。

### 手順

#### 1. Render.comアカウント作成
1. https://render.com にアクセス
2. GitHubアカウントでサインアップ

#### 2. GitHubリポジトリと連携
1. Renderダッシュボードで「New +」→「Web Service」を選択
2. GitHubリポジトリを連携: `https://github.com/Meguroman1978/live_analysis`
3. リポジトリを選択

#### 3. 設定

**Build & Deploy設定:**
- Name: `live-commerce-analysis`（または任意の名前）
- Region: `Singapore`（または最も近いリージョン）
- Branch: `main`
- Root Directory: (空欄)
- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600`

**Environment Variables:**
特に設定不要（デフォルトでOK）

**Instance Type:**
- Free（無料プラン）

#### 4. デプロイ
「Create Web Service」ボタンをクリック

デプロイには5〜10分かかります。完了すると、以下のような永続URLが発行されます：
```
https://live-commerce-analysis.onrender.com
```

### 無料プランの制限

✅ **メリット:**
- 永続的なURL
- 自動SSL（HTTPS）
- 自動デプロイ（GitHubプッシュ時）
- 無料

⚠️ **制限:**
- 15分間アクセスがないとスリープ状態になる
- スリープから復帰に30秒〜1分かかる
- 月750時間まで（実質無制限）

### 有料プランへのアップグレード

スリープなしで常時稼働させたい場合：
- Starter: $7/月
- スリープなし、より高速

---

## 代替案: Heroku

### Heroku デプロイ手順

1. Heroku CLIインストール
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. ログインとデプロイ
```bash
cd /home/user/webapp
heroku login
heroku create live-commerce-analysis
git push heroku main
```

### Heroku 料金
- Eco: $5/月（スリープなし）
- Basic: $7/月

---

## 代替案: Railway

### Railway デプロイ手順

1. https://railway.app にアクセス
2. GitHubアカウントでログイン
3. 「New Project」→「Deploy from GitHub repo」
4. リポジトリを選択
5. 自動デプロイ開始

### Railway 料金
- 無料: $5 クレジット/月（約500時間）
- Developer: $5/月（より多くのリソース）

---

## 推奨デプロイ先

### 用途別推奨

**個人利用・テスト:**
→ **Render.com 無料プラン**（スリープOK）

**ビジネス利用・常時稼働:**
→ **Render.com Starter $7/月** または **Railway $5/月**

**大規模利用:**
→ **AWS/GCP/Azure**（本格的なクラウド）

---

## 次のステップ

1. Render.comアカウントを作成
2. GitHubリポジトリを連携
3. 上記の設定でデプロイ
4. 新しい永続URLを取得
5. READMEとドキュメントを更新

デプロイが完了したら、新しいURLをお知らせください！
