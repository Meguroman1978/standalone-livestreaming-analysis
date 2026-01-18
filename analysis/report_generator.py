import matplotlib
matplotlib.use('Agg')  # バックエンドを設定（GUIなし環境用）
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime
import numpy as np
from .pptx_generator_enhanced import EnhancedPowerPointGenerator

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

class ReportGenerator:
    """レポート生成クラス"""
    
    def __init__(self, output_folder):
        self.output_folder = output_folder
    
    def generate_report(self, data_df, comments_df, video_events, correlations, comment_analysis):
        """
        総合レポートを生成
        
        Args:
            data_df: 配信データDataFrame
            comments_df: コメントDataFrame
            video_events: 動画イベントリスト
            correlations: 相関分析結果
            comment_analysis: コメント分類結果
        
        Returns:
            dict: レポートデータ
        """
        try:
            # 1. 時系列グラフの生成
            chart_path = self._create_timeline_chart(data_df)
            
            # 2. コメント分類の円グラフ生成
            pie_chart_path = self._create_comment_pie_chart(comment_analysis)
            
            # 3. サマリー統計
            summary_stats = self._calculate_summary_stats(data_df, comments_df)
            
            # 4. ピーク分析
            peak_analysis = self._analyze_peaks(correlations, video_events)
            
            # 5. 改善提案の生成
            recommendations = self._generate_recommendations(
                correlations, 
                comment_analysis, 
                data_df
            )
            
            # レポートデータの構築
            report_data = {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary_stats': summary_stats,
                'charts': {
                    'timeline': chart_path,
                    'comment_pie': pie_chart_path
                },
                'peak_analysis': peak_analysis,
                'comment_analysis': comment_analysis,
                'recommendations': recommendations,
                'video_duration': len(video_events)
            }
            
            # JSONとして保存
            report_path = os.path.join(self.output_folder, 'report.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            # 6. PowerPointレポート生成（correlationsを渡す）
            pptx_path = self._generate_powerpoint_report(
                summary_stats,
                chart_path,
                pie_chart_path,
                comment_analysis,
                recommendations,
                len(video_events),
                correlations  # ピーク情報を渡す
            )
            report_data['pptx_file'] = os.path.basename(pptx_path) if pptx_path else None
            
            return report_data
            
        except Exception as e:
            raise Exception(f"レポート生成エラー: {str(e)}")
    
    def _create_timeline_chart(self, data_df):
        """
        時系列複合グラフを作成
        
        Args:
            data_df: 配信データDataFrame
        
        Returns:
            str: グラフファイルのパス
        """
        try:
            fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
            
            x = data_df.get('minute', range(len(data_df)))
            
            # 視聴者数
            if 'viewers' in data_df.columns:
                axes[0].plot(x, data_df['viewers'], color='#2196F3', linewidth=2, marker='o', markersize=4)
                axes[0].set_ylabel('Viewers', fontsize=12, fontweight='bold')
                axes[0].set_title('Concurrent Viewers', fontsize=14, fontweight='bold')
                axes[0].grid(True, alpha=0.3)
                axes[0].fill_between(x, data_df['viewers'], alpha=0.3, color='#2196F3')
            
            # いいね数
            if 'likes' in data_df.columns:
                axes[1].plot(x, data_df['likes'], color='#E91E63', linewidth=2, marker='o', markersize=4)
                axes[1].set_ylabel('Likes', fontsize=12, fontweight='bold')
                axes[1].set_title('Likes Count', fontsize=14, fontweight='bold')
                axes[1].grid(True, alpha=0.3)
                axes[1].fill_between(x, data_df['likes'], alpha=0.3, color='#E91E63')
            
            # コメント数
            if 'comments' in data_df.columns:
                axes[2].plot(x, data_df['comments'], color='#4CAF50', linewidth=2, marker='o', markersize=4)
                axes[2].set_ylabel('Comments', fontsize=12, fontweight='bold')
                axes[2].set_title('Comments Count', fontsize=14, fontweight='bold')
                axes[2].grid(True, alpha=0.3)
                axes[2].fill_between(x, data_df['comments'], alpha=0.3, color='#4CAF50')
            
            # クリック数
            if 'clicks' in data_df.columns:
                axes[3].plot(x, data_df['clicks'], color='#FF9800', linewidth=2, marker='o', markersize=4)
                axes[3].set_ylabel('Clicks', fontsize=12, fontweight='bold')
                axes[3].set_title('Product Clicks', fontsize=14, fontweight='bold')
                axes[3].grid(True, alpha=0.3)
                axes[3].fill_between(x, data_df['clicks'], alpha=0.3, color='#FF9800')
            
            axes[3].set_xlabel('Time (minutes)', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            
            chart_path = os.path.join(self.output_folder, 'timeline_chart.png')
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return 'timeline_chart.png'
            
        except Exception as e:
            print(f"グラフ作成エラー: {str(e)}")
            return None
    
    def _create_comment_pie_chart(self, comment_analysis):
        """
        コメント分類の円グラフを作成
        
        Args:
            comment_analysis: コメント分類結果
        
        Returns:
            str: グラフファイルのパス
        """
        try:
            categories = comment_analysis['categories']
            
            # データ準備
            labels = list(categories.keys())
            sizes = list(categories.values())
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#BDBDBD']
            
            # 円グラフ作成
            fig, ax = plt.subplots(figsize=(10, 8))
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 12}
            )
            
            # テキストのスタイル設定
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)
            
            ax.set_title('Comment Classification', fontsize=16, fontweight='bold', pad=20)
            
            # 凡例の追加
            ax.legend(
                wedges, 
                [f'{label}: {size}' for label, size in zip(labels, sizes)],
                title="Categories",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                fontsize=10
            )
            
            plt.tight_layout()
            
            pie_chart_path = os.path.join(self.output_folder, 'comment_pie_chart.png')
            plt.savefig(pie_chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return 'comment_pie_chart.png'
            
        except Exception as e:
            print(f"円グラフ作成エラー: {str(e)}")
            return None
    
    def _calculate_summary_stats(self, data_df, comments_df):
        """
        サマリー統計を計算
        
        Returns:
            dict: 統計情報
        """
        stats = {}
        
        if 'viewers' in data_df.columns:
            stats['max_viewers'] = int(data_df['viewers'].max())
            stats['avg_viewers'] = float(data_df['viewers'].mean())
        
        if 'likes' in data_df.columns:
            stats['total_likes'] = int(data_df['likes'].sum())
        
        if 'comments' in data_df.columns:
            stats['total_comments_metric'] = int(data_df['comments'].sum())
        
        if 'clicks' in data_df.columns:
            stats['total_clicks'] = int(data_df['clicks'].sum())
        
        if comments_df is not None:
            stats['total_comments_actual'] = len(comments_df)
        
        return stats
    
    def _analyze_peaks(self, correlations, video_events):
        """
        ピーク分析を実施
        
        Returns:
            dict: ピーク分析結果
        """
        peak_analysis = {}
        
        for metric, peaks in correlations.items():
            if peaks:
                peak_analysis[metric] = []
                for peak in peaks[:5]:  # 上位5件
                    minute = peak['minute']
                    # 対応する動画イベントを探す
                    event = next((e for e in video_events if e['minute'] == minute), None)
                    
                    analysis = {
                        'minute': minute,
                        'value': peak['value'],
                        'increase': peak['increase'],
                        'event_description': event['description'] if event else 'イベント情報なし'
                    }
                    peak_analysis[metric].append(analysis)
        
        return peak_analysis
    
    def _generate_recommendations(self, correlations, comment_analysis, data_df):
        """
        改善提案を生成
        
        Returns:
            dict: 改善提案
        """
        recommendations = {
            'good_points': [],
            'improvements': [],
            'next_actions': []
        }
        
        # Good Points
        if correlations.get('clicks') and len(correlations['clicks']) > 3:
            recommendations['good_points'].append(
                "【商品クリック誘導が効果的】複数のタイミングでクリック数が増加しており、視覚的な商品訴求が成功しています。"
            )
        
        if comment_analysis['categories'].get('購入意志', 0) > comment_analysis['total'] * 0.1:
            recommendations['good_points'].append(
                "【購入意欲の高いコメントが多い】視聴者の購買意欲を引き出すことに成功しています。"
            )
        
        # Improvements
        if 'viewers' in data_df.columns:
            viewer_retention = data_df['viewers'].iloc[-1] / data_df['viewers'].max() if data_df['viewers'].max() > 0 else 0
            if viewer_retention < 0.5:
                recommendations['improvements'].append(
                    "【視聴維持率の改善】配信後半で視聴者が大幅に減少しています。中盤に複数の山場を設けて離脱を防ぎましょう。"
                )
        
        if comment_analysis['categories'].get('質問', 0) > comment_analysis['total'] * 0.2:
            recommendations['improvements'].append(
                "【質問への即応性向上】質問コメントが多いため、リアルタイムでの回答を強化することでエンゲージメントが向上します。"
            )
        
        # Next Actions
        recommendations['next_actions'].append(
            "冒頭30秒で「今日の配信で得られる3つのメリット」を明示する（相手ありきの原則）"
        )
        recommendations['next_actions'].append(
            "商品を常に画面中央に配置し、前後の動きでオートフォーカスを活用する（魅せる技術）"
        )
        recommendations['next_actions'].append(
            "「残り○個」「あと○分」などの限定性を強調して「今」買う理由を提示する（鉄則）"
        )
        
        return recommendations
    
    def _generate_powerpoint_report(self, summary_stats, chart_path, pie_chart_path, comment_analysis, recommendations, video_duration, correlations):
        """
        PowerPointレポートを生成（12スライド版）
        
        Returns:
            str: PPTXファイルパス
        """
        try:
            # 強化版PowerPointGenerator初期化
            pptx_gen = EnhancedPowerPointGenerator(self.output_folder)
            
            # ピーク分析データの準備（correlationsを使用）
            peak_info = correlations  # correlationsがそのままpeak_info
            
            # フルパスの準備
            timeline_chart_full_path = os.path.join(self.output_folder, chart_path)
            pie_chart_full_path = os.path.join(self.output_folder, pie_chart_path)
            
            print("[INFO] 12スライドのPowerPointレポートを生成中...")
            
            # 1. カバーページ
            pptx_gen.create_slide_1_cover(summary_stats, video_duration)
            print("[INFO]   ✓ スライド1: カバーページ")
            
            # 2. 主要KPIサマリー
            pptx_gen.create_slide_2_kpi_summary(summary_stats, peak_info)
            print("[INFO]   ✓ スライド2: 主要KPIサマリー")
            
            # 3. 時系列(1) 同時視聴ユーザー数
            pptx_gen.create_slide_3_timeline_viewers(timeline_chart_full_path, peak_info)
            print("[INFO]   ✓ スライド3: 時系列(1) 視聴者数")
            
            # 4. 時系列(2) 商品クリック数
            pptx_gen.create_slide_4_timeline_clicks(timeline_chart_full_path, peak_info)
            print("[INFO]   ✓ スライド4: 時系列(2) クリック数")
            
            # 5. 時系列(3) いいね数とチャット数
            pptx_gen.create_slide_5_timeline_engagement(timeline_chart_full_path, peak_info)
            print("[INFO]   ✓ スライド5: 時系列(3) エンゲージメント")
            
            # 6. 単一指標分析｜同時視聴ユーザー数
            pptx_gen.create_slide_6_single_metric_viewers(peak_info, recommendations)
            print("[INFO]   ✓ スライド6: 単一指標分析(視聴者)")
            
            # 7. 単一指標分析｜商品クリック数
            pptx_gen.create_slide_7_single_metric_clicks(peak_info, recommendations)
            print("[INFO]   ✓ スライド7: 単一指標分析(クリック)")
            
            # 8. 単一指標分析｜チャット＆いいね
            pptx_gen.create_slide_8_single_metric_engagement(peak_info, recommendations)
            print("[INFO]   ✓ スライド8: 単一指標分析(エンゲージメント)")
            
            # 9. 複数指標分析｜視聴×クリックの相関
            pptx_gen.create_slide_9_multi_metric_correlation(summary_stats, peak_info, recommendations)
            print("[INFO]   ✓ スライド9: 複数指標分析(相関)")
            
            # 10. コメント定量分析
            pptx_gen.create_slide_10_comment_analysis(comment_analysis, pie_chart_full_path)
            print("[INFO]   ✓ スライド10: コメント定量分析")
            
            # 11. 総合考察｜成功要因と課題
            pptx_gen.create_slide_11_overall_insights(recommendations, summary_stats)
            print("[INFO]   ✓ スライド11: 総合考察")
            
            # 12. アクションプラン（次回配信）
            pptx_gen.create_slide_12_action_plan(recommendations)
            print("[INFO]   ✓ スライド12: アクションプラン")
            
            # 保存
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"live_commerce_analysis_report_{timestamp}.pptx"
            pptx_path = pptx_gen.save(filename)
            
            print(f"[INFO] PowerPointレポート生成完了: {pptx_path}")
            print(f"[INFO] 総スライド数: 12")
            return pptx_path
            
        except Exception as e:
            print(f"[ERROR] PowerPoint生成エラー: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _prepare_peak_info_for_pptx(self, recommendations):
        """PPTXスライド生成用にピーク情報を準備"""
        # recommendations から peak_analysis を抽出
        # （実際にはgenerate_report内でcorrelationsを渡す方が良いが、
        #  後方互換性のためrecommendationsに含まれていると仮定）
        peak_info = {
            'viewers': [],
            'clicks': [],
            'likes': [],
            'comments': []
        }
        
        # recommendations内にpeak情報があれば使用、なければ空
        # （注: 本来はcorrelationsを直接渡すべきだが、現在の実装に合わせる）
        return peak_info
