import pandas as pd
import os

extracted_dir = "data/extracted"
processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

def clean_value(val):
    """Clean financial values"""
    if pd.isna(val) or val == '':
        return None
    val = str(val).strip().replace(',', '').replace('\n', ' ')
    if '(' in val and ')' in val:
        val = '-' + val.replace('(', '').replace(')', '')
    try:
        return float(val)
    except:
        return None

def parse_income_statement(year):
    """Parse income statement for a given year"""
    file_path = os.path.join(extracted_dir, f"income_statement_{year}.csv")
    
    # Read the CSV
    df = pd.read_csv(file_path, header=None)
    
    print(f"\n{'='*70}")
    print(f"Parsing Income Statement FY {year}")
    print('='*70)
    
    # For 2023, columns are: [0]=Line Item, [1]=Notes, [2]=GROUP 2023, [3]=GROUP 2022, [4]=COMPANY 2023, [5]=COMPANY 2022
    # We'll extract GROUP column (column 2 for current year)
    
    metrics = {}
    
    for idx, row in df.iterrows():
        line_item = str(row[0]).lower() if pd.notna(row[0]) else ''
        
        # Get the value from column 2 (GROUP current year)
        value = clean_value(row[2]) if len(row) > 2 else None
        
        if 'total revenue' in line_item:
            metrics['Total Revenue'] = value
            print(f"✓ Total Revenue: {value:,.2f}" if value else "✗ Total Revenue: Not found")
        
        elif 'ebitda' in line_item and 'earnings before interest' in line_item:
            metrics['EBITDA'] = value
            print(f"✓ EBITDA: {value:,.2f}" if value else "✗ EBITDA: Not found")
        
        elif 'operating profit' in line_item:
            metrics['Operating Profit'] = value
            print(f"✓ Operating Profit: {value:,.2f}" if value else "✗ Operating Profit: Not found")
        
        elif 'profit before' in line_item and 'tax' in line_item:
            metrics['Profit Before Tax'] = value
            print(f"✓ Profit Before Tax: {value:,.2f}" if value else "✗ Profit Before Tax: Not found")
        
        elif 'profit for the year' in line_item and 'attributable' not in line_item:
            metrics['Net Profit'] = value
            print(f"✓ Net Profit: {value:,.2f}" if value else "✗ Net Profit: Not found")
    
    # Create result dataframe
    result = pd.DataFrame([{
        'Fiscal Year': int(year),
        'Total Revenue (KShs M)': metrics.get('Total Revenue'),
        'EBITDA (KShs M)': metrics.get('EBITDA'),
        'Operating Profit (KShs M)': metrics.get('Operating Profit'),
        'Profit Before Tax (KShs M)': metrics.get('Profit Before Tax'),
        'Net Profit (KShs M)': metrics.get('Net Profit')
    }])
    
    return result

# Process all years
print("\n" + "="*70)
print("EXTRACTING KEY FINANCIAL METRICS FROM SAFARICOM REPORTS")
print("="*70)

all_data = []

for year in ['2023', '2024', '2025']:
    try:
        df = parse_income_statement(year)
        all_data.append(df)
    except Exception as e:
        print(f"\n✗ Error processing {year}: {str(e)}")

# Combine all years
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("\n" + "="*70)
    print("SUMMARY - ALL YEARS")
    print("="*70)
    print(combined_df.to_string(index=False))
    
    # Calculate some basic metrics
    print("\n" + "="*70)
    print("FINANCIAL RATIOS")
    print("="*70)
    
    for idx, row in combined_df.iterrows():
        year = row['Fiscal Year']
        revenue = row['Total Revenue (KShs M)']
        ebitda = row['EBITDA (KShs M)']
        net_profit = row['Net Profit (KShs M)']
        
        print(f"\nFY {year}:")
        if revenue and ebitda:
            ebitda_margin = (ebitda / revenue) * 100
            print(f"  EBITDA Margin: {ebitda_margin:.2f}%")
        
        if revenue and net_profit:
            net_margin = (net_profit / revenue) * 100
            print(f"  Net Profit Margin: {net_margin:.2f}%")
    
    # Year-over-year growth
    print("\n" + "="*70)
    print("YEAR-OVER-YEAR GROWTH")
    print("="*70)
    
    for i in range(1, len(combined_df)):
        prev = combined_df.iloc[i-1]
        curr = combined_df.iloc[i]
        
        print(f"\nFY {int(prev['Fiscal Year'])} → FY {int(curr['Fiscal Year'])}:")
        
        if prev['Total Revenue (KShs M)'] and curr['Total Revenue (KShs M)']:
            growth = ((curr['Total Revenue (KShs M)'] - prev['Total Revenue (KShs M)']) / prev['Total Revenue (KShs M)']) * 100
            print(f"  Revenue Growth: {growth:.2f}%")
        
        if prev['Net Profit (KShs M)'] and curr['Net Profit (KShs M)']:
            growth = ((curr['Net Profit (KShs M)'] - prev['Net Profit (KShs M)']) / prev['Net Profit (KShs M)']) * 100
            print(f"  Net Profit Growth: {growth:.2f}%")
    
    # Save
    output_file = os.path.join(processed_dir, "safaricom_financial_summary.csv")
    combined_df.to_csv(output_file, index=False)
    
    print("\n" + "="*70)
    print(f"✓ Data saved to: {output_file}")
    print("="*70 + "\n")
