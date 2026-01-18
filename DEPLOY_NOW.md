# 🚀 今すぐデプロイ - 簡単3ステップ

## ✅ すでに完了していること

- ✅ GitHubへのプッシュ完了
- ✅ リポジトリ: https://github.com/Meguroman1978/standalone-livestreaming-analysis
- ✅ 演者行動推測機能の実装完了
- ✅ CTR計算の修正完了（100%を超えないように）

---

## 🎯 あなたがやること（3ステップのみ）

### ステップ1️⃣: Fly.ioアカウント作成（2分）

1. https://fly.io/app/sign-up にアクセス
2. 「Sign up with GitHub」をクリック
3. GitHubアカウントでログイン
4. クレジットカード情報を登録（無料枠の範囲内で使用可能）

### ステップ2️⃣: Fly.io CLIのインストール（1分）

ターミナルで以下のコマンドを**順番に**実行：

```bash
# CLIをインストール
curl -L https://fly.io/install.sh | sh

# PATHを通す
export PATH="$HOME/.fly/bin:$PATH"
```

### ステップ3️⃣: デプロイ実行（2分）

ターミナルで以下のコマンドを**順番に**実行：

```bash
# Fly.ioにログイン（ブラウザが開きます）
fly auth login

# プロジェクトディレクトリに移動
cd /home/user/webapp

# デプロイ実行！
fly launch --name live-commerce-analysis --region nrt --now
```

**重要**: デプロイ中に質問が出たら、**すべて「N」と答えてください**：
- `Would you like to set up a Postgresql database now?` → **N**
- `Would you like to set up an Upstash Redis database now?` → **N**

---

## 🎉 完成！

デプロイが完了すると、以下のURLで公開されます：

### 🌐 公開URL
**https://live-commerce-analysis.fly.dev**

このURLをブラウザで開けば、誰でもツールを使えます！

---

## 📋 新機能の確認ポイント

デプロイ後、以下を確認してください：

### 1. PowerPointレポート内の新機能
- ✅ 各指標のピーク分析に「演者行動推測」が追加されている
- ✅ 例：「いいね数急増 → 💡 演者がいいね依頼をした可能性」
- ✅ 例：「クリック数急増 → 💡 演者が商品カードクリックを促した可能性」

### 2. CTR計算の修正
- ✅ CTRが100%を超えないように修正済み
- ✅ 計算式: `総クリック数 ÷ 総視聴者数累計 × 100`

### 3. Gensparkプロンプトの改善
- ✅ 演者行動分析が含まれている
- ✅ より詳細な考察が生成される

---

## 🔧 トラブルシューティング

### エラー: `flyctl: command not found`
→ ターミナルを再起動してから、再度 `export PATH="$HOME/.fly/bin:$PATH"` を実行

### エラー: `Error: failed to fetch an image`
→ 数分待ってから `fly deploy` を再実行

### メモリ不足エラー
→ `fly.toml` の `memory_mb = 512` を `memory_mb = 1024` に変更してから再デプロイ

---

## 💰 料金について

**Fly.io 無料枠**で十分に運用できます：
- ✅ 月額 $0
- ✅ 使用していない時は自動でスリープ
- ✅ アクセスがあると自動で起動

---

## 📞 サポート

問題があれば、以下のドキュメントを参照してください：
- `EASY_DEPLOY.md` - デプロイの詳細手順
- `FLY_DEPLOY.md` - Fly.io固有の設定
- `TROUBLESHOOTING.md` - よくある問題と解決方法

---

## 🎊 実装完了内容のまとめ

### 演者行動推測機能
- 各指標のピーク時に、演者がどのような行動をした可能性があるかを推測
- 具体例：
  - いいね急増 → 「いいねをお願いします」発言の可能性
  - クリック急増 → 「商品カードをクリック」促進の可能性
  - コメント急増 → 質問投げかけの可能性
  - 視聴者急増 → 注目トピック提示の可能性

### CTR計算修正
- 旧: `総クリック数 ÷ 最大視聴者数 × 100` (100%超える可能性あり)
- 新: `総クリック数 ÷ 総視聴者数累計 × 100` (100%を超えない)

### スライドへの反映
- PowerPointの各指標スライドに「💡 推測される演者の行動」セクション追加
- Gensparkプロンプトにも同様の考察を含める

---

**🚀 準備完了！あとはステップ1〜3を実行するだけです！**
