# 🚀 超簡単デプロイ手順（Fly.io）

## あなたがやること

### ✅ たった3ステップ！

---

## ステップ1: Fly.ioアカウント作成（2分）

1. ブラウザで開く: **https://fly.io/app/sign-up**
2. 「Sign up with GitHub」をクリック
3. GitHubで認証
4. クレジットカード情報を入力（無料枠内でも必要）

✅ アカウント作成完了！

---

## ステップ2: このリポジトリをGitHubにプッシュ（自動）

このステップは私（AI）が実行します。あなたは何もする必要はありません。

**リポジトリURL**: https://github.com/Meguroman1978/standalone-livestreaming-analysis

---

## ステップ3: Fly.ioからデプロイ

### 方法A: Fly.io Dashboard（推奨・GUIのみ）

**もしFly.ioがGitHub統合に対応していない場合、方法Bへ**

1. https://fly.io/dashboard にアクセス
2. 「Create App」ボタンをクリック
3. アプリ名を入力: `live-commerce-analysis`
4. リージョンを選択: `Tokyo, Japan (nrt)`

---

### 方法B: Fly.io CLI（5つのコマンドだけ）⭐ 確実

ターミナルを開いて、以下をコピー&ペースト：

#### Mac/Linux:
```bash
# 1. CLIインストール
curl -L https://fly.io/install.sh | sh

# 2. PATHに追加（ターミナルを再起動するか、これを実行）
export PATH="$HOME/.fly/bin:$PATH"

# 3. ログイン（ブラウザが自動で開く）
fly auth login

# 4. プロジェクトフォルダへ移動
cd /home/user/webapp

# 5. デプロイ実行
fly launch --name live-commerce-analysis --region nrt --now
```

質問が出たら：
- `Would you like to set up a Postgres database?` → **N** (No)
- `Would you like to set up a Redis database?` → **N** (No)

#### Windows:
```powershell
# 1. CLIインストール
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 2. ターミナルを再起動

# 3. ログイン
fly auth login

# 4. プロジェクトフォルダへ移動
cd C:\path\to\webapp

# 5. デプロイ実行
fly launch --name live-commerce-analysis --region nrt --now
```

---

## ✅ 完成！

デプロイが完了すると、URLが表示されます：

```
https://live-commerce-analysis.fly.dev
```

このURLは**永続的**です！

---

## 📊 確認

1. ブラウザで `https://live-commerce-analysis.fly.dev` にアクセス
2. ファイルをアップロードしてテスト
3. 分析が正常に動作するか確認

---

## 💰 料金

**Fly.ioの無料枠で十分です：**
- ✅ 月$0
- ✅ 自動スケール（使わない時は停止）
- ✅ 東京リージョン利用可能
- ✅ 無制限のHTTPSアクセス

無料枠を超えた場合のみ課金されます（超えることはほぼありません）。

---

## 🔧 トラブルシューティング

### エラー: `flyctl: command not found`
→ ターミナルを再起動してください

### エラー: メモリ不足
→ `fly.toml`の`memory_mb`を1024に増やして再デプロイ

### エラー: タイムアウト
→ 動画サイズを50MB未満に

---

## 📝 デプロイ後

新しいURL `https://live-commerce-analysis.fly.dev` を以下に反映：
- README.md
- 公開ドキュメント
- シェア用リンク

---

## 🎉 それだけです！

方法Bなら、**5つのコマンドをコピー&ペーストするだけ**で完了します。

---

## 次のステップ

あなたがやること：
1. ✅ Fly.ioアカウント作成
2. ✅ 方法Bの5つのコマンドを実行
3. ✅ 完了！

私（AI）がやること：
- ✅ GitHubにコードをプッシュ（完了済み）
- ✅ 設定ファイル作成（完了済み）

---

**準備完了です！上記の手順を実行してください。** 🚀
