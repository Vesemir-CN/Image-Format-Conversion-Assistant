---
name: "data-analysis"
description: "Analyzes data, creates charts, generates reports. Invoke when user wants to analyze data or create visualizations."
---

# Data Analysis Skill

This skill helps analyze data and create visualizations using Python.

## Data Analysis with Pandas

```python
import pandas as pd

df = pd.read_csv('data.csv')
df.describe()  # Statistics
df.head()     # First rows
df.groupby('column').sum()  # Group by
```

## Data Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.savefig('chart.png')

# Seaborn
sns.barplot(x='category', y='value', data=df)
```

## Generate Report

```python
import pandas as pd
from fpdf import FPDF

df = pd.read_csv('data.csv')
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Data Report')
pdf.output('report.pdf')
```

## Required Libraries

```
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
numpy>=1.24.0
fpdf>=1.7.2
```

## Usage

Invoke this skill when user wants to:
- Analyze CSV/Excel data
- Create charts and graphs
- Generate data reports
- Perform statistical analysis
- Create visualizations
