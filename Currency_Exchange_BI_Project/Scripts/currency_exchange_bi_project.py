from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Define project folders
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_FOLDER = PROJECT_ROOT / "Data" / "Raw"
PROCESSED_DATA_FOLDER = PROJECT_ROOT / "Data" / "Processed"

PROCESSED_DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 2. Find the latest raw CSV file
# ---------------------------------------------------------

raw_csv_files = list(RAW_DATA_FOLDER.glob("currency_rates_*.csv"))

if not raw_csv_files:
    print("No raw CSV files were found.")
    raise SystemExit(1)

latest_raw_file = max(
    raw_csv_files,
    key=lambda file: file.stat().st_mtime
)

print("Latest raw file selected:")
print(latest_raw_file)


# ---------------------------------------------------------
# 3. Load the raw data
# ---------------------------------------------------------

currency_dataframe = pd.read_csv(latest_raw_file)

print("\nRaw data loaded successfully.")
print("Raw rows:", len(currency_dataframe))


# ---------------------------------------------------------
# 4. Clean column names
# ---------------------------------------------------------

currency_dataframe.columns = (
    currency_dataframe.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ---------------------------------------------------------
# 5. Remove duplicate rows
# ---------------------------------------------------------

before_duplicates = len(currency_dataframe)

currency_dataframe = currency_dataframe.drop_duplicates()

after_duplicates = len(currency_dataframe)

print(
    "Duplicate rows removed:",
    before_duplicates - after_duplicates
)


# ---------------------------------------------------------
# 6. Handle missing values
# ---------------------------------------------------------

missing_values = currency_dataframe.isnull().sum()

print("\nMissing values before cleaning:")
print(missing_values)

currency_dataframe = currency_dataframe.dropna(
    subset=[
        "rate_date",
        "base_currency",
        "target_currency",
        "exchange_rate"
    ]
)


# ---------------------------------------------------------
# 7. Correct data types
# ---------------------------------------------------------

currency_dataframe["rate_date"] = pd.to_datetime(
    currency_dataframe["rate_date"],
    errors="coerce"
)

currency_dataframe["collection_timestamp"] = pd.to_datetime(
    currency_dataframe["collection_timestamp"],
    errors="coerce"
)

currency_dataframe["exchange_rate"] = pd.to_numeric(
    currency_dataframe["exchange_rate"],
    errors="coerce"
)

currency_dataframe = currency_dataframe.dropna(
    subset=["rate_date", "exchange_rate"]
)


# ---------------------------------------------------------
# 8. Standardize currency codes
# ---------------------------------------------------------

currency_dataframe["base_currency"] = (
    currency_dataframe["base_currency"]
    .astype(str)
    .str.strip()
    .str.upper()
)

currency_dataframe["target_currency"] = (
    currency_dataframe["target_currency"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ---------------------------------------------------------
# 9. Create business-analysis columns
# ---------------------------------------------------------

currency_dataframe["inverse_rate"] = (
    1 / currency_dataframe["exchange_rate"]
).round(6)

currency_dataframe["rate_strength_category"] = pd.cut(
    currency_dataframe["exchange_rate"],
    bins=[0, 1, 10, 100, float("inf")],
    labels=[
        "Below 1",
        "Between 1 and 10",
        "Between 10 and 100",
        "Above 100"
    ]
)

currency_dataframe["collection_date"] = (
    currency_dataframe["collection_timestamp"].dt.date
)

currency_dataframe["collection_hour"] = (
    currency_dataframe["collection_timestamp"].dt.hour
)


# ---------------------------------------------------------
# 10. Sort the cleaned data
# ---------------------------------------------------------

currency_dataframe = currency_dataframe.sort_values(
    by=["rate_date", "target_currency"]
).reset_index(drop=True)


# ---------------------------------------------------------
# 11. Save the processed file
# ---------------------------------------------------------

processed_file = (
    PROCESSED_DATA_FOLDER
    / "cleaned_currency_rates.csv"
)

currency_dataframe.to_csv(
    processed_file,
    index=False
)

print("\nProcessed file saved successfully:")
print(processed_file)


# ---------------------------------------------------------
# 12. Display the cleaned data
# ---------------------------------------------------------

print("\nCleaned currency data:")
print(currency_dataframe)

print("\nCleaning completed successfully.")
print("Final number of rows:", len(currency_dataframe))
print("Final number of columns:", len(currency_dataframe.columns))