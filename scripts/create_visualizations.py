import pandas as pd
import matplotlib.pyplot as plt
import os

# Create visualizations directory
viz_dir = 'visualizations'
os.makedirs(viz_dir, exist_ok=True)

# Read the processed data
df = pd.read_csv('data/processed/safaricom_3year_analysis.csv')

# Set style for better-looking charts
plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#2E7D32', '#1976D2', '#D32F2F']  # Green, Blue, Red

print("="*70)
print("CREATING VISUALIZATIONS")
print("="*70)

# 1. Revenue Trend Chart
fig, ax = plt.subplots(figsize=(12, 6))
years = df['Fiscal Year'].astype(int)
revenue = df['Total Revenue (KShs M)']

ax.plot(years, revenue, marker='o', linewidth=3, markersize=10, color='#2E7D32')
ax.fill_between(years, revenue, alpha=0.3, color='#2E7D32')

# Add value labels
for i, (x, y) in enumerate(zip(years, revenue)):
    ax.text(x, y + 5000, f'KShs {y:,.0f}M', ha='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Revenue (KShs Millions)', fontsize=12, fontweight='bold')
ax.set_title('Safaricom Revenue Growth (FY 2023-2025)', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)

plt.tight_layout()
plt.savefig(f'{viz_dir}/1_revenue_trend.png', dpi=300, bbox_inches='tight')
print("✓ Created: 1_revenue_trend.png")
plt.close()

# 2. Profitability Metrics (Bar Chart)
fig, ax = plt.subplots(figsize=(12, 6))

metrics = ['EBITDA (KShs M)', 'Operating Profit (KShs M)', 'Net Profit (KShs M)']
x = range(len(years))
width = 0.25

for i, metric in enumerate(metrics):
    values = df[metric]
    offset = (i - 1) * width
    bars = ax.bar([p + offset for p in x], values, width, label=metric.replace(' (KShs M)', ''), 
                   color=colors[i], alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}M', ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Amount (KShs Millions)', fontsize=12, fontweight='bold')
ax.set_title('Safaricom Profitability Metrics (FY 2023-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(years.astype(int))
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{viz_dir}/2_profitability_metrics.png', dpi=300, bbox_inches='tight')
print("✓ Created: 2_profitability_metrics.png")
plt.close()

# 3. Profit Margins (Line Chart)
fig, ax = plt.subplots(figsize=(12, 6))

# Calculate margins
ebitda_margin = (df['EBITDA (KShs M)'] / df['Total Revenue (KShs M)']) * 100
net_margin = (df['Net Profit (KShs M)'] / df['Total Revenue (KShs M)']) * 100

ax.plot(years, ebitda_margin, marker='o', linewidth=3, markersize=10, 
        label='EBITDA Margin', color='#1976D2')
ax.plot(years, net_margin, marker='s', linewidth=3, markersize=10, 
        label='Net Profit Margin', color='#D32F2F')

# Add value labels
for i, (x, y1, y2) in enumerate(zip(years, ebitda_margin, net_margin)):
    ax.text(x, y1 + 1, f'{y1:.1f}%', ha='center', fontsize=10, fontweight='bold', color='#1976D2')
    ax.text(x, y2 - 2, f'{y2:.1f}%', ha='center', fontsize=10, fontweight='bold', color='#D32F2F')

ax.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Margin (%)', fontsize=12, fontweight='bold')
ax.set_title('Safaricom Profit Margins Trend (FY 2023-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(years)
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 60)

plt.tight_layout()
plt.savefig(f'{viz_dir}/3_profit_margins.png', dpi=300, bbox_inches='tight')
print("✓ Created: 3_profit_margins.png")
plt.close()

# 4. Year-over-Year Growth Rates
fig, ax = plt.subplots(figsize=(12, 6))

# Calculate growth rates
revenue_growth = []
profit_growth = []

for i in range(1, len(df)):
    rev_growth = ((df.iloc[i]['Total Revenue (KShs M)'] - df.iloc[i-1]['Total Revenue (KShs M)']) / 
                  df.iloc[i-1]['Total Revenue (KShs M)']) * 100
    prof_growth = ((df.iloc[i]['Net Profit (KShs M)'] - df.iloc[i-1]['Net Profit (KShs M)']) / 
                   df.iloc[i-1]['Net Profit (KShs M)']) * 100
    revenue_growth.append(rev_growth)
    profit_growth.append(prof_growth)

growth_years = [f'{int(years.iloc[i-1])}→{int(years.iloc[i])}' for i in range(1, len(years))]
x = range(len(growth_years))
width = 0.35

bars1 = ax.bar([p - width/2 for p in x], revenue_growth, width, label='Revenue Growth', 
               color='#2E7D32', alpha=0.8)
bars2 = ax.bar([p + width/2 for p in x], profit_growth, width, label='Net Profit Growth', 
               color='#D32F2F', alpha=0.8)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:+.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                fontsize=10, fontweight='bold')

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('Period', fontsize=12, fontweight='bold')
ax.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Safaricom Year-over-Year Growth Rates', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(growth_years)
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{viz_dir}/4_growth_rates.png', dpi=300, bbox_inches='tight')
print("✓ Created: 4_growth_rates.png")
plt.close()

