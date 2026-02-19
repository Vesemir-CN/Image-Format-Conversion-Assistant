# Vercel Python Flask Entry Point
import os
import sys

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Try to import Flask, install if missing
try:
    from flask import Flask, request, jsonify, send_file
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask', '-q'])
    from flask import Flask, request, jsonify, send_file

# Try to import Flask-Cors
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False

# Import app components
from converter import ConversionEngine
from file_processor import FileInfo, FileProcessor

# Get MAX_FILE_SIZE_MB from config
try:
    from config import MAX_FILE_SIZE_MB
except:
    MAX_FILE_SIZE_MB = 50

# Create Flask app
app = Flask(__name__)

# Enable CORS if available
if CORS_AVAILABLE:
    CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/outputs'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Active conversions
active_conversions = {}


class ConversionTask:
    def __init__(self, task_id, files, target_format, dpi=300):
        self.task_id = task_id
        self.files = files
        self.target_format = target_format
        self.dpi = dpi
        self.status = 'pending'
        self.progress = 0
        self.message = 'Initializing...'
        self.output_files = []
        self.error = ''
        from datetime import datetime
        self.start_time = datetime.now()


@app.route('/')
def index():
    try:
        html_path = os.path.join(project_root, 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return f'Error: {str(e)}', 500


@app.route('/api/upload', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                continue
            
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_path)
            
            is_valid, error_msg = FileProcessor.validate_file(temp_path)
            if not is_valid:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return jsonify({'error': f'File validation failed: {error_msg}'}), 400
            
            file_info = FileInfo(temp_path)
            uploaded_files.append({
                'id': len(uploaded_files),
                'name': file_info.name,
                'size': file_info.size_str,
                'format': file_info.format_type
            })
        
        return jsonify({
            'success': True,
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/convert', methods=['POST'])
def start_conversion():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        files = data.get('files', [])
        target_format = data.get('target_format')
        dpi = data.get('dpi', 300)
        
        if not files:
            return jsonify({'error': 'No files provided'}), 400
        
        if not target_format:
            return jsonify({'error': 'No target format provided'}), 400
        
        from datetime import datetime
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        file_infos = []
        for file_data in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_data['name'])
            if os.path.exists(file_path):
                file_infos.append(FileInfo(file_path))
        
        if not file_infos:
            return jsonify({'error': 'No valid files found'}), 400
        
        task = ConversionTask(task_id, file_infos, target_format, dpi)
        active_conversions[task_id] = task
        
        def convert_worker():
            engine = ConversionEngine()
            
            def progress_callback(message, progress):
                task.progress = progress
                task.message = message
                task.status = 'processing'
            
            import threading
            cancel_event = threading.Event()
            
            try:
                success_files, failed_files = engine.convert(
                    file_infos,
                    target_format,
                    app.config['OUTPUT_FOLDER'],
                    dpi,
                    progress_callback,
                    cancel_event
                )
                
                task.output_files = success_files
                task.status = 'completed'
                task.message = f'Conversion completed: {len(success_files)} files'
                
            except Exception as e:
                task.error = str(e)
                task.status = 'failed'
                task.message = f'Error: {str(e)}'
        
        import threading
        thread = threading.Thread(target=convert_worker)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status/<task_id>', methods=['GET'])
def get_status(task_id):
    if task_id not in active_conversions:
        return jsonify({'error': 'Task not found'}), 404
    
    task = active_conversions[task_id]
    
    return jsonify({
        'success': True,
        'task': {
            'id': task.task_id,
            'status': task.status,
            'progress': task.progress,
            'message': task.message,
            'output_files': [os.path.basename(f) for f in task.output_files],
            'error': task.error
        }
    })


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True)


@app.route('/api/cancel/<task_id>', methods=['POST'])
def cancel_conversion(task_id):
    if task_id not in active_conversions:
        return jsonify({'error': 'Task not found'}), 404
    
    task = active_conversions[task_id]
    task.status = 'cancelled'
    task.message = 'Conversion cancelled by user'
    
    return jsonify({'success': True})


@app.route('/api/formats', methods=['GET'])
def get_supported_formats():
    try:
        from config import SUPPORTED_FORMATS, CONVERSION_COMBINATIONS
        
        formats = []
        for fmt, (name, exts) in SUPPORTED_FORMATS.items():
            formats.append({
                'id': fmt,
                'name': name,
                'extensions': exts
            })
        
        conversions = []
        for (src, dst), name in CONVERSION_COMBINATIONS.items():
            conversions.append({
                'source': src,
                'target': dst,
                'name': name
            })
        
        return jsonify({
            'success': True,
            'formats': formats,
            'conversions': conversions
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'formats': [
                {'id': 'pdf', 'name': 'PDF', 'extensions': ['.pdf']},
                {'id': 'jpg', 'name': 'JPEG', 'extensions': ['.jpg', '.jpeg']},
                {'id': 'png', 'name': 'PNG', 'extensions': ['.png']},
                {'id': 'tiff', 'name': 'TIFF', 'extensions': ['.tif', '.tiff']}
            ],
            'conversions': []
        })


# Vercel handler
handler = app
