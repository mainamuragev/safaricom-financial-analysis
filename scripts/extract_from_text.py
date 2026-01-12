import pdfplumber
import re
import pandas as pd
import os

processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

def extract_metrics_from_text(pdf_path, page_num, year):
    """Extract key metrics directly from PDF text"""
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        print(f"\nExtracting FY {year} from page {page_num + 1}...")
        
        # Find key metrics using regex
        metrics = {}
        
        # Total revenue pattern
        revenue_match = re.search(r'Total revenue.*?(\d{1,3}(?:,\d{3})*\.\d)', text, re.IGNORECASE | re.DOTALL)
        if revenue_match:
            metrics['Total Revenue'] = float(revenue_match.group(1).replace(',', ''))
            print(f"✓ Total Revenue: {metrics['Total Revenue']:,.2f}")
        
        # EBITDA pattern
        ebitda_match = re.search(r'(?:EBITDA|Earnings before interest.*?amortisation).*?(\d{1,3}(?:,\d{3})*\.\d)', text, re.IGNORECASE | re.DOTALL)
        if ebitda_match:
            metrics['EBITDA'] = float(ebitda_match.group(1).replace(',', ''))
            print(f"✓ EBITDA: {metrics['EBITDA']:,.2f}")
        
        # Operating profit
        op_profit_match = re.search(r'Operating profit.*?(\d{1,3}(?:,\d{3})*\.\d)', text, re.IGNORECASE | re.DOTALL)
        if op_profit_match:
            metrics['Operating Profit'] = float(op_profit_match.group(1).replace(',', ''))
            print(f"✓ Operating Profit: {metrics['Operating Profit']:,.2f}")
        
        # Profit before tax
        pbt_match = re.search(r'Profit before.*?tax.*?(\d{1,3}(?:,\d{3})*\.\d)', text, re.IGNORECASE | re.DOTALL)
        if pbt_match:
            metrics['Profit Before Tax'] = float(pbt_match.group(1).replace(',', ''))
            print(f"✓ Profit Before Tax: {metrics['Profit Before Tax']:,.2f}")
        
        # Net profit (profit for the year)
        # Look for the pattern more carefully
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'profit for the year' in line.lower() and i + 1 < len(lines):
                # Get next few lines to find numbers
                next_lines = ' '.join(lines[i:i+3])
                profit_match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d)', next_lines)
                if profit_match:
                    val = float(profit_match.group(1).replace(',', ''))
                    if val > 30000:  # Net profit should be substantial
                        metrics['Net Profit'] = val
                        print(f"✓ Net Profit: {metrics['Net Profit']:,.2f}")
                        break
        
        return metrics

# Process all three years
print("="*70)
print("EXTRACTING FINANCIAL METRICS FROM PDF TEXT")
print("="*70)

data = []

# 2023 - already have it from CSV parsing
df_2023 = pd.read_csv('data/processed/safaricom_financial_summary.csv')
data.append(df_2023.iloc[0].to_dict())

# 2024
metrics_2024 = extract_metrics_from_text(
    'data/raw/Safaricom 2024-Annual-Report-Update.pdf',
    180,  # Page 181
    2024
)
data.append({
    'Fiscal Year': 2024,
    'Total Revenue (KShs M)': metrics_2024.get('Total Revenue'),
    'EBITDA (KShs M)': metrics_2024.get('EBITDA'),
    'Operating Profit (KShs M)': metrics_2024.get('Operating Profit'),
    'Profit Before Tax (KShs M)': metrics_2024.get('Profit Before Tax'),
    'Net Profit (KShs M)': metrics_2024.get('Net Profit')
})

# 2025
metrics_2025 = extract_metrics_from_text(
    'data/raw/Safaricom Annual-2025-Reporrt.pdf',
    200,  # Page 201
    2025
)
data.append({
    'Fiscal Year': 2025,
    'Total Revenue (KShs M)': metrics_2025.get('Total Revenue'),
    'EBITDA (KShs M)': metrics_2025.get('EBITDA'),
    'Operating Profit (KShs M)': metrics_2025.get('Operating Profit'),
    'Profit Before Tax (KShs M)': metrics_2025.get('Profit Before Tax'),
    'Net Profit (KShs M)': metrics_2025.get('Net Profit')
})

# Create final dataframe
final_df = pd.DataFrame(data)

print("\n" + "="*70)
print("FINAL SUMMARY - ALL YEARS")
print("="*70)
print(final_df.to_string(index=False))

# Calculate metrics
print("\n" + "="*70)
print("FINANCIAL ANALYSIS")
print("="*70)

for idx, row in final_df.iterrows():
    year = int(row['Fiscal Year'])
    revenue = row['Total Revenue (KShs M)']
    ebitda = row['EBITDA (KShs M)']
    net_profit = row['Net Profit (KShs M)']
    
    print(f"\nFY {year}:")
    if pd.notna(revenue):
        print(f"  Total Revenue: KShs {revenue:,.2f}M")
    if pd.notna(ebitda) and pd.notna(revenue):
        margin = (ebitda / revenue) * 100
        print(f"  EBITDA Margin: {margin:.2f}%")
    if pd.notna(net_profit) and pd.notna(revenue):
        margin = (net_profit / revenue) * 100
        print(f"  Net Profit Margin: {margin:.2f}%")

# Growth analysis
print("\n" + "="*70)
print("YEAR-OVER-YEAR GROWTH")
print("="*70)

for i in range(1, len(final_df)):
    prev = final_df.iloc[i-1]
    curr = final_df.iloc[i]
    
    prev_year = int(prev['Fiscal Year'])
    curr_year = int(curr['Fiscal Year'])
    
    print(f"\nFY {prev_year} → FY {curr_year}:")
    
    if pd.notna(prev['Total Revenue (KShs M)']) and pd.notna(curr['Total Revenue (KShs M)']):
        growth = ((curr['Total Revenue (KShs M)'] - prev['Total Revenue (KShs M)']) / prev['Total Revenue (KShs M)']) * 100
        print(f"  Revenue Growth: {growth:+.2f}%")
        delta = curr['Total Revenue (KShs M)'] - prev['Total Revenue (KShs M)']
        print(f"  Revenue Change: KShs {delta:,.2f}M")
    
    if pd.notna(prev['Net Profit (KShs M)']) and pd.notna(curr['Net Profit (KShs M)']):
        growth = ((curr['Net Profit (KShs M)'] - prev['Net Profit (KShs M)']) / prev['Net Profit (KShs M)']) * 100
        print(f"  Net Profit Growth: {growth:+.2f}%")
        delta = curr['Net Profit (KShs M)'] - prev['Net Profit (KShs M)']
        print(f"  Net Profit Change: KShs {delta:,.2f}M")

# Save final result
output_file = os.path.join(processed_dir, "safaricom_3year_analysis.csv")
final_df.to_csv(output_file, index=False)

print("\n" + "="*70)
print(f"✓ Complete analysis saved to: {output_file}")
print("="*70 + "\n")
