import pandas as pd
import os

# Read the processed data
df = pd.read_csv('data/processed/safaricom_3year_analysis.csv')

# Create a formatted report
report = []
report.append("="*80)
report.append("SAFARICOM PLC - FINANCIAL ANALYSIS REPORT (FY 2023-2025)")
report.append("="*80)
report.append("")

# Summary statistics
report.append("EXECUTIVE SUMMARY")
report.append("-"*80)
report.append(f"Analysis Period: FY 2023 - FY 2025")
report.append(f"Company: Safaricom PLC (NSE: SCOM)")
report.append(f"Currency: Kenya Shillings (KShs) - Millions")
report.append("")

# Key findings
report.append("KEY FINDINGS:")
report.append("")

# Revenue trend
revenue_cagr = (((df.iloc[-1]['Total Revenue (KShs M)'] / df.iloc[0]['Total Revenue (KShs M)']) ** (1/2)) - 1) * 100
report.append(f"1. Revenue CAGR (2023-2025): {revenue_cagr:.2f}%")
report.append(f"   - FY 2023: KShs {df.iloc[0]['Total Revenue (KShs M)']:,.0f}M")
report.append(f"   - FY 2024: KShs {df.iloc[1]['Total Revenue (KShs M)']:,.0f}M (+12.4%)")
report.append(f"   - FY 2025: KShs {df.iloc[2]['Total Revenue (KShs M)']:,.0f}M (+11.2%)")
report.append("")

# Profitability
report.append("2. Profitability Trends:")
for idx, row in df.iterrows():
    year = int(row['Fiscal Year'])
    ebitda_margin = (row['EBITDA (KShs M)'] / row['Total Revenue (KShs M)']) * 100
    net_margin = (row['Net Profit (KShs M)'] / row['Total Revenue (KShs M)']) * 100
    report.append(f"   FY {year}: EBITDA Margin {ebitda_margin:.2f}% | Net Margin {net_margin:.2f}%")
report.append("")

# Net profit analysis
report.append("3. Net Profit Performance:")
report.append(f"   - FY 2023: KShs {df.iloc[0]['Net Profit (KShs M)']:,.0f}M")
report.append(f"   - FY 2024: KShs {df.iloc[1]['Net Profit (KShs M)']:,.0f}M (-18.7%)")
report.append(f"   - FY 2025: KShs {df.iloc[2]['Net Profit (KShs M)']:,.0f}M (+7.3%)")
report.append("")

# Detailed table
report.append("")
report.append("="*80)
report.append("DETAILED FINANCIAL METRICS")
report.append("="*80)
report.append("")
report.append(df.to_string(index=False))
report.append("")

# Observations
report.append("="*80)
report.append("OBSERVATIONS")
report.append("="*80)
report.append("")
report.append("STRENGTHS:")
report.append("• Consistent double-digit revenue growth (11-12% annually)")
report.append("• Strong EBITDA margins above 44%")
report.append("• Recovery in net profit in FY 2025")
report.append("")
report.append("CONCERNS:")
report.append("• Net profit declined significantly in FY 2024 despite revenue growth")
report.append("• Declining net profit margins (16.88% → 11.77%)")
report.append("• Suggests increasing operational costs or other expenses")
report.append("")

# Methodology
report.append("="*80)
report.append("METHODOLOGY")
report.append("="*80)
report.append("")
report.append("Data Source: Safaricom PLC Annual Reports (FY 2023, 2024, 2025)")
report.append("Extraction Method: Automated PDF parsing using Python (pdfplumber)")
report.append("Data Points: Income Statement metrics from consolidated GROUP results")
report.append("Analysis Date: January 2026")
report.append("")
report.append("="*80)
report.append("END OF REPORT")
report.append("="*80)

# Print and save report
report_text = '\n'.join(report)
print(report_text)

# Save to file
output_file = 'data/processed/SAFARICOM_FINANCIAL_REPORT.txt'
with open(output_file, 'w') as f:
    f.write(report_text)

print(f"\n✓ Report saved to: {output_file}")
