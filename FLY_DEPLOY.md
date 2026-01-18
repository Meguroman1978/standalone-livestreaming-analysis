# Fly.io デプロイガイド（最も簡単な方法）

## 🚀 Fly.ioでデプロイする手順

### 前提条件
- GitHubアカウント（既にお持ち）
- クレジットカード（無料枠内でも登録必要）

---

## 方法1: Fly.io Dashboard（GUIのみ、コマンド不要）⭐ 推奨

### ステップ1: Fly.ioアカウント作成
1. https://fly.io/app/sign-up にアクセス
2. GitHubアカウントでサインアップ
3. クレジットカード情報を登録（無料枠内でも必要）

### ステップ2: GitHubからデプロイ
1. Fly.io ダッシュボードにログイン: https://fly.io/dashboard
2. 右上の「Create App」をクリック
3. 「Deploy from GitHub」を選択
4. リポジトリを選択: `Meguroman1978/standalone-livestreaming-analysis`
5. ブランチを選択: `main`

### ステップ3: アプリ設定
```
App Name: live-commerce-analysis
Region: Tokyo, Japan (nrt)
```

### ステップ4: 自動デプロイ
- fly.tomlファイルが自動検出されます
- 「Deploy」ボタンをクリック
- 5〜10分待つ

### ✅ 完成！
デプロイ完了後、URLが表示されます：
```
https://live-commerce-analysis.fly.dev
```

---

## 方法2: Fly.io CLI（もしターミナルを使える場合）

もしターミナルを少しだけ使ってもいい場合は、こちらの方が確実です。

### ステップ1: Fly.io CLIインストール（Mac）
ターミナルを開いて：
```bash
curl -L https://fly.io/install.sh | sh
```

### ステップ2: ログイン
```bash
fly auth login
```
→ ブラウザが開くので、GitHubでログイン

### ステップ3: デプロイ
```bash
cd /home/user/webapp
fly launch
```

質問に答える：
- App Name: `live-commerce-analysis`（または任意）
- Region: `nrt`（Tokyo）
- Would you like to set up a Postgres database? → **No**
- Would you like to set up a Redis database? → **No**
- Would you like to deploy now? → **Yes**

### ✅ 完成！
数分後にデプロイ完了。URLが表示されます。

---

## 💰 料金（無料枠）

Fly.ioの無料枠：
- ✅ 最大3つのアプリ
- ✅ 共有CPU 1コア
- ✅ メモリ 256MB（1つのアプリ）
- ✅ ストレージ 3GB
- ✅ 月160時間の稼働時間（実質無制限）
- ✅ 自動スケール（アクセスがない時は停止）

このツールは無料枠内で十分動作します！

---

## 🔧 デプロイ後の確認

1. URLにアクセス: `https://live-commerce-analysis.fly.dev`
2. ファイルをアップロード
3. 分析を実行
4. PowerPointダウンロードを確認

---

## ⚠️ もしエラーが出た場合

### メモリ不足エラー
fly.tomlの`memory_mb`を増やす：
```toml
memory_mb = 1024  # 512から1024に変更
```

### タイムアウトエラー
大きな動画ファイルの場合、処理時間がかかります。
推奨: 動画サイズ50MB未満

---

## 📝 デプロイ後にやること

### 1. ドキュメントのURL更新
新しいURL: `https://live-commerce-analysis.fly.dev`

更新が必要なファイル：
- README.md
- PUBLIC_ANNOUNCEMENT.md
- PUBLIC_GUIDE.md
- DEPLOYMENT.md
- static/share.html

### 2. GitHubリポジトリの説明を更新
リポジトリページで：
- About → Website: `https://live-commerce-analysis.fly.dev`
- Description: ライブコマース配信分析ツール

### 3. 自動デプロイ設定（オプション）
GitHubにプッシュしたら自動でデプロイされるように設定可能。

---

## 🎊 推奨デプロイ方法

**あなたの希望（ターミナル最小限）なら：**

### 👉 方法1を推奨
1. Fly.io Dashboard (https://fly.io/dashboard) にアクセス
2. 「Create App」→「Deploy from GitHub」
3. リポジトリ選択してデプロイ

これだけです！

---

## 🆘 もし方法1がうまくいかない場合

Fly.ioのGUIデプロイがうまくいかない場合は、
**ターミナルで5つのコマンドだけ**実行してください：

```bash
# 1. CLIインストール
curl -L https://fly.io/install.sh | sh

# 2. ログイン（ブラウザが開く）
fly auth login

# 3. プロジェクトフォルダへ移動
cd /home/user/webapp

# 4. デプロイ
fly launch

# 5. 確認（URLが表示される）
fly status
```

これで永続的にデプロイ完了です！🚀

---

## 次のステップ

1. Fly.ioアカウント作成: https://fly.io/app/sign-up
2. 上記の方法1でGUIデプロイ
3. URLを取得
4. ドキュメント更新
5. 公開完了！
