from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from analysis.video_analyzer import VideoAnalyzer
from analysis.data_analyzer import DataAnalyzer
from analysis.comment_analyzer import CommentAnalyzer
from analysis.report_generator import ReportGenerator

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_VIDEO_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'mkv'}
app.config['ALLOWED_DATA_EXTENSIONS'] = {'csv', 'xlsx', 'xls'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """ファイルアップロードエンドポイント"""
    try:
        # Check if files are present
        if 'video' not in request.files:
            return jsonify({'error': '動画ファイルがアップロードされていません'}), 400
        if 'data' not in request.files:
            return jsonify({'error': '配信データがアップロードされていません'}), 400
        if 'comments' not in request.files:
            return jsonify({'error': 'コメントデータがアップロードされていません'}), 400
        
        video_file = request.files['video']
        data_file = request.files['data']
        comments_file = request.files['comments']
        
        # Validate files
        if video_file.filename == '' or data_file.filename == '' or comments_file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        if not allowed_file(video_file.filename, app.config['ALLOWED_VIDEO_EXTENSIONS']):
            return jsonify({'error': '動画ファイルの形式が無効です'}), 400
        
        if not allowed_file(data_file.filename, app.config['ALLOWED_DATA_EXTENSIONS']):
            return jsonify({'error': '配信データの形式が無効です（CSV/Excelのみ）'}), 400
        
        if not allowed_file(comments_file.filename, app.config['ALLOWED_DATA_EXTENSIONS']):
            return jsonify({'error': 'コメントデータの形式が無効です（CSV/Excelのみ）'}), 400
        
        # Create unique session folder
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_folder, exist_ok=True)
        
        # Save files with proper extension handling
        def safe_filename(original_filename):
            """
            ファイル名を安全にしつつ、拡張子を確実に保持
            """
            # 拡張子を取得
            if '.' in original_filename:
                name, ext = original_filename.rsplit('.', 1)
                # secure_filenameを適用
                safe_name = secure_filename(name)
                # 拡張子が失われた場合のフォールバック
                if not safe_name:
                    safe_name = 'file'
                return f"{safe_name}.{ext.lower()}"
            else:
                return secure_filename(original_filename) or 'file'
        
        video_filename = safe_filename(video_file.filename)
        data_filename = safe_filename(data_file.filename)
        comments_filename = safe_filename(comments_file.filename)
        
        video_path = os.path.join(session_folder, video_filename)
        data_path = os.path.join(session_folder, data_filename)
        comments_path = os.path.join(session_folder, comments_filename)
        
        video_file.save(video_path)
        data_file.save(data_path)
        comments_file.save(comments_path)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'ファイルのアップロードが完了しました'
        })
        
    except Exception as e:
        return jsonify({'error': f'アップロードエラー: {str(e)}'}), 500

