import pdfplumber

pdf_path = "data/raw/Safaricom Annual-2025-Reporrt.pdf"
page_num = 200  # Page 201

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[page_num]
    
    print(f"Extracting from page {page_num + 1}")
    print("="*70)
    
    # Get all tables
    tables = page.extract_tables()
    
    print(f"Number of tables found: {len(tables)}")
    
    for i, table in enumerate(tables):
        print(f"\n--- Table {i+1} ---")
        print(f"Dimensions: {len(table)} rows x {len(table[0]) if table else 0} columns")
        
        # Print first 10 rows
        for j, row in enumerate(table[:10]):
            print(f"Row {j}: {row}")
