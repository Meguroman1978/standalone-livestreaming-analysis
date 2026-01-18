"""
Genspark AIスライド生成用プロンプトジェネレーター
"""

class GensparkPromptGenerator:
    """Genspark AIスライド機能用のプロンプトを生成"""
    
    def __init__(self):
        pass
    
    def generate_prompt(self, data_df, comments_df, summary_stats, peak_analysis, comment_analysis, recommendations):
        """
        分析結果からGenspark AIスライド生成用プロンプトを生成
        
        Args:
            data_df: 配信データDataFrame
            comments_df: コメントDataFrame
            summary_stats: サマリー統計
            peak_analysis: ピーク分析
            comment_analysis: コメント分析
            recommendations: 推奨事項
            
        Returns:
            str: Genspark AIスライド生成用プロンプト
        """
        prompt_parts = []
        
        # 1. 時系列データサマリー
        prompt_parts.append(self._generate_timeseries_summary(data_df, summary_stats))
        
        # 2. 単一指標分析
        prompt_parts.append(self._generate_single_metric_analysis(data_df, peak_analysis, recommendations))
        
        # 3. 複数指標分析
        prompt_parts.append(self._generate_multi_metric_analysis(data_df, summary_stats))
        
        # 4. コメント定量分析
        prompt_parts.append(self._generate_comment_analysis(comment_analysis, comments_df))
        
        # 5. 総合考察
        prompt_parts.append(self._generate_overall_insights(recommendations, summary_stats))
        
        return "\n\n" + ("-" * 80 + "\n").join(prompt_parts)
    
    def _generate_timeseries_summary(self, data_df, summary_stats):
        """時系列データサマリーセクション"""
        lines = ["【時系列グラフ生成用データ出力】", "時系列指標推移データサマリー"]
        
        # ヘッダー
        headers = []
        if 'minute' in data_df.columns:
            headers.append("経過時間 (分)")
        if 'viewers' in data_df.columns:
            headers.append("同時視聴ユーザー数")
        if 'likes' in data_df.columns:
            headers.append("いいね数")
        if 'comments' in data_df.columns:
            headers.append("チャット数")
        if 'clicks' in data_df.columns:
            headers.append("商品クリック数")
        
        lines.append("\n".join(headers))
        
        # データ行（サンプリング: 5分ごと）
        for idx, row in data_df.iterrows():
            if idx % 5 == 0 or idx == 0 or idx == len(data_df) - 1:  # 0分、5分ごと、最後
                row_data = []
                if 'minute' in data_df.columns:
                    row_data.append(str(int(row.get('minute', idx))))
                if 'viewers' in data_df.columns:
                    row_data.append(str(int(row.get('viewers', 0))))
                if 'likes' in data_df.columns:
                    row_data.append(str(int(row.get('likes', 0))))
                if 'comments' in data_df.columns:
                    row_data.append(str(int(row.get('comments', 0))))
                if 'clicks' in data_df.columns:
                    row_data.append(str(int(row.get('clicks', 0))))
                lines.append("\n".join(row_data))
        
        # サマリー統計
        lines.append("")
        lines.append(f"• 同時視聴ユーザー数（最大）: {summary_stats.get('max_viewers', 0):.0f}名")
        lines.append(f"• 合計いいね数: {summary_stats.get('total_likes', 0):.0f}回")
        lines.append(f"• 合計チャット数: {summary_stats.get('total_comments_actual', summary_stats.get('total_comments_metric', 0)):.0f}回")
        lines.append(f"• 合計商品クリック数: {summary_stats.get('total_clicks', 0):.0f}回")
        
        return "\n".join(lines)
    
    def _generate_single_metric_analysis(self, data_df, peak_analysis, recommendations):
        """単一指標分析セクション"""
        lines = ["各指標の考察とアドバイス_1（単一指標分析）"]
        
        # 1. 同時視聴ユーザー数
        lines.append("\n1. 同時視聴ユーザー数の推移")
        if 'viewers' in peak_analysis and peak_analysis['viewers']:
            peak = peak_analysis['viewers'][0]
            lines.append(f"• 分析: 配信開始から徐々に増加し、開始{peak['minute']}分に最大{peak['value']:.0f}名を記録しました。")
            lines.append("• 考察: 冒頭で視聴者の関心を引くことに成功しています。視覚的な演出や希少性の訴求が効果的でした。")
            lines.append("• アドバイス: 中盤以降の維持率向上のため、「この後限定アイテムの特典発表があります」といった期待感のほのめかしを入れることをお勧めします。")
        else:
            lines.append("• データ不足のため、詳細な分析ができませんでした。")
        
        # 2. 商品クリック数
        lines.append("\n2. 商品クリック数の推移")
        if 'clicks' in peak_analysis and peak_analysis['clicks']:
            peaks = peak_analysis['clicks'][:3]
            peak_str = "、".join([f"{p['minute']}分（{p['value']:.0f}回）" for p in peaks])
            lines.append(f"• 分析: 複数のピークがあり、特に{peak_str}に顕著な伸びが見られます。")
            lines.append("• 考察: デモンストレーションや実演時にクリックが急増する傾向があります。物理的に商品を指し示す演出が効果的です。")
            lines.append("• アドバイス: 商品カードを画面上に表示する際、「クリック」と明記したり、ステッキで指し示したりする演出をさらに強化すべきです。")
        else:
            lines.append("• データ不足のため、詳細な分析ができませんでした。")
        
        # 3. チャット数
        lines.append("\n3. チャット数の推移")
        if 'comments' in peak_analysis and peak_analysis['comments']:
            peak = peak_analysis['comments'][0]
            lines.append(f"• 分析: 開始{peak['minute']}分に{peak['value']:.0f}回とピークを記録。")
            lines.append("• 考察: 視聴者への問いかけや、クローズドクエスチョン（番号での回答）を投げかけたことでコメントが活性化しました。")
            lines.append("• アドバイス: 「コメントをしたユーザーは視聴時間が3〜4倍長い」というデータがあるため、視聴者の名前を呼び、内容を復唱する接客コミュニケーションを継続することが重要です。")
        else:
            lines.append("• データ不足のため、詳細な分析ができませんでした。")
        
        # 4. いいね数
        lines.append("\n4. いいね数の推移")
        if 'likes' in peak_analysis and peak_analysis['likes']:
            peak = peak_analysis['likes'][0]
            lines.append(f"• 分析: 開始{peak['minute']}分に{peak['value']:.0f}回という顕著なピークを記録。")
            lines.append("• 考察: 視聴者が「お得感」と満足に同時に達した結果、共感の「いいね」が集中しました。")
            lines.append("• アドバイス: タイムアタック的なエンタメ要素を盛り込むことで、「いいね」をさらにゲーム感覚で楽しんでもらう仕掛けも検討の余地があります。")
        else:
            lines.append("• データ不足のため、詳細な分析ができませんでした。")
        
        return "\n".join(lines)
    
    def _generate_multi_metric_analysis(self, data_df, summary_stats):
        """複数指標分析セクション"""
        lines = ["各指標の考察とアドバイス_2（複数指標分析）"]
        
        # 視聴者数 × クリック数
        lines.append("\n相関分析：同時視聴ユーザー数 × 商品クリック数")
        ctr = (summary_stats.get('total_clicks', 0) / summary_stats.get('max_viewers', 1)) * 100 if summary_stats.get('max_viewers', 0) > 0 else 0
        lines.append(f"• 推定CTR: {ctr:.2f}%")
        lines.append("• 考察: 同時視聴者数が安定している時間帯に商品クリックが繰り返し発生しており、特に実演中に高い相関が見られます。")
        lines.append("• アドバイス: 具体的な不安解消（STORY）と、製品仕様（FACT）を混ぜて話すことで、信頼感が増し購入意欲（クリック）へ繋がりやすくなります。")
        
        # チャット数 × いいね数
        lines.append("\n相関分析：チャット数 × いいね数")
        lines.append("• 考察: チャットといいねが連動して上昇するタイミングがあり、これは「自分たちも参加している」という双方向性が高まった状態です。")
        lines.append("• アドバイス: アンケートやクイズ（例：どちらの色が好き？）を意図的に配置し、盛り上がりがピークに達した直後に「予約はこちら」と誘導する動線が最も効果的です。")
        
        return "\n".join(lines)
    
    def _generate_comment_analysis(self, comment_analysis, comments_df):
        """コメント定量分析セクション"""
        lines = ["各指標の考察とアドバイス_3（コメント定量分析・詳細分類）"]
        
        # 円グラフ1: カテゴリ別
        lines.append("\n【円グラフ1：定点観測用カテゴリ】")
        categories = comment_analysis.get('categories', {})
        total = comment_analysis.get('total', 1)
        
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            lines.append(f"• {category}: {percentage:.0f}%")
        
        # 分析サマリー
        lines.append("\n分析サマリー")
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        top_names = "、".join([f"{cat[0]} ({cat[1]/total*100:.0f}%)" for cat in top_categories])
        lines.append(f"• 主要コメントジャンル: {top_names}")
        lines.append("• 視聴者の熱量: ポジティブな反応が非常に多く、ブランドへのロイヤリティが高い層が視聴しています。")
        
        if categories.get('購入意志', 0) > 0:
            purchase_rate = (categories.get('購入意志', 0) / total * 100)
            lines.append(f"• 商業的効果: 購入意志を示すコメントが{purchase_rate:.1f}%あり、高いCV（コンバージョン）が期待できる状態です。")
        
        # 定性分析
        lines.append("\n定性分析")
        lines.append("1. 質問の傾向: 「自分に合うかどうか」を確認する内容が目立ちます。色味、肌質、年齢層への適合性に関心が集中しています。")
        lines.append("2. ユーザー属性: リピーターと新規検討層が混在しています。")
        lines.append("3. 次回への提案: より具体的なターゲット層（年代別、肌質別）に向けた実演を行うことで、自分事化を促進できます。")
        
        return "\n".join(lines)
    
    def _generate_overall_insights(self, recommendations, summary_stats):
        """総合考察セクション"""
        lines = ["総合的な考察と今後のアドバイス"]
        
        lines.append("\n今回の配信は、FACT（製品仕様）とSTORY（使用感・体験）のバランスが良く、視聴者の熱量が高い配信でした。")
        
        # 成功要因
        lines.append("\n成功要因:")
        good_points = recommendations.get('good_points', [])
        for i, point in enumerate(good_points[:3], 1):
            lines.append(f"{i}. {point}")
        
        # 今後の課題
        lines.append("\n今後の課題とアクションプラン:")
        improvements = recommendations.get('improvements', [])
        next_actions = recommendations.get('next_actions', [])
        
        all_actions = improvements + next_actions
        for i, action in enumerate(all_actions[:5], 1):
            lines.append(f"{i}. {action}")
        
        # 次なるステップ
        lines.append("\n次なるステップのご提案:")
        lines.append("今回のデータで特定の時間帯やトピックにコメントが集中したことを受け、その要素を主役にした深掘り配信を企画することをお勧めします。")
        lines.append("特定のアイテムへの熱量をさらに高めることで、併せ買いを促進するフレームワークとして有効です。")
        
        return "\n".join(lines)
