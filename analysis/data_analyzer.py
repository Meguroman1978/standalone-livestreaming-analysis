import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataAnalyzer:
    """配信データ分析クラス"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
    
    def load_and_clean_data(self):
        """
        データを読み込んでクレンジング
        
        Returns:
            pandas.DataFrame: クレンジング済みデータフレーム
        """
        try:
            # ファイル形式に応じて読み込み
            if self.data_path.endswith('.csv'):
                self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            elif self.data_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(self.data_path)
            else:
                raise Exception("未対応のファイル形式です")
            
            # 列名を正規化（よくある列名パターンに対応）
            column_mapping = self._detect_column_names()
            self.df = self.df.rename(columns=column_mapping)
            
            # 時間列の処理
            if 'time' in self.df.columns:
                self.df['time'] = pd.to_datetime(self.df['time'], errors='coerce')
            elif 'minute' in self.df.columns:
                self.df['minute'] = pd.to_numeric(self.df['minute'], errors='coerce')
            else:
                # 時間列がない場合は分単位のインデックスを作成
                self.df['minute'] = range(len(self.df))
            
            # 数値列の処理
            numeric_columns = ['viewers', 'likes', 'comments', 'clicks']
            for col in numeric_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
            
            # NaNを0で埋める
            self.df = self.df.fillna(0)
            
            return self.df
            
        except Exception as e:
            raise Exception(f"データ読み込みエラー: {str(e)}")
    
    def _detect_column_names(self):
        """
        列名を自動検出して標準名にマッピング
        
        Returns:
            dict: 列名マッピング辞書
        """
        mapping = {}
        columns = self.df.columns
        
        # 時間関連
        time_patterns = ['時間', '時刻', 'time', 'timestamp', '分', 'minute']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in time_patterns):
                mapping[col] = 'time' if 'time' in str(col).lower() or '時' in str(col) else 'minute'
                break
        
        # 視聴者数
        viewer_patterns = ['視聴', 'viewer', 'watch', '同時', 'concurrent']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in viewer_patterns):
                mapping[col] = 'viewers'
                break
        
        # いいね数
        like_patterns = ['いいね', 'like', 'favorite', 'heart']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in like_patterns):
                mapping[col] = 'likes'
                break
        
        # コメント数
        comment_patterns = ['コメント', 'comment', 'chat', 'チャット']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in comment_patterns):
                mapping[col] = 'comments'
                break
        
        # クリック数
        click_patterns = ['クリック', 'click', '商品', 'product']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in click_patterns):
                mapping[col] = 'clicks'
                break
        
        return mapping
    
    def get_summary_statistics(self):
        """
        サマリー統計を計算
        
        Returns:
            dict: 統計情報
        """
        if self.df is None:
            raise Exception("データが読み込まれていません")
        
        stats = {}
        
        if 'viewers' in self.df.columns:
            stats['max_viewers'] = int(self.df['viewers'].max())
            stats['avg_viewers'] = float(self.df['viewers'].mean())
        
        if 'likes' in self.df.columns:
            stats['total_likes'] = int(self.df['likes'].sum())
        
        if 'comments' in self.df.columns:
            stats['total_comments'] = int(self.df['comments'].sum())
        
        if 'clicks' in self.df.columns:
            stats['total_clicks'] = int(self.df['clicks'].sum())
        
        return stats
    
    def find_peaks(self, column, threshold_percentile=75):
        """
        指定列のピーク（急増ポイント）を検出
        
        Args:
            column (str): 分析対象の列名
            threshold_percentile (int): ピーク判定の閾値パーセンタイル
        
        Returns:
            list: ピーク情報のリスト
        """
        if self.df is None or column not in self.df.columns:
            return []
        
        # 前後の差分を計算
        self.df[f'{column}_diff'] = self.df[column].diff().fillna(0)
        
        # 閾値を計算
        threshold = self.df[f'{column}_diff'].quantile(threshold_percentile / 100)
        
        # ピークを検出
        peaks = []
        for idx, row in self.df.iterrows():
            if row[f'{column}_diff'] >= threshold and row[f'{column}_diff'] > 0:
                peak_info = {
                    'minute': int(row.get('minute', idx)),
                    'value': float(row[column]),
                    'increase': float(row[f'{column}_diff']),
                    'metric': column
                }
                peaks.append(peak_info)
        
        return peaks
    
    def correlate_with_events(self, video_events):
        """
        データのピークと動画イベントを関連付け
        
        Args:
            video_events (list): 動画イベントのリスト
        
        Returns:
            dict: 相関分析結果
        """
        correlations = {
            'viewers': self.find_peaks('viewers'),
            'likes': self.find_peaks('likes'),
            'comments': self.find_peaks('comments'),
            'clicks': self.find_peaks('clicks')
        }
        
        return correlations
