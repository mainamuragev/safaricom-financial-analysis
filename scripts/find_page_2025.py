import pdfplumber

pdf_path = "data/raw/Safaricom Annual-2025-Reporrt.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Search pages 195-205 more carefully
    for page_num in range(194, 205):
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        if text and 'revenue from contracts with customers' in text.lower():
            # Also check for the actual financial numbers
            if '384,433' in text or '373,492' in text:  # 2025 revenue numbers we saw earlier
                print(f"\n✓ Found correct Income Statement on PAGE {page_num + 1}")
                print("\nFirst 1000 characters:")
                print(text[:1000])
                
                # Also extract table to verify
                tables = page.extract_tables()
                print(f"\nNumber of tables found: {len(tables)}")
                break
