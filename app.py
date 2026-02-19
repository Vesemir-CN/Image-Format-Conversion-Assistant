#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scientific Image Processing Assistant - Backend API

A Flask-based backend for image format conversion
"""

import os
import tempfile
import threading
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file

from converter import ConversionEngine
from file_processor import FileInfo, FileProcessor
from config import MAX_FILE_SIZE_MB

# 尝试导入Flask-Cors，如果失败则不使用
try:
    from flask_cors import CORS
except ImportError:
    CORS = None

app = Flask(__name__)
# 仅在CORS可用时启用
if CORS:
    CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['OUTPUT_FOLDER'] = tempfile.gettempdir()

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Active conversions
active_conversions = {}


class ConversionTask:
    """Represents an ongoing conversion task"""
    
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
        self.start_time = datetime.now()


@app.route('/')
def index():
    """Serve the main HTML file"""
    try:
        # Try to read the index.html file directly
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return f'Error loading index.html: {str(e)}', 500


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Upload files for conversion"""
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
            
            # Save to temporary location
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_path)
            
            # Validate file
            is_valid, error_msg = FileProcessor.validate_file(temp_path)
            if not is_valid:
                os.remove(temp_path)
                return jsonify({'error': f'File validation failed: {error_msg}'}), 400
            
            # Create FileInfo
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
    """Start a conversion task"""
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
        
        # Create task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Get actual file paths
        file_infos = []
        for file_data in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_data['name'])
            if os.path.exists(file_path):
                file_infos.append(FileInfo(file_path))
        
        if not file_infos:
            return jsonify({'error': 'No valid files found'}), 400
        
        # Create task
        task = ConversionTask(task_id, file_infos, target_format, dpi)
        active_conversions[task_id] = task
        
        # Start conversion in background
        def convert_worker():
            engine = ConversionEngine()
            
            def progress_callback(message, progress):
                task.progress = progress
                task.message = message
                task.status = 'processing'
            
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
    """Get conversion status"""
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
    """Download converted file"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True)


@app.route('/api/cancel/<task_id>', methods=['POST'])
def cancel_conversion(task_id):
    """Cancel an ongoing conversion"""
    if task_id not in active_conversions:
        return jsonify({'error': 'Task not found'}), 404
    
    task = active_conversions[task_id]
    task.status = 'cancelled'
    task.message = 'Conversion cancelled by user'
    
    return jsonify({'success': True})


@app.route('/api/formats', methods=['GET'])
def get_supported_formats():
    """Get supported formats"""
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


if __name__ == '__main__':
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
