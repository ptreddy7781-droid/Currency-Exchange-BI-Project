import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests


# ---------------------------------------------------------
# 1. Project folder paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_FOLDER = PROJECT_ROOT / "Data" / "Raw"

RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 2. API settings
# ---------------------------------------------------------

API_URL = "https://api.frankfurter.dev/v1/latest"

PARAMETERS = {
    "base": "EUR",
    "symbols": "USD,GBP,INR,CHF,JPY,CAD,AUD"
}


# ---------------------------------------------------------
# 3. Extract data from the API
# ---------------------------------------------------------

print("Connecting to the Frankfurter API...")

try:
    response = requests.get(
        API_URL,
        params=PARAMETERS,
        timeout=30
    )

    response.raise_for_status()
    api_data = response.json()

    print("Data collected successfully.")

except requests.exceptions.RequestException as error:
    print("API connection failed.")
    print("Error:", error)
    raise SystemExit(1)


# ---------------------------------------------------------
# 4. Create timestamped file names
# ---------------------------------------------------------

collection_time = datetime.now()
timestamp = collection_time.strftime("%Y%m%d_%H%M%S")

json_file = RAW_DATA_FOLDER / f"currency_rates_{timestamp}.json"
csv_file = RAW_DATA_FOLDER / f"currency_rates_{timestamp}.csv"


# ---------------------------------------------------------
# 5. Save the original JSON response
# ---------------------------------------------------------

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(api_data, file, indent=4)

print("Raw JSON file saved:", json_file)


# ---------------------------------------------------------
# 6. Convert the rates into a table
# ---------------------------------------------------------

records = []

for currency_code, exchange_rate in api_data["rates"].items():
    records.append(
        {
            "rate_date": api_data["date"],
            "base_currency": api_data["base"],
            "target_currency": currency_code,
            "exchange_rate": exchange_rate,
            "collection_timestamp": collection_time
        }
    )

currency_dataframe = pd.DataFrame(records)


# ---------------------------------------------------------
# 7. Save the raw CSV file
# ---------------------------------------------------------

currency_dataframe.to_csv(
    csv_file,
    index=False
)

print("Raw CSV file saved:", csv_file)


# ---------------------------------------------------------
# 8. Display the collected data
# ---------------------------------------------------------

print("\nCurrency exchange rates:")
print(currency_dataframe)

print("\nExtraction completed successfully.")
print("Total records collected:", len(currency_dataframe))