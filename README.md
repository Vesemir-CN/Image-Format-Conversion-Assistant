# 图像格式转换工具 (Image Format Converter)

一个功能完善的图像格式转换工具，支持 PDF、JPG、TIFF 三种格式之间的双向转换。

## 功能特点

### 支持的转换格式 (6种组合)
- PDF → JPG：PDF每一页转换为单独的JPG文件
- PDF → TIFF：PDF每一页转换为单独的TIFF文件
- JPG → PDF：多个JPG文件合并为单个PDF
- JPG → TIFF：JPG文件转换为TIFF格式
- TIFF → PDF：多个TIFF文件合并为单个PDF
- TIFF → JPG：TIFF文件转换为JPG格式

### 主要功能
- ✅ 批量转换：支持同时选择多个文件进行转换
- ✅ DPI自定义：JPG输出支持300-600 DPI调节
- ✅ 自定义输出目录：用户可选择输出路径
- ✅ 拖拽支持：支持从文件管理器拖拽文件
- ✅ 实时进度：显示转换进度和状态

## 系统要求

- Python 3.8 或更高版本
- Windows/macOS/Linux (跨平台)
- **Poppler** (PDF处理必需)

## 安装指南

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Poppler (必需)

#### Windows 系统:
1. 下载 Poppler for Windows:
   - 访问 https://github.com/oschwartz10612/poppler-windows/releases/
   - 下载最新版本的 "Release" 包 (如 poppler-24.02.0.zip)
2. 解压文件到合适的位置，例如: `C:\poppler`
3. 将 Poppler 的 bin 目录添加到系统 PATH:
   - 右键点击"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在系统变量中找到 Path，点击编辑
   - 添加 `C:\poppler\Library\bin` (路径根据实际解压位置调整)

4. 验证安装:
   ```bash
   pdftoppm -v
   ```

#### macOS 系统:
```bash
brew install poppler
```

#### Linux 系统 (Ubuntu/Debian):
```bash
sudo apt-get install poppler-utils
```

#### Linux 系统 (CentOS/RHEL):
```bash
sudo yum install poppler-utils
```

## 使用方法

### 启动程序

```bash
python main.py
```

### 操作步骤

1. **添加文件**
   - 点击"浏览文件"按钮选择文件
   - 或直接将文件拖拽到文件列表区域
   - 支持同时选择多种格式的文件

2. **选择格式**
   - 源格式：自动检测或手动选择
   - 目标格式：从下拉菜单选择目标格式

3. **设置DPI** (仅JPG输出)
   - 使用滑块调节 (步长10)
   - 或直接输入数值
   - 范围：300-600

4. **选择输出目录**
   - 点击"浏览"按钮选择目录
   - 或手动输入目录路径

5. **开始转换**
   - 点击"开始转换"按钮
   - 转换过程中可查看进度
   - 可随时点击"取消"中断转换

## 转换输出说明

| 转换类型 | 输出文件命名 | 说明 |
|---------|-------------|------|
| PDF→JPG | 原文件名_页码.jpg | 每页一个文件 |
| PDF→TIFF | 原文件名_页码.tif | 每页一个文件 |
| JPG→PDF | output_时间戳.pdf | 合并所有JPG |
| JPG→TIFF | 原文件名.tif | 一对一转换 |
| TIFF→PDF | output_时间戳.pdf | 合并所有TIFF |
| TIFF→JPG | 原文件名_页码.jpg | 支持多页TIFF |

## 常见问题

### Q: 转换失败提示"pdf2image"相关错误
A: 请确保已正确安装 Poppler 并添加到系统 PATH

### Q: DPI值输入无效怎么办?
A: 程序会自动修正超出范围的DPI值到有效范围(300-600)

### Q: 支持哪些图像格式?
A: 支持 PDF、JPG/JPEG、TIFF/TIF 格式

### Q: 如何处理大文件?
A: 程序使用多线程处理，避免界面冻结；建议批量转换时控制文件数量

## 技术栈

- **GUI框架**: PyQt5
- **图像处理**: Pillow (PIL)
- **PDF转图像**: pdf2image
- **图像转PDF**: img2pdf
- **PDF处理**: poppler

## 项目结构

```
Picture_trans/
├── main.py              # 主入口文件
├── gui.py               # GUI界面模块
├── converter.py         # 转换引擎模块
├── file_processor.py    # 文件处理模块
├── config.py            # 配置和常量
├── requirements.txt     # Python依赖
└── README.md           # 使用说明
```

## 许可证

MIT License
