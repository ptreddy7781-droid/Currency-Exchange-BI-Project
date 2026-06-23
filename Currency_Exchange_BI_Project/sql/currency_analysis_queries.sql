-- 1. View all currency records
SELECT *
FROM public.currency_rates
ORDER BY target_currency;


-- 2. Count total records
SELECT COUNT(*) AS total_records
FROM public.currency_rates;


-- 3. Show the highest exchange rate
SELECT
    target_currency,
    exchange_rate
FROM public.currency_rates
ORDER BY exchange_rate DESC
LIMIT 1;


-- 4. Show the lowest exchange rate
SELECT
    target_currency,
    exchange_rate
FROM public.currency_rates
ORDER BY exchange_rate ASC
LIMIT 1;


-- 5. Compare all exchange rates
SELECT
    target_currency,
    exchange_rate,
    inverse_rate,
    rate_strength_category
FROM public.currency_rates
ORDER BY exchange_rate DESC;


-- 6. Count currencies by strength category
SELECT
    rate_strength_category,
    COUNT(*) AS currency_count
FROM public.currency_rates
GROUP BY rate_strength_category
ORDER BY currency_count DESC;


-- 7. Show currencies with an exchange rate below 1
SELECT
    target_currency,
    exchange_rate
FROM public.currency_rates
WHERE exchange_rate < 1
ORDER BY exchange_rate;


-- 8. Show currencies with an exchange rate above 10
SELECT
    target_currency,
    exchange_rate
FROM public.currency_rates
WHERE exchange_rate > 10
ORDER BY exchange_rate DESC;


-- 9. Calculate average exchange rate
SELECT
    ROUND(AVG(exchange_rate)::numeric, 4) AS average_exchange_rate
FROM public.currency_rates;


-- 10. Show the latest data collection time
SELECT
    MAX(collection_timestamp) AS latest_collection_time
FROM public.currency_rates;