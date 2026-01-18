import pandas as pd
import re
from collections import Counter

class CommentAnalyzer:
    """コメント分析クラス"""
    
    def __init__(self, comments_path):
        self.comments_path = comments_path
        self.df = None
    
    def load_and_clean_data(self):
        """
        コメントデータを読み込んでクレンジング
        
        Returns:
            pandas.DataFrame: クレンジング済みコメントデータ
        """
        try:
            # ファイル形式に応じて読み込み
            if self.comments_path.endswith('.csv'):
                self.df = pd.read_csv(self.comments_path, encoding='utf-8-sig')
            elif self.comments_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(self.comments_path)
            else:
                raise Exception("未対応のファイル形式です")
            
            # 列名を正規化
            column_mapping = self._detect_column_names()
            self.df = self.df.rename(columns=column_mapping)
            
            # 必須列のチェック
            if 'comment' not in self.df.columns:
                raise Exception("コメント列が見つかりません")
            
            # 空のコメントを削除
            self.df = self.df[self.df['comment'].notna()]
            self.df = self.df[self.df['comment'].astype(str).str.strip() != '']
            
            # 時間列の処理
            if 'time' in self.df.columns:
                self.df['time'] = pd.to_datetime(self.df['time'], errors='coerce')
            elif 'minute' in self.df.columns:
                self.df['minute'] = pd.to_numeric(self.df['minute'], errors='coerce')
            
            return self.df
            
        except Exception as e:
            raise Exception(f"コメントデータ読み込みエラー: {str(e)}")
    
    def _detect_column_names(self):
        """
        列名を自動検出して標準名にマッピング
        
        Returns:
            dict: 列名マッピング辞書
        """
        mapping = {}
        columns = self.df.columns
        
        # コメント本文
        comment_patterns = ['コメント', 'comment', 'message', 'text', '本文', 'content']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in comment_patterns):
                mapping[col] = 'comment'
                break
        
        # 時間
        time_patterns = ['時間', '時刻', 'time', 'timestamp', '分', 'minute']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in time_patterns):
                mapping[col] = 'time' if 'time' in str(col).lower() or '時刻' in str(col) else 'minute'
                break
        
        # ユーザー名
        user_patterns = ['ユーザー', 'user', 'name', '名前', 'username']
        for col in columns:
            if any(pattern in str(col).lower() for pattern in user_patterns):
                mapping[col] = 'user'
                break
        
        return mapping
    
    def classify_comments(self, comments_df=None):
        """
        コメントを6つのカテゴリに分類
        - 質問
        - 驚き
        - ワクワク・期待
        - 挨拶
        - 購入意志
        - その他
        
        Args:
            comments_df (pandas.DataFrame, optional): コメントデータフレーム
        
        Returns:
            dict: 分類結果
        """
        if comments_df is None:
            comments_df = self.df
        
        if comments_df is None:
            raise Exception("コメントデータが読み込まれていません")
        
        # 分類カテゴリの定義
        categories = {
            '質問': [],
            '驚き': [],
            'ワクワク・期待': [],
            '挨拶': [],
            '購入意志': [],
            'その他': []
        }
        
        # 分類パターン
        question_patterns = [r'？', r'\?', r'ですか', r'ますか', r'どう', r'なに', r'いつ', r'どこ', r'誰', r'何']
        surprise_patterns = [r'すごい', r'えー', r'！', r'!', r'わー', r'おー', r'マジ', r'うそ', r'本当']
        excitement_patterns = [r'楽しみ', r'欲しい', r'気になる', r'いいね', r'素敵', r'かわいい', r'かっこいい', r'ワクワク']
        greeting_patterns = [r'こんにちは', r'こんばんは', r'おはよう', r'初めて', r'はじめまして', r'よろしく', r'来ました']
        purchase_patterns = [r'買', r'購入', r'注文', r'ポチ', r'カート', r'決済', r'買い物', r'ほしい']
        
        for idx, row in comments_df.iterrows():
            comment = str(row['comment'])
            classified = False
            
            # 購入意志（最優先）
            if any(re.search(pattern, comment) for pattern in purchase_patterns):
                categories['購入意志'].append(comment)
                classified = True
            # 質問
            elif any(re.search(pattern, comment) for pattern in question_patterns):
                categories['質問'].append(comment)
                classified = True
            # 驚き
            elif any(re.search(pattern, comment) for pattern in surprise_patterns):
                categories['驚き'].append(comment)
                classified = True
            # ワクワク・期待
            elif any(re.search(pattern, comment) for pattern in excitement_patterns):
                categories['ワクワク・期待'].append(comment)
                classified = True
            # 挨拶
            elif any(re.search(pattern, comment) for pattern in greeting_patterns):
                categories['挨拶'].append(comment)
                classified = True
            
            # その他
            if not classified:
                categories['その他'].append(comment)
        
        # 集計結果
        result = {
            'categories': {k: len(v) for k, v in categories.items()},
            'examples': {k: v[:5] for k, v in categories.items()},  # 各カテゴリの例を5件まで
            'total': len(comments_df)
        }
        
        return result
    
    def analyze_comment_timing(self):
        """
        コメントのタイミング分析
        
        Returns:
            dict: 時系列のコメント数
        """
        if self.df is None:
            raise Exception("コメントデータが読み込まれていません")
        
        if 'minute' in self.df.columns:
            comment_counts = self.df.groupby('minute').size().to_dict()
            return comment_counts
        
        return {}
    
    def get_top_keywords(self, n=20):
        """
        頻出キーワードを抽出
        
        Args:
            n (int): 取得する上位N件
        
        Returns:
            list: (キーワード, 出現回数)のタプルリスト
        """
        if self.df is None:
            return []
        
        # 全コメントを結合
        all_comments = ' '.join(self.df['comment'].astype(str).tolist())
        
        # 簡易的な単語分割（実際はMeCabなどを使用するとより正確）
        words = re.findall(r'\w+', all_comments)
        
        # 1文字の単語や数字のみの単語を除外
        words = [w for w in words if len(w) > 1 and not w.isdigit()]
        
        # 頻出単語をカウント
        word_counts = Counter(words)
        
        return word_counts.most_common(n)
