# -*- coding: utf-8 -*-
"""
Configuration module for Image Format Converter

Contains all constants, configuration parameters, and application settings
"""

import os

APP_NAME = "图像格式转换工具"
APP_VERSION = "1.0.0"
AUTHOR = "Image Converter Team"

SUPPORTED_FORMATS = {
    'pdf': ['PDF文件', ['.pdf']],
    'jpg': ['JPEG文件', ['.jpg', '.jpeg']],
    'png': ['PNG文件', ['.png']],
    'tiff': ['TIFF文件', ['.tif', '.tiff']],
    'svg': ['SVG文件', ['.svg']]
}

ALL_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.svg']

MIN_DPI = 300
MAX_DPI = 600
DEFAULT_DPI = 300
DPI_STEP = 10

JPEG_QUALITY = 95

TIFF_COMPRESSION = 'tiff_lzw'

CONVERSION_COMBINATIONS = {
    ('pdf', 'jpg'): 'PDF转JPG',
    ('pdf', 'png'): 'PDF转PNG',
    ('pdf', 'tiff'): 'PDF转TIFF',
    ('jpg', 'pdf'): 'JPG转PDF',
    ('jpg', 'png'): 'JPG转PNG',
    ('jpg', 'tiff'): 'JPG转TIFF',
    ('jpg', 'svg'): 'JPG转SVG',
    ('png', 'pdf'): 'PNG转PDF',
    ('png', 'jpg'): 'PNG转JPG',
    ('png', 'tiff'): 'PNG转TIFF',
    ('png', 'svg'): 'PNG转SVG',
    ('tiff', 'pdf'): 'TIFF转PDF',
    ('tiff', 'jpg'): 'TIFF转JPG',
    ('tiff', 'png'): 'TIFF转PNG',
    ('tiff', 'svg'): 'TIFF转SVG',
    ('svg', 'pdf'): 'SVG转PDF',
    ('svg', 'jpg'): 'SVG转JPG',
    ('svg', 'png'): 'SVG转PNG',
    ('svg', 'tiff'): 'SVG转TIFF'
}

DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop")

MAX_FILE_SIZE_MB = 500

THUMBNAIL_SIZE = (48, 48)

STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
}

QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

QPushButton#btn_cancel {
    background-color: #d83b01;
}

QPushButton#btn_cancel:hover {
    background-color: #b33000;
}

QPushButton#btn_clear {
    background-color: #666666;
}

QPushButton#btn_clear:hover {
    background-color: #444444;
}

QListWidget {
    border: 1px solid #cccccc;
    background-color: white;
    border-radius: 4px;
}

QListWidget::item {
    padding: 5px;
}

QListWidget::item:selected {
    background-color: #0078d4;
    color: white;
}

QComboBox {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
    background-color: white;
}

QComboBox:hover {
    border: 1px solid #0078d4;
}

QComboBox::drop-down {
    border: none;
}

QSlider::groove:horizontal {
    border: 1px solid #cccccc;
    height: 8px;
    background-color: white;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background-color: #0078d4;
    border: 1px solid #005a9e;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background-color: #106ebe;
}

QLineEdit {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
    background-color: white;
}

QLineEdit:focus {
    border: 1px solid #0078d4;
}

QProgressBar {
    border: 1px solid #cccccc;
    border-radius: 4px;
    text-align: center;
    background-color: white;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

QLabel {
    color: #333333;
}

QLabel#status_label {
    color: #666666;
    font-size: 12px;
}
"""
