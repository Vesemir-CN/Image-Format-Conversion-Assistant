# -*- coding: utf-8 -*-
"""
File processing module for Image Format Converter

Handles file operations including:
- File validation
- File information extraction
- Directory management
"""

import os
import sys
from typing import List, Dict, Tuple, Optional
from datetime import datetime

from config import (
    SUPPORTED_FORMATS, ALL_EXTENSIONS, MAX_FILE_SIZE_MB,
    THUMBNAIL_SIZE, MIN_DPI, MAX_DPI
)


class FileInfo:
    """Container for file information"""
    
    def __init__(self, file_path: str):
        self.path = file_path
        self.name = os.path.basename(file_path)
        self.ext = os.path.splitext(file_path)[1].lower()
        self._size = None
    
    @property
    def size(self) -> int:
        """Get file size in bytes"""
        if self._size is None:
            try:
                self._size = os.path.getsize(self.path)
            except OSError:
                self._size = 0
        return self._size
    
    @property
    def size_str(self) -> str:
        """Get human readable file size"""
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    @property
    def format_type(self) -> str:
        """Get the format type (pdf, jpg, png, tiff, svg)"""
        if self.ext in ['.pdf']:
            return 'pdf'
        elif self.ext in ['.jpg', '.jpeg']:
            return 'jpg'
        elif self.ext in ['.png']:
            return 'png'
        elif self.ext in ['.tif', '.tiff']:
            return 'tiff'
        elif self.ext in ['.svg']:
            return 'svg'
        return 'unknown'
    
    @property
    def format_name(self) -> str:
        """Get the format display name"""
        fmt = self.format_type
        if fmt in SUPPORTED_FORMATS:
            return SUPPORTED_FORMATS[fmt][0]
        return "未知格式"


class FileProcessor:
    """Handles file operations and validation"""
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """
        Validate if a file is valid for conversion
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, f"文件不存在: {os.path.basename(file_path)}"
        
        if not os.path.isfile(file_path):
            return False, f"路径不是文件: {os.path.basename(file_path)}"
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ALL_EXTENSIONS:
            return False, f"不支持的文件格式: {ext}"
        
        file_size = os.path.getsize(file_path)
        max_size = MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size:
            return False, f"文件过大: {os.path.basename(file_path)} (最大 {MAX_FILE_SIZE_MB}MB)"
        
        return True, ""
    
    @staticmethod
    def validate_directory(dir_path: str) -> Tuple[bool, str]:
        """
        Validate if a directory is valid for output
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not dir_path:
            return False, "输出目录不能为空"
        
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except OSError as e:
                return False, f"无法创建目录: {str(e)}"
        
        if not os.path.isdir(dir_path):
            return False, f"路径不是目录: {dir_path}"
        
        if not os.access(dir_path, os.W_OK):
            return False, f"目录没有写入权限: {dir_path}"
        
        return True, ""
    
    @staticmethod
    def get_unique_filename(dir_path: str, base_name: str, ext: str) -> str:
        """Generate a unique filename to avoid conflicts"""
        filename = f"{base_name}{ext}"
        filepath = os.path.join(dir_path, filename)
        
        if not os.path.exists(filepath):
            return filepath
        
        counter = 1
        while True:
            filename = f"{base_name}_{counter}{ext}"
            filepath = os.path.join(dir_path, filename)
            if not os.path.exists(filepath):
                return filepath
            counter += 1
    
    @staticmethod
    def validate_dpi(dpi: int) -> Tuple[int, bool]:
        """
        Validate and correct DPI value
        
        Returns:
            Tuple of (corrected_dpi, was_modified)
        """
        if dpi < MIN_DPI:
            return MIN_DPI, True
        elif dpi > MAX_DPI:
            return MAX_DPI, True
        return dpi, False
    
    @staticmethod
    def get_file_list_info(files: List[FileInfo]) -> Dict:
        """Get aggregated information about a list of files"""
        if not files:
            return {
                'count': 0,
                'total_size': 0,
                'formats': set()
            }
        
        formats = set()
        total_size = 0
        
        for f in files:
            formats.add(f.format_type)
            total_size += f.size
        
        return {
            'count': len(files),
            'total_size': total_size,
            'formats': formats
        }
    
    @staticmethod
    def can_convert(source_format: str, target_format: str) -> bool:
        """Check if conversion from source to target is supported"""
        if source_format == target_format:
            return False
        return source_format in ['pdf', 'jpg', 'tiff'] and target_format in ['pdf', 'jpg', 'tiff']
    
    @staticmethod
    def get_supported_target_formats(source_format: str) -> List[str]:
        """Get list of supported target formats for a given source format"""
        all_formats = ['pdf', 'jpg', 'tiff']
        return [f for f in all_formats if f != source_format]
    
    @staticmethod
    def sort_files_by_ext(files: List[FileInfo]) -> List[FileInfo]:
        """Sort files by extension for consistent ordering"""
        ext_priority = {'.pdf': 0, '.jpg': 1, '.jpeg': 1, '.tif': 2, '.tiff': 2}
        return sorted(files, key=lambda f: ext_priority.get(f.ext, 99))
