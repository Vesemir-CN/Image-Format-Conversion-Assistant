# -*- coding: utf-8 -*-
"""
GUI Module for Image Format Converter

Provides the main application window and all UI components
"""

import os
import sys
from typing import List, Optional

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt5.QtGui import QIcon, QDrag, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QComboBox,
    QSlider, QLineEdit, QProgressBar, QFileDialog, QMessageBox,
    QApplication, QFrame
)

from config import (
    APP_NAME, APP_VERSION, STYLESHEET,
    MIN_DPI, MAX_DPI, DEFAULT_DPI, DPI_STEP,
    SUPPORTED_FORMATS, DEFAULT_OUTPUT_DIR
)
from file_processor import FileInfo, FileProcessor
from converter import ConversionWorker


class DropListWidget(QListWidget):
    """Custom list widget that supports drag and drop"""
    
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlternatingRowColors(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    files.append(path)
                elif os.path.isdir(path):
                    for root, _, filenames in os.walk(path):
                        for f in filenames:
                            files.append(os.path.join(root, f))
            if files:
                self.files_dropped.emit(files)
            event.acceptProposedAction()


class ConversionThread(QThread):
    """Thread for running conversion in background"""
    
    progress_updated = pyqtSignal(str, int)
    conversion_completed = pyqtSignal(list, list, str)
    conversion_failed = pyqtSignal(str)
    
    def __init__(self, files: List[FileInfo], target_format: str, output_dir: str, dpi: int):
        super().__init__()
        self.files = files
        self.target_format = target_format
        self.output_dir = output_dir
        self.dpi = dpi
    
    def run(self):
        try:
            from converter import ConversionEngine
            
            engine = ConversionEngine()
            import threading
            cancel_event = threading.Event()
            
            def progress_callback(message: str, progress: int):
                self.progress_updated.emit(message, progress)
            
            success_files, failed_files = engine.convert(
                self.files,
                self.target_format,
                self.output_dir,
                self.dpi,
                progress_callback,
                cancel_event
            )
            
            self.conversion_completed.emit(success_files, failed_files, self.output_dir)
            
        except Exception as e:
            self.conversion_failed.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.files: List[FileInfo] = []
        self.output_directory = DEFAULT_OUTPUT_DIR
        self.dpi_value = DEFAULT_DPI
        self.source_format = None
        self.target_format = 'jpg'
        self.conversion_thread: Optional[ConversionThread] = None
        
        self._init_ui()
        self._apply_stylesheet()
        self._connect_signals()
        
        self._update_source_format()
    
    def _init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(900, 700)
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        main_layout.addWidget(self._create_file_selection_group())
        main_layout.addWidget(self._create_format_selection_group())
        main_layout.addWidget(self._create_dpi_settings_group())
        main_layout.addWidget(self._create_output_directory_group())
        main_layout.addWidget(self._create_progress_group())
        main_layout.addWidget(self._create_control_buttons())
        main_layout.addWidget(self._create_status_bar())
        
        main_layout.addStretch()
    
    def _create_file_selection_group(self) -> QGroupBox:
        """Create file selection group"""
        group = QGroupBox("文件选择")
        
        layout = QVBoxLayout()
        
        self.file_list_widget = DropListWidget()
        self.file_list_widget.files_dropped.connect(self._on_files_dropped)
        
        button_layout = QHBoxLayout()
        
        self.btn_browse = QPushButton("浏览文件")
        self.btn_browse.clicked.connect(self._browse_files)
        
        self.btn_remove = QPushButton("移除选中")
        self.btn_remove.clicked.connect(self._remove_selected_files)
        
        self.btn_clear = QPushButton("清空列表")
        self.btn_clear.clicked.connect(self._clear_file_list)
        
        button_layout.addWidget(self.btn_browse)
        button_layout.addWidget(self.btn_remove)
        button_layout.addWidget(self.btn_clear)
        button_layout.addStretch()
        
        layout.addWidget(self.file_list_widget)
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_format_selection_group(self) -> QGroupBox:
        """Create format selection group"""
        group = QGroupBox("格式选择")
        
        layout = QHBoxLayout()
        
        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("源格式:"))
        self.source_format_combo = QComboBox()
        self.source_format_combo.addItem("自动检测", "auto")
        for fmt, (name, _) in SUPPORTED_FORMATS.items():
            self.source_format_combo.addItem(name, fmt)
        self.source_format_combo.currentIndexChanged.connect(self._on_source_format_changed)
        source_layout.addWidget(self.source_format_combo)
        
        layout.addLayout(source_layout)
        
        layout.addSpacing(20)
        
        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("目标格式:"))
        self.target_format_combo = QComboBox()
        self._populate_target_formats()
        self.target_format_combo.currentIndexChanged.connect(self._on_target_format_changed)
        target_layout.addWidget(self.target_format_combo)
        
        layout.addLayout(target_layout)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def _create_dpi_settings_group(self) -> QGroupBox:
        """Create DPI settings group"""
        group = QGroupBox("DPI 设置 (仅JPG输出)")
        group.setCheckable(True)
        group.setChecked(True)
        
        layout = QVBoxLayout()
        
        slider_layout = QHBoxLayout()
        
        slider_layout.addWidget(QLabel("滑块:"))
        
        self.dpi_slider = QSlider(Qt.Horizontal)
        self.dpi_slider.setMinimum(MIN_DPI)
        self.dpi_slider.setMaximum(MAX_DPI)
        self.dpi_slider.setValue(DEFAULT_DPI)
        self.dpi_slider.setTickPosition(QSlider.TicksBelow)
        self.dpi_slider.setTickInterval(DPI_STEP * 10)
        self.dpi_slider.valueChanged.connect(self._on_dpi_slider_changed)
        
        slider_layout.addWidget(self.dpi_slider)
        
        self.dpi_value_label = QLabel(f"{DEFAULT_DPI}")
        self.dpi_value_label.setMinimumWidth(40)
        slider_layout.addWidget(self.dpi_value_label)
        
        layout.addLayout(slider_layout)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("或直接输入:"))
        
        self.dpi_input = QLineEdit()
        self.dpi_input.setText(str(DEFAULT_DPI))
        self.dpi_input.setMaximumWidth(100)
        self.dpi_input.textChanged.connect(self._on_dpi_input_changed)
        
        input_layout.addWidget(self.dpi_input)
        input_layout.addWidget(QLabel(f"(范围: {MIN_DPI}-{MAX_DPI})"))
        input_layout.addStretch()
        
        layout.addLayout(input_layout)
        
        group.setLayout(layout)
        self.dpi_group = group
        return group
    
    def _create_output_directory_group(self) -> QGroupBox:
        """Create output directory group"""
        group = QGroupBox("输出目录")
        
        layout = QHBoxLayout()
        
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(DEFAULT_OUTPUT_DIR)
        self.output_dir_input.textChanged.connect(self._on_output_dir_changed)
        
        self.btn_browse_output = QPushButton("浏览")
        self.btn_browse_output.clicked.connect(self._browse_output_directory)
        
        layout.addWidget(self.output_dir_input)
        layout.addWidget(self.btn_browse_output)
        
        group.setLayout(layout)
        return group
    
    def _create_progress_group(self) -> QGroupBox:
        """Create progress display group"""
        group = QGroupBox("转换进度")
        
        layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        
        self.progress_label = QLabel("等待开始转换...")
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        
        group.setLayout(layout)
        return group
    
    def _create_control_buttons(self) -> QWidget:
        """Create control buttons"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn_start = QPushButton("开始转换")
        self.btn_start.setMinimumHeight(45)
        self.btn_start.clicked.connect(self._start_conversion)
        
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setMinimumHeight(45)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel_conversion)
        
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_cancel)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _create_status_bar(self) -> QWidget:
        """Create status bar"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel("就绪")
        self.status_label.setObjectName("status_label")
        
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _apply_stylesheet(self):
        """Apply the application stylesheet"""
        self.setStyleSheet(STYLESHEET)
    
    def _connect_signals(self):
        """Connect UI signals to handlers"""
        pass
    
    def _populate_target_formats(self):
        """Populate target format combo box based on source format"""
        self.target_format_combo.clear()
        
        source_fmt = self.source_format_combo.currentData()
        
        if source_fmt == 'auto':
            for fmt, (name, _) in SUPPORTED_FORMATS.items():
                self.target_format_combo.addItem(name, fmt)
        else:
            for fmt, (name, _) in SUPPORTED_FORMATS.items():
                if fmt != source_fmt:
                    self.target_format_combo.addItem(name, fmt)
        
        if self.target_format_combo.count() > 0:
            self.target_format_combo.setCurrentIndex(0)
            self.target_format = self.target_format_combo.currentData()
    
    def _on_files_dropped(self, file_paths: List[str]):
        """Handle dropped files"""
        self._add_files(file_paths)
    
    def _browse_files(self):
        """Open file browser dialog"""
        filters = []
        filter_texts = []
        
        for fmt, (name, exts) in SUPPORTED_FORMATS.items():
            filters.append(f"{name} (*{' *'.join(exts)})")
            filter_texts.extend(exts)
        
        filters.append("所有支持的文件 (*" + " *".join(filter_texts) + ")")
        filter_text = ";;".join(filters)
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择要转换的文件",
            "",
            filter_text
        )
        
        if files:
            self._add_files(files)
    
    def _add_files(self, file_paths: List[str]):
        """Add files to the list"""
        for path in file_paths:
            is_valid, error_msg = FileProcessor.validate_file(path)
            
            if not is_valid:
                QMessageBox.warning(self, "文件无效", error_msg)
                continue
            
            if any(f.path == path for f in self.files):
                continue
            
            file_info = FileInfo(path)
            self.files.append(file_info)
            
            item = QListWidgetItem(f"{file_info.name} ({file_info.format_name}, {file_info.size_str})")
            item.setData(Qt.UserRole, file_info)
            self.file_list_widget.addItem(item)
        
        self._update_source_format()
        self._update_ui_state()
    
    def _remove_selected_files(self):
        """Remove selected files from list"""
        current_item = self.file_list_widget.currentItem()
        if current_item:
            row = self.file_list_widget.row(current_item)
            self.file_list_widget.takeItem(row)
            self.files.pop(row)
            self._update_source_format()
            self._update_ui_state()
    
    def _clear_file_list(self):
        """Clear all files from list"""
        self.file_list_widget.clear()
        self.files.clear()
        self._update_source_format()
        self._update_ui_state()
    
    def _update_source_format(self):
        """Update source format based on selected files"""
        if not self.files:
            self.source_format_combo.setCurrentIndex(0)
            self.source_format = None
        else:
            formats = set(f.format_type for f in self.files)
            if len(formats) == 1:
                fmt = list(formats)[0]
                for i in range(self.source_format_combo.count()):
                    if self.source_format_combo.itemData(i) == fmt:
                        self.source_format_combo.setCurrentIndex(i)
                        self.source_format = fmt
                        break
            else:
                self.source_format_combo.setCurrentIndex(0)
                self.source_format = None
        
        self._populate_target_formats()
    
    def _on_source_format_changed(self, index: int):
        """Handle source format change"""
        self.source_format = self.source_format_combo.currentData()
        if self.source_format == 'auto':
            self.source_format = None
        self._populate_target_formats()
    
    def _on_target_format_changed(self, index: int):
        """Handle target format change"""
        self.target_format = self.target_format_combo.currentData()
        self._update_dpi_visibility()
    
    def _update_dpi_visibility(self):
        """Show/hide DPI settings based on target format"""
        if self.target_format == 'jpg':
            self.dpi_group.setVisible(True)
        else:
            self.dpi_group.setVisible(False)
    
    def _on_dpi_slider_changed(self, value: int):
        """Handle DPI slider change"""
        corrected, modified = FileProcessor.validate_dpi(value)
        
        if modified:
            self.dpi_slider.setValue(corrected)
            self._show_dpi_warning(corrected)
        
        self.dpi_value = corrected
        self.dpi_value_label.setText(str(corrected))
        self.dpi_input.setText(str(corrected))
    
    def _on_dpi_input_changed(self, text: str):
        """Handle DPI input change"""
        try:
            value = int(text)
            corrected, modified = FileProcessor.validate_dpi(value)
            
            if modified:
                self.dpi_input.setText(str(corrected))
                self.dpi_slider.setValue(corrected)
                self._show_dpi_warning(corrected)
            
            self.dpi_value = corrected
            self.dpi_value_label.setText(str(corrected))
            
        except ValueError:
            pass
    
    def _show_dpi_warning(self, corrected_value: int):
        """Show DPI correction warning"""
        if corrected_value < MIN_DPI:
            QMessageBox.warning(
                self,
                "DPI已调整",
                f"DPI值已自动调整为最小值 {MIN_DPI}"
            )
        elif corrected_value > MAX_DPI:
            QMessageBox.warning(
                self,
                "DPI已调整",
                f"DPI值已自动调整为最大值 {MAX_DPI}"
            )
    
    def _browse_output_directory(self):
        """Open directory browser dialog"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录",
            self.output_directory
        )
        
        if dir_path:
            self.output_directory = dir_path
            self.output_dir_input.setText(dir_path)
    
    def _on_output_dir_changed(self, text: str):
        """Handle output directory change"""
        self.output_directory = text
    
    def _update_ui_state(self):
        """Update UI state based on current settings"""
        has_files = len(self.files) > 0
        self.btn_start.setEnabled(has_files)
        
        if has_files:
            self.status_label.setText(f"已选择 {len(self.files)} 个文件")
        else:
            self.status_label.setText("请添加要转换的文件")
    
    def _validate_inputs(self) -> bool:
        """Validate all inputs before conversion"""
        if not self.files:
            QMessageBox.warning(self, "错误", "请至少选择一个文件")
            return False
        
        is_valid, error_msg = FileProcessor.validate_directory(self.output_directory)
        if not is_valid:
            QMessageBox.warning(self, "错误", f"输出目录无效: {error_msg}")
            return False
        
        if self.target_format == 'jpg':
            self.dpi_value, _ = FileProcessor.validate_dpi(self.dpi_value)
        
        return True
    
    def _start_conversion(self):
        """Start the conversion process"""
        if not self._validate_inputs():
            return
        
        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.btn_browse.setEnabled(False)
        self.btn_clear.setEnabled(False)
        
        self.progress_bar.setValue(0)
        self.progress_label.setText("正在初始化转换...")
        
        self.conversion_thread = ConversionThread(
            self.files,
            self.target_format,
            self.output_directory,
            self.dpi_value
        )
        
        self.conversion_thread.progress_updated.connect(self._on_progress_updated)
        self.conversion_thread.conversion_completed.connect(self._on_conversion_completed)
        self.conversion_thread.conversion_failed.connect(self._on_conversion_failed)
        
        self.conversion_thread.start()
    
    def _cancel_conversion(self):
        """Cancel the conversion process"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.terminate()
        
        self._reset_ui_state()
        self.progress_label.setText("转换已取消")
        QMessageBox.information(self, "取消", "转换已取消")
    
    def _on_progress_updated(self, message: str, progress: int):
        """Handle progress update"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(message)
    
    def _on_conversion_completed(self, success_files: List[str], failed_files: List[str], output_dir: str):
        """Handle conversion completion"""
        self._reset_ui_state()
        
        success_count = len(success_files)
        failed_count = len(failed_files)
        
        if failed_count > 0:
            msg = f"转换完成！成功: {success_count} 个文件，失败: {failed_count} 个文件"
            QMessageBox.warning(self, "转换完成", msg)
        else:
            msg = f"转换成功完成！共 {success_count} 个文件"
            reply = QMessageBox.question(
                self,
                "转换成功",
                msg,
                QMessageBox.Ok | QMessageBox.Open,
                QMessageBox.Ok
            )
            
            if reply == QMessageBox.Open:
                os.startfile(output_dir)
        
        self.progress_bar.setValue(100)
        self.progress_label.setText("转换完成")
    
    def _on_conversion_failed(self, error: str):
        """Handle conversion failure"""
        self._reset_ui_state()
        
        QMessageBox.critical(
            self,
            "转换失败",
            f"转换过程中发生错误:\n{error}"
        )
        
        self.progress_label.setText("转换失败")
    
    def _reset_ui_state(self):
        """Reset UI to normal state"""
        self.btn_start.setEnabled(len(self.files) > 0)
        self.btn_cancel.setEnabled(False)
        self.btn_browse.setEnabled(True)
        self.btn_clear.setEnabled(True)


def main():
    """Main entry point for GUI application"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