# 5. Summary Dashboard (Multi-panel)
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Panel 1: Revenue
ax1 = fig.add_subplot(gs[0, 0])
ax1.bar(years, revenue, color='#2E7D32', alpha=0.7)
for x, y in zip(years, revenue):
    ax1.text(x, y, f'{y:,.0f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1.set_title('Total Revenue', fontsize=14, fontweight='bold')
ax1.set_ylabel('KShs Millions', fontsize=10)
ax1.grid(True, alpha=0.3, axis='y')

# Panel 2: Net Profit
ax2 = fig.add_subplot(gs[0, 1])
net_profit = df['Net Profit (KShs M)']
ax2.bar(years, net_profit, color='#D32F2F', alpha=0.7)
for x, y in zip(years, net_profit):
    ax2.text(x, y, f'{y:,.0f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.set_title('Net Profit', fontsize=14, fontweight='bold')
ax2.set_ylabel('KShs Millions', fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')

# Panel 3: Margins
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(years, ebitda_margin, marker='o', linewidth=2, markersize=8, label='EBITDA Margin', color='#1976D2')
ax3.plot(years, net_margin, marker='s', linewidth=2, markersize=8, label='Net Margin', color='#D32F2F')
ax3.set_title('Profit Margins', fontsize=14, fontweight='bold')
ax3.set_ylabel('Percentage (%)', fontsize=10)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)

# Panel 4: Key Metrics Summary (Text)
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

summary_text = f"""
KEY METRICS SUMMARY

Revenue CAGR (2023-2025):
    {(((revenue.iloc[-1] / revenue.iloc[0]) ** (1/2)) - 1) * 100:.2f}%

FY 2025 Performance:
    Revenue: KShs {revenue.iloc[-1]:,.0f}M
    EBITDA: KShs {df.iloc[-1]['EBITDA (KShs M)']:,.0f}M
    Net Profit: KShs {net_profit.iloc[-1]:,.0f}M

Margins (FY 2025):
    EBITDA Margin: {ebitda_margin.iloc[-1]:.2f}%
    Net Margin: {net_margin.iloc[-1]:.2f}%

Growth (2024→2025):
    Revenue: {revenue_growth[-1]:+.2f}%
    Net Profit: {profit_growth[-1]:+.2f}%
"""

ax4.text(0.1, 0.5, summary_text, fontsize=11, family='monospace', 
         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

fig.suptitle('Safaricom PLC - Financial Performance Dashboard (FY 2023-2025)', 
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig(f'{viz_dir}/5_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Created: 5_dashboard.png")
plt.close()

print("\n" + "="*70)
print(f"✓ All visualizations saved to: {viz_dir}/")
print("="*70)
print("\nGenerated files:")
print("  1. 1_revenue_trend.png - Revenue growth over 3 years")
print("  2. 2_profitability_metrics.png - EBITDA, Operating Profit, Net Profit")
print("  3. 3_profit_margins.png - EBITDA and Net Profit margins")
print("  4. 4_growth_rates.png - Year-over-year growth rates")
print("  5. 5_dashboard.png - Comprehensive dashboard")
print("="*70 + "\n")
