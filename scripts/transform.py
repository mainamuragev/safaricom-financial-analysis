import pandas as pd
import re
import os

extracted_dir = "data/extracted"
processed_dir = "data/processed"

# Create processed directory
os.makedirs(processed_dir, exist_ok=True)

def clean_value(value):
    """Clean financial values - remove commas, handle parentheses for negatives"""
    if pd.isna(value) or value == '':
        return None
    
    # Convert to string
    value = str(value).strip()
    
    # Remove commas
    value = value.replace(',', '')
    
    # Handle parentheses (negative numbers)
    if '(' in value and ')' in value:
        value = '-' + value.replace('(', '').replace(')', '')
    
    try:
        return float(value)
    except:
        return None

def process_income_statement(year):
    """Process income statement for a given year"""
    file_path = os.path.join(extracted_dir, f"income_statement_{year}.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    # Read the raw CSV
    df = pd.read_csv(file_path, header=None)
    
    print(f"\n{'='*70}")
    print(f"Processing Income Statement {year}")
    print('='*70)
    print(f"Raw shape: {df.shape}")
    print(f"First few rows:\n{df.head(10)}")
    
    # We'll manually structure the key metrics based on what we see
    # This is a starting point - you may need to adjust based on actual data
    
    return df

# Process each year
for year in ['2023', '2024', '2025']:
    df = process_income_statement(year)

print("\n" + "="*70)
print("Review the output above to understand the data structure")
print("="*70)
