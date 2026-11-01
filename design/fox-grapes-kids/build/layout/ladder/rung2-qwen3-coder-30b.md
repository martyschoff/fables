```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Ellipse
from reportlab.graphics import renderPDF
import re

# Page dimensions
TRIM_WIDTH = 8.5 * inch
TRIM_HEIGHT = 8.5 * inch
PRINT_WIDTH = 8.75 * inch
PRINT_HEIGHT = 8.75 * inch
BLEED = 0.125 * inch
SAFE_MARGIN = 0.5 * inch

# Cream background color
CREAM = Color(0.95, 0.93, 0.87, 1)

def build_book():
    # Create canvas with print dimensions
    c = canvas.Canvas("book.pdf", pagesize=(PRINT_WIDTH, PRINT_HEIGHT))
    
    # Set bleed marks
    draw_trim_marks(c)
    
    # Set background color
    c.setFillColor(CREAM)
    c.rect(0, 0, PRINT_WIDTH, PRINT_HEIGHT, fill=1)
    
    # Read content
    with open("content/story.md", "r") as f:
        lines = f.readlines()
    
    # Parse content
    pages = []
    current_page = []
    for line in lines:
        if line.startswith('- **p4:**'):
            text = line[8:].strip()
            current_page.append(text)
        elif line.strip() == '':
            if current_page:
                pages.append(current_page)
                current_page = []
    
    if current_page:
        pages.append(current_page)
    
    # Ensure 32 pages
    while len(pages) < 32:
        pages.append([])
    
    # Create pages with text and placeholder art
    for i, page_content in enumerate(pages):
        if i > 0:
            c.showPage()
        
        # Draw background
        c.setFillColor(CREAM)
        c.rect(0, 0, PRINT_WIDTH, PRINT_HEIGHT, fill=1)
        
        # Add trim marks on print size
        draw_trim_marks(c)
        
        # Add placeholder art (overlapping translucent ellipses)
        add_watercolor_art(c)
        
        # Add text content
        if page_content:
            y_position = PRINT_HEIGHT - SAFE_MARGIN - 20  # Start near top of safe area
            
            for text in page_content:
                # Calculate text dimensions using simpleSplit
                styles = getSampleStyleSheet()
                style = ParagraphStyle(
                    'Custom',
                    parent=styles['Normal'],
                    fontSize=20,
                    alignment=TA_LEFT,
                    spaceAfter=12,
                )
                
                para = Paragraph(text, style)
                width, height = para.wrap(PRINT_WIDTH - 2 * SAFE_MARGIN, PRINT_HEIGHT - 2 * SAFE_MARGIN)
                
                if y_position - height > SAFE_MARGIN:
                    para.drawOn(c, SAFE_MARGIN, y_position - height)
                    y_position -= height + 12
                else:
                    # If we run out of space, move to next page
                    break
    
    # Save the PDF
    c.save()

def draw_trim_marks(c):
    # Trim marks at edges (outside trim area)
    c.setLineWidth(0.5)
    
    # Top trim marks
    c.line(-BLEED, PRINT_HEIGHT - BLEED, 0, PRINT_HEIGHT - BLEED)
    c.line(PRINT_WIDTH, PRINT_HEIGHT - BLEED, PRINT_WIDTH + BLEED, PRINT_HEIGHT - BLEED)
    
    # Bottom trim marks
    c.line(-BLEED, 0, 0, 0)
    c.line(PRINT_WIDTH, 0, PRINT_WIDTH + BLEED, 0)
    
    # Left trim marks
    c.line(0, -BLEED, 0, 0)
    c.line(0, PRINT_HEIGHT, 0, PRINT_HEIGHT + BLEED)
    
    # Right trim marks
    c.line(PRINT_WIDTH, -BLEED, PRINT_WIDTH, 0)
    c.line(PRINT_WIDTH, PRINT_HEIGHT, PRINT_WIDTH, PRINT_HEIGHT + BLEED)

def add_watercolor_art(c):
    # Draw translucent overlapping ellipses for watercolor effect
    c.setFillColor(Color(0.8, 0.6, 0.4, alpha=0.2))
    
    # Create a series of overlapping ellipses
    for i in range(15):
        x = (i * 30) % (PRINT_WIDTH - 100)
        y = (i * 20) % (PRINT_HEIGHT - 100)
        w = 80 + (i * 5)
        h = 60 + (i * 3)
        
        c.ellipse(x, y, x + w, y + h)

if __name__ == "__main__":
    build_book()
```
