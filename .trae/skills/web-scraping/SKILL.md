---
name: "web-scraping"
description: "Scrapes websites and extracts data. Invoke when user wants to collect data from websites."
---

# Web Scraping Skill

This skill helps scrape websites and extract data using Python.

## Basic Scraping with BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup

response = requests.get('https://example.com')
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements
titles = soup.find_all('h2')
for title in titles:
    print(title.text)
```

## Scraping Tables

```python
import pandas as pd

tables = pd.read_html('https://example.com/table')
df = tables[0]
```

## Selenium for Dynamic Pages

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://example.com')
elements = driver.find_elements(By.CSS_SELECTOR, '.class-name')
driver.quit()
```

## Scrapy Framework

```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://example.com']
    
    def parse(self, response):
        for item in response.css('.item'):
            yield {
                'title': item.css('h2::text').get(),
            }
```

## Required Libraries

```
requests>=2.28.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
selenium>=4.8.0
pandas>=2.0.0
```

## Best Practices

1. Respect robots.txt
2. Add delays between requests
3. Use proper headers (User-Agent)
4. Check website terms of service
5. Cache responses when possible

## Usage

Invoke this skill when user wants to:
- Scrape website data
- Extract information from HTML
- Collect data for analysis
- Parse dynamic websites
- Build datasets from web
