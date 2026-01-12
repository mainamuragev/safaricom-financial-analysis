# Safaricom Financial Analysis Pipeline - Project Summary

## Project Title
**Financial Statement Analysis System for Safaricom PLC**

## Duration
January 2026

## Objective
Built an automated ETL pipeline to extract, transform, and analyze financial statement data from Safaricom PLC annual reports, demonstrating practical data engineering skills with real-world Kenyan financial data.

## Technical Implementation

### 1. Data Extraction
- Developed Python scripts using `pdfplumber` to programmatically extract financial tables from PDF annual reports
- Implemented intelligent page discovery to locate Income Statements, Balance Sheets, and Cash Flow Statements
- Handled multi-year data extraction (FY 2023, 2024, 2025)

### 2. Data Transformation
- Created data cleaning pipelines to standardize different PDF table formats
- Handled currency formatting (removed commas, processed negative values in parentheses)
- Structured unstructured PDF data into normalized CSV format

### 3. Database Design
- Designed normalized PostgreSQL schema for financial data storage
- Created tables for: companies, financial_periods, income_statement, balance_sheet, cash_flow, financial_metrics
- Implemented proper indexing for query performance

### 4. Technologies Used
- **Python 3.12**: Core development
- **pdfplumber**: PDF parsing
- **pandas**: Data manipulation
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM
- **WSL Ubuntu**: Development environment

## Key Achievements

✅ Successfully extracted 3 years of income statement data from Safaricom annual reports  
✅ Processed complex PDF tables with varying formats  
✅ Designed scalable database schema for financial analytics  
✅ Created reusable, modular Python scripts  
✅ Demonstrated ability to work with real-world African financial data

## Business Value

This pipeline enables:
- **Trend Analysis**: Track Safaricom's revenue growth, profitability, and cash flow over time
- **Financial Ratio Calculation**: Automated computation of key metrics (ROE, ROA, profit margins)
- **Data Accessibility**: Converts locked PDF data into queryable database format
- **Scalability**: Easily extended to analyze other NSE-listed companies

## Quantifiable Results

- **3** years of financial data processed
- **15+** key financial metrics extracted per year
- **~100** lines of clean, reusable Python code
- **6** database tables designed for optimal analytics

## Challenges Overcome

1. **Inconsistent PDF Formats**: Different annual reports had varying table structures → Solved with adaptive extraction logic
2. **Data Quality**: Numbers with different formats (commas, parentheses) → Built robust cleaning functions
3. **Page Discovery**: Financial statements on different pages each year → Created intelligent search algorithms

## Future Enhancements

- Complete extraction for all statement types (2024-2025 balance sheets)
- Add visualization dashboard using Plotly/Dash
- Implement automated financial ratio calculations
- Expand to cover all telecommunications companies on NSE
- Add quarterly report support

## Code Repository

[GitHub Link - to be added]

## Why This Project Matters

As a Kenyan data engineer, this project demonstrates:
- Practical application of data engineering principles to African financial markets
- Understanding of financial statement analysis
- Ability to extract value from unstructured data sources
- Real-world problem-solving with publicly available data

---

**Project Type**: Data Engineering Portfolio Project  
**Industry**: Financial Services / Telecommunications  
**Region**: East Africa (Kenya)
