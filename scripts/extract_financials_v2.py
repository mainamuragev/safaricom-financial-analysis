import pdfplumber
import pandas as pd
import re
import os

raw_data_dir = "data/raw"
extracted_dir = "data/extracted"
os.makedirs(extracted_dir, exist_ok=True)

def clean_value(val):
    """Clean financial values"""
    if not val or val == '':
        return None
    val = str(val).strip().replace(',', '')
    if '(' in val:
        val = '-' + val.replace('(', '').replace(')', '')
    try:
        return float(val)
    except:
        return None

def extract_income_statement_2025():
    """Special extraction for 2025 since table structure is different"""
    pdf_path = os.path.join(raw_data_dir, "Safaricom Annual-2025-Reporrt.pdf")
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[200]  # Page 201
        text = page.extract_text()
        
        # Parse the text to extract key metrics
        lines = text.split('\n')
        
        data = []
        for i, line in enumerate(lines):
            if 'Revenue from contracts with customers' in line:
                # Find the numbers on following lines
                numbers = []
                for j in range(i, min(i+5, len(lines))):
                    matches = re.findall(r'[\d,]+\.?\d*', lines[j])
                    numbers.extend(matches)
                
                if len(numbers) >= 4:
                    data.append(['Revenue from contracts with customers', '5(a)', 
                                numbers[0], numbers[1], numbers[2], numbers[3]])
            
            elif 'Total revenue' in line and 'from' not in line.lower():
                numbers = []
                for j in range(i, min(i+3, len(lines))):
                    matches = re.findall(r'[\d,]+\.?\d*', lines[j])
                    numbers.extend(matches)
                if len(numbers) >= 4:
                    data.append(['Total revenue', '', numbers[0], numbers[1], numbers[2], numbers[3]])
            
            elif 'EBITDA' in line or 'Earnings before interest' in line:
                numbers = []
                for j in range(i, min(i+3, len(lines))):
                    matches = re.findall(r'[\d,]+\.?\d*', lines[j])
                    numbers.extend(matches)
                if len(numbers) >= 4:
                    data.append(['EBITDA', '', numbers[0], numbers[1], numbers[2], numbers[3]])
            
            elif 'Operating profit' in line and 'EBIT' in line:
                numbers = []
                for j in range(i, min(i+3, len(lines))):
                    matches = re.findall(r'[\(]?[\d,]+\.?\d*[\)]?', lines[j])
                    numbers.extend(matches)
                if len(numbers) >= 4:
                    data.append(['Operating profit (EBIT)', '', numbers[0], numbers[1], numbers[2], numbers[3]])
            
            elif 'Profit for the year' in line and 'attributable' not in line.lower():
                numbers = []
                for j in range(i, min(i+3, len(lines))):
                    matches = re.findall(r'[\(]?[\d,]+\.?\d*[\)]?', lines[j])
                    numbers.extend(matches)
                if len(numbers) >= 4:
                    data.append(['Profit for the year', '', numbers[0], numbers[1], numbers[2], numbers[3]])
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=['Line Item', 'Notes', 'GROUP 2025', 'GROUP 2024', 'COMPANY 2025', 'COMPANY 2024'])
        
        return df

# Main extraction
print("\n" + "="*70)
print("EXTRACTING KEY FINANCIAL METRICS")
print("="*70)

# Extract 2025 with special handling
print("\nExtracting 2025 Income Statement...")
df_2025 = extract_income_statement_2025()
output_file = os.path.join(extracted_dir, "income_statement_2025_cleaned.csv")
df_2025.to_csv(output_file, index=False)
print(f"✓ Saved to: {output_file}")
print(f"\nPreview:")
print(df_2025)

print("\n" + "="*70)
print("For 2023 and 2024, we'll use the existing extractions")
print("="*70)
