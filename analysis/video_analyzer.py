import cv2
import os
import json
from datetime import timedelta

class VideoAnalyzer:
    """動画分析クラス"""
    
    def __init__(self, video_path, output_folder):
        self.video_path = video_path
        self.output_folder = output_folder
        self.fps = None
        self.total_frames = None
        self.duration_seconds = None
    
    def analyze_video_structure(self):
        """
        動画を分析し、1分ごとのキーイベントを抽出
        
        Returns:
            list: 各分のイベント情報を含む辞書のリスト
        """
        try:
            cap = cv2.VideoCapture(self.video_path)
            
            if not cap.isOpened():
                raise Exception("動画ファイルを開けませんでした")
            
            # 動画の基本情報を取得
            self.fps = cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration_seconds = self.total_frames / self.fps if self.fps > 0 else 0
            
            events = []
            
            # 1分ごとにキーフレームを抽出
            minute = 0
            frames_per_minute = int(self.fps * 60)
            
            while minute * frames_per_minute < self.total_frames:
                frame_number = minute * frames_per_minute
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                
                if ret:
                    # キーフレームを保存
                    thumbnail_path = os.path.join(
                        self.output_folder, 
                        f'frame_min_{minute:02d}.jpg'
                    )
                    cv2.imwrite(thumbnail_path, frame)
                    
                    # 簡易的なシーン情報
                    # 実際の実装では、より高度な画像解析が可能
                    brightness = cv2.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))[0]
                    
                    # シーン推測を追加
                    scene_inference = self._infer_scene_context(minute, brightness)
                    
                    event = {
                        'minute': minute,
                        'timestamp': str(timedelta(seconds=minute * 60)),
                        'frame_number': frame_number,
                        'thumbnail': f'frame_min_{minute:02d}.jpg',
                        'brightness': float(brightness),
                        'description': f'{minute}分目のシーン',
                        'inferred_context': scene_inference
                    }
                    
                    events.append(event)
                
                minute += 1
            
            cap.release()
            
            # 動画情報をメタデータとして保存
            metadata = {
                'fps': self.fps,
                'total_frames': self.total_frames,
                'duration_seconds': self.duration_seconds,
                'duration_minutes': self.duration_seconds / 60,
                'events': events
            }
            
            metadata_path = os.path.join(self.output_folder, 'video_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            return events
            
        except Exception as e:
            raise Exception(f"動画分析エラー: {str(e)}")
    
    def _infer_scene_context(self, minute, brightness):
        """
        シーンの文脈を推測（一般的なライブコマースのパターンに基づく）
        
        Args:
            minute (int): 経過分数
            brightness (float): 画面の明るさ
        
        Returns:
            dict: 推測されるシーン情報
        """
        # 一般的なライブコマースの流れに基づく推測
        inferences = []
        
        if minute == 0:
            inferences.append("配信開始: 挨拶、自己紹介の可能性")
            inferences.append("視聴者への呼びかけ: 「いいね」やコメントの促し")
        elif minute <= 2:
            inferences.append("商品紹介の導入: 本日の商品の概要説明")
            inferences.append("期待感の醸成: 限定性や特別感の訴求")
        elif minute <= 5:
            inferences.append("商品の詳細説明: 特徴や使用方法の紹介")
            inferences.append("実演・デモンストレーション開始の可能性")
        elif minute <= 10:
            inferences.append("商品カード表示の促し: クリック誘導")
            inferences.append("視覚的な商品紹介: 多角的な見せ方")
        elif minute <= 15:
            inferences.append("質問への回答: コメントへの対応")
            inferences.append("購入の促進: 限定性の再強調")
        else:
            inferences.append("まとめと購入の最終促し")
            inferences.append("感謝の言葉と次回予告")
        
        # 明るさに基づく追加推測
        if brightness > 150:
            inferences.append("明るいシーン: 商品のクローズアップや詳細説明の可能性")
        elif brightness < 80:
            inferences.append("暗めのシーン: 雰囲気作りや特定の演出の可能性")
        
        return {
            'likely_actions': inferences,
            'scene_type': self._classify_scene_type(minute)
        }
    
    def _classify_scene_type(self, minute):
        """シーンタイプを分類"""
        if minute == 0:
            return "オープニング"
        elif minute <= 2:
            return "導入"
        elif minute <= 5:
            return "商品紹介（前半）"
        elif minute <= 10:
            return "商品紹介（中盤）・実演"
        elif minute <= 15:
            return "質疑応答・購入促進"
        else:
            return "クロージング"
    
    def get_frame_at_time(self, seconds):
        """
        指定された時間のフレームを取得
        
        Args:
            seconds (float): 取得する時間（秒）
        
        Returns:
            numpy.ndarray: フレーム画像
        """
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)
        ret, frame = cap.read()
        cap.release()
        
        return frame if ret else None
    
    def compress_video_if_needed(self, max_resolution=360):
        """
        動画が大きすぎる場合に圧縮
        
        Args:
            max_resolution (int): 最大解像度（高さ）
        
        Returns:
            str: 圧縮後の動画パス（圧縮不要の場合は元のパス）
        """
        try:
            cap = cv2.VideoCapture(self.video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            if height <= max_resolution:
                return self.video_path
            
            # 圧縮が必要
            compressed_path = os.path.join(
                self.output_folder, 
                f'compressed_{os.path.basename(self.video_path)}'
            )
            
            # ffmpegを使用した圧縮（OpenCVのみで実装）
            cap = cv2.VideoCapture(self.video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # 新しい解像度を計算
            new_height = max_resolution
            new_width = int(width * (new_height / height))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(compressed_path, fourcc, fps, (new_width, new_height))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                resized_frame = cv2.resize(frame, (new_width, new_height))
                out.write(resized_frame)
            
            cap.release()
            out.release()
            
            self.video_path = compressed_path
            return compressed_path
            
        except Exception as e:
            print(f"動画圧縮エラー: {str(e)}")
            return self.video_path