@app.route('/api/analyze/<session_id>', methods=['POST'])
def analyze(session_id):
    """分析実行エンドポイント"""
    try:
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        
        if not os.path.exists(session_folder):
            return jsonify({'error': 'セッションが見つかりません'}), 404
        
        # Find uploaded files
        files = os.listdir(session_folder)
        video_file = None
        data_file = None
        comments_file = None
        
        # Separate files by type
        video_files = []
        data_files = []
        
        print(f"[DEBUG] Session folder: {session_folder}")
        print(f"[DEBUG] Files in folder: {files}")
        
        for f in files:
            full_path = os.path.join(session_folder, f)
            print(f"[DEBUG] Checking file: {f}")
            # Check if it's a video file
            if any(f.lower().endswith('.' + ext) for ext in app.config['ALLOWED_VIDEO_EXTENSIONS']):
                video_files.append(full_path)
                print(f"[DEBUG] -> Video file")
            # Check if it's a data file (CSV/Excel)
            elif any(f.lower().endswith('.' + ext) for ext in app.config['ALLOWED_DATA_EXTENSIONS']):
                data_files.append(full_path)
                print(f"[DEBUG] -> Data file")
            else:
                print(f"[DEBUG] -> Ignored (no matching extension)")
        
        print(f"[DEBUG] Video files: {video_files}")
        print(f"[DEBUG] Data files: {data_files}")
        
        # Assign video file
        if video_files:
            video_file = video_files[0]
        
        # Detect data and comments files by content (column structure)
        if len(data_files) < 2:
            return jsonify({'error': '配信データ（分チャート）とコメントデータの両方が必要です。2つのCSV/Excelファイルをアップロードしてください。'}), 400
        
        # Analyze each file's column structure to determine which is which
        import pandas as pd
        
        def detect_file_type(file_path):
            """
            ファイルの内容を読み込んで、配信データかコメントデータかを判定
            Returns: 'streaming_data', 'comment_data', or 'unknown'
            """
            try:
                # Read file
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, nrows=5, encoding='utf-8-sig')
                else:
                    df = pd.read_excel(file_path, nrows=5)
                
                columns = [str(col).lower() for col in df.columns]
                
                # Check for streaming data patterns (時間 + 複数の数値指標)
                has_time = any(pattern in ' '.join(columns) for pattern in ['時間', '分', 'minute', 'time', '経過'])
                has_viewers = any(pattern in ' '.join(columns) for pattern in ['視聴', 'viewer', '同時', 'ユーザー'])
                has_metrics = any(pattern in ' '.join(columns) for pattern in ['いいね', 'like', 'クリック', 'click', 'チャット', 'chat'])
                
                # Check for comment data patterns (コメント本文 + 時間)
                has_comment_text = any(pattern in ' '.join(columns) for pattern in ['original_text', 'comment', 'text', 'コメント', 'message'])
                has_user = any(pattern in ' '.join(columns) for pattern in ['user', 'username', 'ユーザー'])
                
                # Determine file type
                if has_comment_text and (has_time or has_user):
                    return 'comment_data'
                elif has_time and (has_viewers or has_metrics):
                    return 'streaming_data'
                else:
                    return 'unknown'
                    
            except Exception as e:
                print(f"Error detecting file type for {file_path}: {str(e)}")
                return 'unknown'
        
        # Detect file types
        file_types = {}
        for df_path in data_files:
            file_type = detect_file_type(df_path)
            file_types[df_path] = file_type
        
        # Assign files based on detected types
        for df_path, file_type in file_types.items():
            if file_type == 'streaming_data' and not data_file:
                data_file = df_path
            elif file_type == 'comment_data' and not comments_file:
                comments_file = df_path
        
        # If still not assigned, try filename patterns as fallback
        if not data_file or not comments_file:
            for df_path in data_files:
                filename = os.path.basename(df_path).lower()
                if not data_file and ('data' in filename or '配信' in filename or 'chart' in filename or 'チャート' in filename):
                    data_file = df_path
                elif not comments_file and ('comment' in filename or 'コメント' in filename or 'chat' in filename):
                    comments_file = df_path
        
        # Last resort: use order if still not assigned
        if not data_file and not comments_file and len(data_files) >= 2:
            data_file = data_files[0]
            comments_file = data_files[1]
        elif not data_file and comments_file:
            for df_path in data_files:
                if df_path != comments_file:
                    data_file = df_path
                    break
        elif data_file and not comments_file:
            for df_path in data_files:
                if df_path != data_file:
                    comments_file = df_path
                    break
        
        if not video_file or not data_file or not comments_file:
            error_details = {
                'video': bool(video_file),
                'data': bool(data_file),
                'comments': bool(comments_file),
                'detected_types': file_types
            }
            error_msg = f'ファイルの自動判別に失敗しました。配信データ: {bool(data_file)}, コメントデータ: {bool(comments_file)}'
            return jsonify({'error': error_msg, 'details': error_details}), 400
        
        # Initialize analyzers
        video_analyzer = VideoAnalyzer(video_file, session_folder)
        data_analyzer = DataAnalyzer(data_file)
        comment_analyzer = CommentAnalyzer(comments_file)
        report_generator = ReportGenerator(session_folder)
        
        # Step 1: Preprocess and analyze data
        data_df = data_analyzer.load_and_clean_data()
        comments_df = comment_analyzer.load_and_clean_data()
        
        # Step 2: Analyze video (extract key frames and events)
        video_events = video_analyzer.analyze_video_structure()
        
        # Step 3: Correlate metrics with video events
        correlations = data_analyzer.correlate_with_events(video_events)
        
        # Step 4: Analyze comments
        comment_analysis = comment_analyzer.classify_comments(comments_df)
        
        # Step 5: Generate report
        report_data = report_generator.generate_report(
            data_df=data_df,
            comments_df=comments_df,
            video_events=video_events,
            correlations=correlations,
            comment_analysis=comment_analysis
        )
        
        return jsonify({
            'success': True,
            'report_data': report_data,
            'session_id': session_id
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'分析エラー: {str(e)}'}), 500

@app.route('/api/report/<session_id>', methods=['GET'])
def get_report(session_id):
    """レポート取得エンドポイント"""
    try:
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        report_path = os.path.join(session_folder, 'report.json')
        
        if not os.path.exists(report_path):
            return jsonify({'error': 'レポートが見つかりません'}), 404
        
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        return jsonify(report_data)
        
    except Exception as e:
        return jsonify({'error': f'レポート取得エラー: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/api/download/<session_id>', methods=['GET'])
def download_report(session_id):
    """PowerPointレポートダウンロードエンドポイント"""
    try:
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        
        if not os.path.exists(session_folder):
            return jsonify({'error': 'セッションが見つかりません'}), 404
        
        # PPTXファイルを探す
        import glob
        pptx_files = glob.glob(os.path.join(session_folder, '*.pptx'))
        
        if not pptx_files:
            return jsonify({'error': 'PowerPointレポートが見つかりません'}), 404
        
        # 最新のファイルを取得
        pptx_file = max(pptx_files, key=os.path.getctime)
        
        return send_file(
            pptx_file,
            as_attachment=True,
            download_name=os.path.basename(pptx_file),
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
    except Exception as e:
        return jsonify({'error': f'ダウンロードエラー: {str(e)}'}), 500
