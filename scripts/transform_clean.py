import pandas as pd
import re
import os

extracted_dir = "data/extracted"
processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

def clean_value(val):
    """Clean financial values - remove commas, handle negatives"""
    if pd.isna(val) or val == '' or val is None:
        return None
    
    val = str(val).strip().replace(',', '')
    
    # Handle parentheses (negative numbers)
    if '(' in val and ')' in val:
        val = '-' + val.replace('(', '').replace(')', '')
    
    try:
        return float(val)
    except:
        return None

def extract_key_metrics_from_raw(year):
    """Extract key financial metrics from raw CSV"""
    
    file_path = os.path.join(extracted_dir, f"income_statement_{year}.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    # Read raw CSV
    df_raw = pd.read_csv(file_path, header=None)
    
    # Define the key metrics we want to extract
    metrics = {
        'Total Revenue': None,
        'Direct Costs': None,
        'EBITDA': None,
        'Operating Profit': None,
        'Profit Before Tax': None,
        'Net Profit': None
    }
    
    # Search through the dataframe for these metrics
    for idx, row in df_raw.iterrows():
        row_str = ' '.join([str(x) for x in row if pd.notna(x)]).lower()
        
        if 'total revenue' in row_str and metrics['Total Revenue'] is None:
            # Get the first numeric value we can find
            for val in row:
                cleaned = clean_value(val)
                if cleaned and cleaned > 100000:  # Revenue should be large
                    metrics['Total Revenue'] = cleaned
                    break
        
        elif 'direct costs' in row_str and metrics['Direct Costs'] is None:
            for val in row:
                cleaned = clean_value(val)
                if cleaned and abs(cleaned) > 50000:
                    metrics['Direct Costs'] = cleaned
                    break
        
        elif 'ebitda' in row_str and 'earnings before interest' in row_str:
            if metrics['EBITDA'] is None:
                for val in row:
                    cleaned = clean_value(val)
                    if cleaned and cleaned > 100000:
                        metrics['EBITDA'] = cleaned
                        break
        
        elif 'operating profit' in row_str and metrics['Operating Profit'] is None:
            for val in row:
                cleaned = clean_value(val)
                if cleaned and cleaned > 50000:
                    metrics['Operating Profit'] = cleaned
                    break
        
        elif 'profit before' in row_str and 'tax' in row_str:
            if metrics['Profit Before Tax'] is None:
                for val in row:
                    cleaned = clean_value(val)
                    if cleaned and cleaned > 50000:
                        metrics['Profit Before Tax'] = cleaned
                        break
        
        elif 'profit for the year' in row_str and metrics['Net Profit'] is None:
            for val in row:
                cleaned = clean_value(val)
                if cleaned and cleaned > 30000:
                    metrics['Net Profit'] = cleaned
                    break
    
    # Create structured dataframe
    result = pd.DataFrame([{
        'Fiscal Year': year,
        'Total Revenue (KShs M)': metrics['Total Revenue'],
        'Direct Costs (KShs M)': metrics['Direct Costs'],
        'EBITDA (KShs M)': metrics['EBITDA'],
        'Operating Profit (KShs M)': metrics['Operating Profit'],
        'Profit Before Tax (KShs M)': metrics['Profit Before Tax'],
        'Net Profit (KShs M)': metrics['Net Profit']
    }])
    
    return result

print("\n" + "="*70)
print("TRANSFORMING FINANCIAL DATA")
print("="*70)

# Process each year
all_data = []

for year in ['2023', '2024', '2025']:
    print(f"\nProcessing FY {year}...")
    df = extract_key_metrics_from_raw(year)
    
    if df is not None:
        print(f"✓ Extracted metrics for {year}")
        print(df.to_string(index=False))
        all_data.append(df)
    else:
        print(f"✗ Failed to process {year}")

# Combine all years
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Save to processed directory
    output_file = os.path.join(processed_dir, "income_statement_summary.csv")
    combined_df.to_csv(output_file, index=False)
    
    print("\n" + "="*70)
    print("FINAL SUMMARY - ALL YEARS")
    print("="*70)
    print(combined_df.to_string(index=False))
    
    # Calculate year-over-year growth
    print("\n" + "="*70)
    print("YEAR-OVER-YEAR GROWTH ANALYSIS")
    print("="*70)
    
    if len(combined_df) > 1:
        for i in range(1, len(combined_df)):
            prev_year = combined_df.iloc[i-1]['Fiscal Year']
            curr_year = combined_df.iloc[i]['Fiscal Year']
            
            prev_revenue = combined_df.iloc[i-1]['Total Revenue (KShs M)']
            curr_revenue = combined_df.iloc[i]['Total Revenue (KShs M)']
            
            if prev_revenue and curr_revenue:
                growth = ((curr_revenue - prev_revenue) / prev_revenue) * 100
                print(f"Revenue Growth {prev_year} → {curr_year}: {growth:.2f}%")
            
            prev_profit = combined_df.iloc[i-1]['Net Profit (KShs M)']
            curr_profit = combined_df.iloc[i]['Net Profit (KShs M)']
            
            if prev_profit and curr_profit:
                growth = ((curr_profit - prev_profit) / prev_profit) * 100
                print(f"Net Profit Growth {prev_year} → {curr_year}: {growth:.2f}%")
    
    print("\n" + "="*70)
    print(f"✓ Summary saved to: {output_file}")
    print("="*70 + "\n")
