-- =========================================================
-- Currency Exchange BI Project
-- PostgreSQL Database Setup
-- =========================================================

-- IMPORTANT:
-- Run the CREATE DATABASE statement while connected to the
-- default PostgreSQL database, such as "postgres".

CREATE DATABASE currency_exchange_db;

-- After creating the database, connect to:
-- currency_exchange_db
-- Then run the remaining statements below.

CREATE TABLE IF NOT EXISTS public.currency_rates (
id SERIAL PRIMARY KEY,
base_currency VARCHAR(10) NOT NULL,
target_currency VARCHAR(10) NOT NULL,
exchange_rate NUMERIC(20, 8) NOT NULL,
inverse_rate NUMERIC(20, 8),
rate_date DATE,
collected_at TIMESTAMP,
collection_hour INTEGER,
rate_strength_category VARCHAR(50),
source VARCHAR(100)
);

-- Create an index for faster currency searches
CREATE INDEX IF NOT EXISTS idx_currency_rates_target_currency
ON public.currency_rates(target_currency);

-- Create an index for date-based analysis
CREATE INDEX IF NOT EXISTS idx_currency_rates_rate_date
ON public.currency_rates(rate_date);

-- View the table structure
SELECT
column_name,
data_type,
is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name = 'currency_rates'
ORDER BY ordinal_position;

-- View the loaded data
SELECT *
FROM public.currency_rates
ORDER BY exchange_rate DESC;
