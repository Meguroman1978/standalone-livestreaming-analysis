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
            # ファイルパスの確認
            import os
            if not os.path.exists(self.comments_path):
                raise Exception(f"ファイルが見つかりません: {self.comments_path}")
            
            # ファイル形式に応じて読み込み
            file_ext = self.comments_path.lower().split('.')[-1]
            
            if file_ext == 'csv':
                try:
                    self.df = pd.read_csv(self.comments_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    # Try different encodings
                    try:
                        self.df = pd.read_csv(self.comments_path, encoding='shift-jis')
                    except:
                        self.df = pd.read_csv(self.comments_path, encoding='cp932')
            elif file_ext in ['xlsx', 'xls']:
                self.df = pd.read_excel(self.comments_path)
            else:
                raise Exception(f"未対応のファイル形式です: .{file_ext} (対応形式: .csv, .xlsx, .xls)")
            
            # データが空でないか確認
            if self.df.empty:
                raise Exception("ファイルにデータがありません")
            
            # 列名を正規化
            column_mapping = self._detect_column_names()
            if column_mapping:
                self.df = self.df.rename(columns=column_mapping)
            
            # 必須列のチェック
            if 'comment' not in self.df.columns:
                available_columns = ', '.join(self.df.columns.tolist())
                raise Exception(f"コメント列が見つかりません。利用可能な列: {available_columns}")
            
            # 空のコメントを削除
            self.df = self.df[self.df['comment'].notna()]
            self.df = self.df[self.df['comment'].astype(str).str.strip() != '']
            
            if self.df.empty:
                raise Exception("有効なコメントデータがありません")
            
            # 時間列の処理
            if 'elapsed_time' in self.df.columns:
                # elapsed_timeは秒数なので分に変換
                self.df['minute'] = (self.df['elapsed_time'] / 60).astype(int)
            elif 'time' in self.df.columns:
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
        
        # コメント本文（より具体的なパターンを優先）
        comment_patterns = [
            ('original_text', 10),  # 最優先
            ('original', 9),
            ('text', 8),
            ('コメント', 7),
            ('comment', 6),
            ('message', 5),
            ('本文', 4),
            ('content', 3)
        ]
        
        best_match = None
        best_priority = -1
        
        for col in columns:
            col_lower = str(col).lower()
            for pattern, priority in comment_patterns:
                if pattern in col_lower:
                    if priority > best_priority:
                        best_match = col
                        best_priority = priority
                        break
        
        if best_match:
            mapping[best_match] = 'comment'
        
        # 時間
        time_patterns = ['時間', '時刻', 'time', 'timestamp', '分', 'minute', 'elapsed']
        for col in columns:
            col_lower = str(col).lower()
            if any(pattern in col_lower for pattern in time_patterns):
                # elapsed_timeは秒数なので分に変換する必要がある
                if 'elapsed' in col_lower:
                    mapping[col] = 'elapsed_time'
                elif 'time' in col_lower or '時' in str(col):
                    mapping[col] = 'time'
                else:
                    mapping[col] = 'minute'
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
        コメントを6つのカテゴリに分類（タイムスタンプ付き）
        - 質問
        - 驚き
        - ワクワク・期待
        - 挨拶
        - 購入意志
        - その他
        
        Args:
            comments_df (pandas.DataFrame, optional): コメントデータフレーム
        
        Returns:
            dict: 分類結果（タイムスタンプと具体的なコメント内容を含む）
        """
        if comments_df is None:
            comments_df = self.df
        
        if comments_df is None:
            raise Exception("コメントデータが読み込まれていません")
        
        # 分類カテゴリの定義（タイムスタンプ付き）
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
            
            # タイムスタンプ情報を取得
            timestamp_info = self._get_timestamp_info(row)
            
            # コメント情報を構造化
            comment_data = {
                'text': comment,
                'timestamp': timestamp_info,
                'user': row.get('user', '不明') if 'user' in row else '不明'
            }
            
            # 購入意志（最優先）
            if any(re.search(pattern, comment) for pattern in purchase_patterns):
                categories['購入意志'].append(comment_data)
                classified = True
            # 質問
            elif any(re.search(pattern, comment) for pattern in question_patterns):
                categories['質問'].append(comment_data)
                classified = True
            # 驚き
            elif any(re.search(pattern, comment) for pattern in surprise_patterns):
                categories['驚き'].append(comment_data)
                classified = True
            # ワクワク・期待
            elif any(re.search(pattern, comment) for pattern in excitement_patterns):
                categories['ワクワク・期待'].append(comment_data)
                classified = True
            # 挨拶
            elif any(re.search(pattern, comment) for pattern in greeting_patterns):
                categories['挨拶'].append(comment_data)
                classified = True
            
            # その他
            if not classified:
                categories['その他'].append(comment_data)
        
        # 集計結果
        result = {
            'categories': {k: len(v) for k, v in categories.items()},
            'examples': {k: v[:10] for k, v in categories.items()},  # 各カテゴリの例を10件まで
            'detailed_comments': categories,  # 全コメント（タイムスタンプ付き）
            'total': len(comments_df)
        }
        
        return result
    
    def _get_timestamp_info(self, row):
        """
        タイムスタンプ情報を取得してフォーマット
        
        Args:
            row: DataFrameの行
        
        Returns:
            str: フォーマットされたタイムスタンプ（例：「2分30秒」）
        """
        if 'elapsed_time' in row.index and pd.notna(row['elapsed_time']):
            seconds = int(row['elapsed_time'])
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}分{secs:02d}秒"
        elif 'minute' in row.index and pd.notna(row['minute']):
            return f"{int(row['minute'])}分"
        elif 'time' in row.index and pd.notna(row['time']):
            return str(row['time'])
        else:
            return "時刻不明"
    
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
