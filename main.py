# -*- coding: utf-8 -*-
#!/usr/bin/env py -3
"""
Image Format Converter - A comprehensive image format conversion tool

Supported conversions:
- PDF <-> JPG
- PDF <-> TIFF
- JPG <-> TIFF
- JPG <-> PDF
- TIFF <-> PDF
- TIFF <-> JPG

Requirements:
- Python 3.8+
- PyQt5
- Pillow (PIL)
- pdf2image
- img2pdf
- poppler (system dependency)
"""

import sys
import os

from PyQt5.QtWidgets import QApplication, QMessageBox

from gui import MainWindow
from config import APP_NAME, APP_VERSION


def main():
    """Main entry point for the application"""
    os.environ.setdefault('QT_QPA_PLATFORM', 'windows')
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
