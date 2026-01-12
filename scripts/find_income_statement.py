import pdfplumber

pdf_path = "data/raw/Safaricom Annual-2025-Reporrt.pdf"

print(f"Searching: {pdf_path.split('/')[-1]}")
print('='*70)

with pdfplumber.open(pdf_path) as pdf:
    # Search pages 190-210
    for page_num in range(189, 211):
        if page_num >= len(pdf.pages):
            break
        
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        if text:
            text_lower = text.lower()
            # Look for revenue which is key indicator of income statement
            if 'revenue from contracts with customers' in text_lower and 'total revenue' in text_lower:
                print(f"\nFound Income Statement on PAGE {page_num + 1}")
                print(text[:1200])
                break
