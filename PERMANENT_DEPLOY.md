# 🚀 永続的デプロイガイド - 完全版

## ⚠️ Sandbox環境の制限

現在のURL（https://5000-ip2kbkxvu53507tra95yz-b9b802c4.sandbox.novita.ai）は
**Sandbox環境のため一時的**です。数時間〜数日でアクセスできなくなります。

**→ 永続的な公開には、本番環境へのデプロイが必要です。**

---

## 🎯 推奨デプロイ先

### 1. **Render.com**（最も簡単・推奨）

#### 特徴
✅ **無料プランあり**
✅ GitHubから自動デプロイ
✅ 永続的URL
✅ 自動SSL（HTTPS）
✅ 設定が簡単

#### 制限
⚠️ 無料プランは15分アクセスがないとスリープ（復帰に30秒〜1分）
⚠️ 月750時間まで（実質無制限）

#### デプロイ手順

**ステップ1: Render.comアカウント作成**
1. https://render.com にアクセス
2. 「Get Started」をクリック
3. GitHubアカウントでサインアップ

**ステップ2: リポジトリ連携**
1. Renderダッシュボードで「New +」→「Web Service」
2. 「Connect Account」でGitHub連携
3. リポジトリ選択: `Meguroman1978/live_analysis`

**ステップ3: 設定**
```
Name: live-commerce-analysis
Region: Singapore（または最寄り）
Branch: main
Runtime: Python 3
Build Command: ./build.sh
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600 --workers 2
Instance Type: Free
```

**ステップ4: デプロイ**
「Create Web Service」をクリック → 5〜10分待つ

**完成！**
新しい永続URL: `https://live-commerce-analysis.onrender.com`

---

### 2. **Railway.app**（高速・無料枠あり）

#### 特徴
✅ 無料: $5クレジット/月
✅ 非常に高速なデプロイ
✅ スリープなし
✅ 自動デプロイ

#### デプロイ手順

1. https://railway.app にアクセス
2. GitHubでログイン
3. 「New Project」→「Deploy from GitHub repo」
4. `Meguroman1978/live_analysis` を選択
5. 自動デプロイ開始（3〜5分）

**完成！**
新しいURL: `https://live-commerce-analysis.railway.app`

---

### 3. **Heroku**（有名・安定）

#### 特徴
✅ 非常に安定
✅ 豊富なドキュメント
⚠️ 無料プランなし（最低$5/月）

#### デプロイ手順

```bash
# Heroku CLIインストール（Macの場合）
brew install heroku/brew/heroku

# ログイン
heroku login

# アプリ作成
cd /home/user/webapp
heroku create live-commerce-analysis

# デプロイ
git push heroku main

# 完成！
# URL: https://live-commerce-analysis.herokuapp.com
```

---

## 💰 料金比較

| サービス | 無料プラン | 有料プラン | スリープ |
|---------|----------|----------|---------|
| **Render.com** | ✅ あり | $7/月〜 | あり（無料のみ） |
| **Railway** | ✅ $5クレジット | $5/月〜 | なし |
| **Heroku** | ❌ なし | $5/月〜 | なし |

---

## 🎯 用途別推奨

### 個人利用・デモ
→ **Render.com 無料プラン**
- スリープOK
- 完全無料

### ビジネス利用
→ **Railway $5/月** または **Render.com Starter $7/月**
- スリープなし
- 高速レスポンス

### エンタープライズ
→ **AWS/GCP/Azure**
- カスタマイズ可能
- スケーラブル

---

## 📋 必要なファイル（すべて準備済み）

✅ `Procfile` - Gunicorn起動設定
✅ `runtime.txt` - Python 3.12指定
✅ `build.sh` - ビルドスクリプト
✅ `render.yaml` - Render設定
✅ `requirements.txt` - 依存関係

---

## 🔧 デプロイ後の確認

デプロイが完了したら、以下を確認：

1. **URLアクセス**: 新しいURLにアクセス
2. **ファイルアップロード**: 動画・データ・コメントをアップロード
3. **分析実行**: 分析が正常に完了するか
4. **PowerPointダウンロード**: レポートをダウンロード
5. **Gensparkプロンプト**: プロンプト表示を確認

---

## 📝 デプロイ後にやること

### 1. ドキュメントのURL更新

以下のファイルのURLを新しいURLに置き換え：
- `README.md`
- `PUBLIC_ANNOUNCEMENT.md`
- `PUBLIC_GUIDE.md`
- `DEPLOYMENT.md`
- `static/share.html`

### 2. GitHubリポジトリのAboutセクション更新

GitHubリポジトリページで：
1. About（説明）を編集
2. Website: 新しいURLを追加
3. Description: ツールの説明を追加

### 3. SNSでアナウンス

新しい永続URLをシェア！

---

## ⚡ クイックスタート（Render.com推奨）

```bash
# 1. Render.comにアクセス
https://render.com

# 2. GitHubでサインアップ

# 3. New Web Service

# 4. リポジトリ選択
Meguroman1978/live_analysis

# 5. 設定（自動検出）
Name: live-commerce-analysis
Build: ./build.sh
Start: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600
Instance: Free

# 6. Create Web Service

# 完了！新しいURLが発行されます
https://live-commerce-analysis.onrender.com
```

---

## 🎊 次のステップ

1. **Render.comアカウントを作成**
   → https://render.com

2. **上記の手順でデプロイ**
   → 10分で完了

3. **新しいURLを取得**
   → `https://your-app-name.onrender.com`

4. **ドキュメント更新**
   → 古いSandbox URLを新しいURLに置き換え

5. **公開完了！**
   → 永続的に誰でもアクセス可能

---

## 💡 よくある質問

**Q: 無料プランで十分ですか？**
A: 個人利用やデモなら十分です。ビジネス利用なら有料プランを推奨。

**Q: スリープ状態からの復帰は遅いですか？**
A: 30秒〜1分程度です。初回アクセス時のみ。

**Q: カスタムドメインは使えますか？**
A: はい。Render/Railway/Herokuすべて対応しています。

**Q: データベースは必要ですか？**
A: このツールは不要です。ファイルベースで動作します。

**Q: 複数ユーザーの同時利用は可能ですか？**
A: はい。セッションIDで分離されているため、複数ユーザーが同時に使えます。

---

**今すぐRender.comでデプロイしてみましょう！** 🚀
