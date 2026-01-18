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
        
        # Save files
        video_filename = secure_filename(video_file.filename)
        data_filename = secure_filename(data_file.filename)
        comments_filename = secure_filename(comments_file.filename)
        
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
        
        for f in files:
            full_path = os.path.join(session_folder, f)
            # Check if it's a video file
            if any(f.lower().endswith('.' + ext) for ext in app.config['ALLOWED_VIDEO_EXTENSIONS']):
                video_files.append(full_path)
            # Check if it's a data file (CSV/Excel)
            elif any(f.lower().endswith('.' + ext) for ext in app.config['ALLOWED_DATA_EXTENSIONS']):
                data_files.append(full_path)
        
        # Assign video file
        if video_files:
            video_file = video_files[0]
        
        # Assign data and comments files
        # First try to detect by filename
        for df in data_files:
            filename = os.path.basename(df).lower()
            if 'data' in filename or '配信' in filename or 'distribution' in filename:
                data_file = df
            elif 'comment' in filename or 'コメント' in filename or 'chat' in filename:
                comments_file = df
        
        # If still not assigned, use order (first as data, second as comments)
        if len(data_files) >= 2:
            if not data_file:
                data_file = data_files[0]
            if not comments_file:
                # Find the file that's not data_file
                for df in data_files:
                    if df != data_file:
                        comments_file = df
                        break
        elif len(data_files) == 1:
            # Only one data file - could be either data or comments
            # Try to determine by content or just treat as data
            if not data_file and not comments_file:
                return jsonify({'error': '配信データとコメントデータの両方が必要です'}), 400
        
        if not video_file or not data_file or not comments_file:
            error_msg = f'アップロードされたファイルが不完全です (動画: {bool(video_file)}, データ: {bool(data_file)}, コメント: {bool(comments_file)})'
            return jsonify({'error': error_msg}), 400
        
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
