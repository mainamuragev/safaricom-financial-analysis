-- Create database schema for Safaricom financial analysis

-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ticker VARCHAR(10),
    sector VARCHAR(100),
    country VARCHAR(100)
);

-- Financial periods table
CREATE TABLE IF NOT EXISTS financial_periods (
    period_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(company_id),
    fiscal_year INTEGER NOT NULL,
    period_end_date DATE NOT NULL,
    report_type VARCHAR(50) -- 'Annual', 'Quarterly', etc.
);

-- Income statement line items
CREATE TABLE IF NOT EXISTS income_statement (
    id SERIAL PRIMARY KEY,
    period_id INTEGER REFERENCES financial_periods(period_id),
    line_item VARCHAR(255) NOT NULL,
    value_kshs_millions NUMERIC(15, 2),
    notes VARCHAR(50)
);

-- Balance sheet line items
CREATE TABLE IF NOT EXISTS balance_sheet (
    id SERIAL PRIMARY KEY,
    period_id INTEGER REFERENCES financial_periods(period_id),
    line_item VARCHAR(255) NOT NULL,
    category VARCHAR(100), -- 'Current Assets', 'Non-current Assets', etc.
    value_kshs_millions NUMERIC(15, 2),
    notes VARCHAR(50)
);

-- Cash flow statement line items
CREATE TABLE IF NOT EXISTS cash_flow (
    id SERIAL PRIMARY KEY,
    period_id INTEGER REFERENCES financial_periods(period_id),
    line_item VARCHAR(255) NOT NULL,
    category VARCHAR(100), -- 'Operating', 'Investing', 'Financing'
    value_kshs_millions NUMERIC(15, 2),
    notes VARCHAR(50)
);

-- Calculated financial metrics
CREATE TABLE IF NOT EXISTS financial_metrics (
    metric_id SERIAL PRIMARY KEY,
    period_id INTEGER REFERENCES financial_periods(period_id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC(15, 4),
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_income_period ON income_statement(period_id);
CREATE INDEX IF NOT EXISTS idx_balance_period ON balance_sheet(period_id);
CREATE INDEX IF NOT EXISTS idx_cashflow_period ON cash_flow(period_id);
CREATE INDEX IF NOT EXISTS idx_metrics_period ON financial_metrics(period_id);
