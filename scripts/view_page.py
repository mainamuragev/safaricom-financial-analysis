import pdfplumber

# Check pages 186-188 for Income Statement
pdf_path = "data/raw/2023-Safaricom-Annual-Report.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(185, 189):  # pages 186-189
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        print(f"\n{'='*70}")
        print(f"PAGE {page_num + 1}")
        print('='*70)
        print(text)  # Print full page to see everything
        print("\n")
