import pdfplumber
import pandas as pd
import os

# Define the page numbers for each statement in each PDF (0-indexed)
pdf_configs = {
    "2023-Safaricom-Annual-Report.pdf": {
        "year": "2023",
        "income_statement": 187,  # Page 188
        "balance_sheet": 188,      # Page 189
        "cash_flow": 193           # Page 194
    },
    "Safaricom 2024-Annual-Report-Update.pdf": {
        "year": "2024",
        "income_statement": 180,  # Page 181
        "balance_sheet": 192,      # Page 193
        "cash_flow": 205           # Page 206
    },
    "Safaricom Annual-2025-Reporrt.pdf": {
        "year": "2025",
        "income_statement": 200,  # Page 201 (CORRECTED)
        "balance_sheet": 210,      # Page 211
        "cash_flow": 224           # Page 225
    }
}

raw_data_dir = "data/raw"
extracted_dir = "data/extracted"

# Create extracted directory if it doesn't exist
os.makedirs(extracted_dir, exist_ok=True)

print("\n" + "="*70)
print("EXTRACTING FINANCIAL STATEMENTS FROM SAFARICOM ANNUAL REPORTS")
print("="*70)

# Extract data from each PDF
for pdf_file, config in pdf_configs.items():
    pdf_path = os.path.join(raw_data_dir, pdf_file)
    year = config["year"]
    
    print(f"\n{'='*70}")
    print(f"Processing: {pdf_file} (FY {year})")
    print('='*70)
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extract Income Statement
        page = pdf.pages[config["income_statement"]]
        tables = page.extract_tables()
        
        if tables:
            print(f"✓ Income Statement extracted from page {config['income_statement'] + 1}")
            df = pd.DataFrame(tables[0])
            output_file = os.path.join(extracted_dir, f"income_statement_{year}.csv")
            df.to_csv(output_file, index=False, header=False)
            print(f"  → Saved to: {output_file}")
        else:
            print(f"✗ No tables found on income statement page")
        
        # Extract Balance Sheet
        page = pdf.pages[config["balance_sheet"]]
        tables = page.extract_tables()
        
        if tables:
            print(f"✓ Balance Sheet extracted from page {config['balance_sheet'] + 1}")
            df = pd.DataFrame(tables[0])
            output_file = os.path.join(extracted_dir, f"balance_sheet_{year}.csv")
            df.to_csv(output_file, index=False, header=False)
            print(f"  → Saved to: {output_file}")
        else:
            print(f"✗ No tables found on balance sheet page")
            
        # Extract Cash Flow Statement
        page = pdf.pages[config["cash_flow"]]
        tables = page.extract_tables()
        
        if tables:
            print(f"✓ Cash Flow Statement extracted from page {config['cash_flow'] + 1}")
            df = pd.DataFrame(tables[0])
            output_file = os.path.join(extracted_dir, f"cash_flow_{year}.csv")
            df.to_csv(output_file, index=False, header=False)
            print(f"  → Saved to: {output_file}")
        else:
            print(f"✗ No tables found on cash flow page")

print("\n" + "="*70)
print("EXTRACTION COMPLETE!")
print("="*70)
print(f"\nExtracted files saved in: {extracted_dir}/")
print("\nNext steps:")
print("  1. Review the extracted CSV files")
print("  2. Clean and transform the data")
print("  3. Load into database")
print("="*70 + "\n")
