import pdfplumber
import os

# Get the PDF files
raw_data_dir = "data/raw"
pdf_files = sorted([f for f in os.listdir(raw_data_dir) if f.endswith('.pdf')])

print(f"Found {len(pdf_files)} PDF files:")
for i, pdf_file in enumerate(pdf_files, 1):
    print(f"  {i}. {pdf_file}")

# Explore each PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(raw_data_dir, pdf_file)
    print(f"\n{'='*70}")
    print(f"Exploring: {pdf_file}")
    print('='*70)
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        
        found_statements = []
        
        # Search through ALL pages
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if text:
                text_lower = text.lower()
                
                # Look for specific financial statement keywords
                if 'consolidated statement of comprehensive income' in text_lower:
                    found_statements.append((page_num + 1, 'Income Statement'))
                elif 'consolidated statement of financial position' in text_lower:
                    found_statements.append((page_num + 1, 'Balance Sheet'))
                elif 'consolidated statement of cash flows' in text_lower:
                    found_statements.append((page_num + 1, 'Cash Flow Statement'))
        
        # Print findings
        if found_statements:
            print("Financial Statements Found:")
            for page_num, statement_type in found_statements:
                print(f"  - PAGE {page_num}: {statement_type}")
        else:
            print("No clear financial statements found. Searching for 'notes' section...")
            # Sometimes statements are in the notes section
            for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text and 'notes to the financial statements' in text.lower():
                    print(f"  - PAGE {page_num + 1}: Notes to Financial Statements")
                    break
        
        print()
