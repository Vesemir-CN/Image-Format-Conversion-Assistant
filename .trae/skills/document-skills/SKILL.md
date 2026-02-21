---
name: "document-skills"
description: "Creates and edits documents (PDF, Word, Excel, PowerPoint). Invoke when user wants to create or edit documents."
---

# Document Skills

This skill helps create and edit various document formats including PDF, Word, Excel, and PowerPoint.

## Word Document (.docx)

```python
from docx import Document

doc = Document()
doc.add_heading('Title', 0)
doc.add_paragraph('Content here')
doc.save('document.docx')
```

## Excel Spreadsheet (.xlsx)

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 'Data'
ws.append([1, 2, 3])
wb.save('spreadsheet.xlsx')
```

## PowerPoint (.pptx)

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = "Title"
prs.save('presentation.pptx')
```

## PDF Creation

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("document.pdf", pagesize=letter)
c.drawString(100, 750, "Hello World")
c.save()
```

## PDF Extraction

```python
import PyPDF2

with open('file.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = reader.pages[0].extract_text()
```

## Required Libraries

```
python-docx>=0.8.0
openpyxl>=3.0.0
python-pptx>=0.6.0
reportlab>=4.0.0
PyPDF2>=3.0.0
```

## Usage

Invoke this skill when user wants to:
- Create Word documents
- Generate Excel spreadsheets
- Create PowerPoint presentations
- Create or edit PDF files
- Extract text from PDFs
- Convert between document formats
