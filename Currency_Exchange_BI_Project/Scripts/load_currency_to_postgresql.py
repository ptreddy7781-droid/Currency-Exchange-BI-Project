from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ---------------------------------------------------------
# 1. Define project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
    PROJECT_ROOT
    / "Data"
    / "Processed"
    / "cleaned_currency_rates.csv"
)

ENV_FILE = PROJECT_ROOT / ".env"


# ---------------------------------------------------------
# 2. Load database credentials
# ---------------------------------------------------------

load_dotenv(ENV_FILE)

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


required_settings = {
    "DB_HOST": db_host,
    "DB_PORT": db_port,
    "DB_NAME": db_name,
    "DB_USER": db_user,
    "DB_PASSWORD": db_password,
}

missing_settings = [
    setting_name
    for setting_name, setting_value in required_settings.items()
    if not setting_value
]

if missing_settings:
    print("Missing database settings:", missing_settings)
    raise SystemExit(1)


# ---------------------------------------------------------
# 3. Check processed CSV file
# ---------------------------------------------------------

if not PROCESSED_FILE.exists():
    print("Processed CSV file was not found:")
    print(PROCESSED_FILE)
    raise SystemExit(1)


# ---------------------------------------------------------
# 4. Read cleaned data
# ---------------------------------------------------------

currency_dataframe = pd.read_csv(PROCESSED_FILE)

currency_dataframe["rate_date"] = pd.to_datetime(
    currency_dataframe["rate_date"]
)

currency_dataframe["collection_timestamp"] = pd.to_datetime(
    currency_dataframe["collection_timestamp"]
)

currency_dataframe["collection_date"] = pd.to_datetime(
    currency_dataframe["collection_date"]
).dt.date

print("Processed data loaded successfully.")
print("Rows ready for database:", len(currency_dataframe))


# ---------------------------------------------------------
# 5. Create PostgreSQL connection
# ---------------------------------------------------------

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=db_user,
    password=db_password,
    host=db_host,
    port=int(db_port),
    database=db_name,
)

engine = create_engine(database_url)


# ---------------------------------------------------------
# 6. Test database connection
# ---------------------------------------------------------

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database();")
        )

        connected_database = result.scalar()

        print("PostgreSQL connection successful.")
        print("Connected database:", connected_database)

except Exception as error:
    print("PostgreSQL connection failed.")
    print("Error:", error)
    raise SystemExit(1)


# ---------------------------------------------------------
# 7. Load data into PostgreSQL
# ---------------------------------------------------------

table_name = "currency_rates"

try:
    currency_dataframe.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi"
    )

    print("Data loaded into PostgreSQL successfully.")
    print("Table created:", table_name)

except Exception as error:
    print("Failed to load data into PostgreSQL.")
    print("Error:", error)
    raise SystemExit(1)


# ---------------------------------------------------------
# 8. Verify stored records
# ---------------------------------------------------------

with engine.connect() as connection:
    record_count = connection.execute(
        text("SELECT COUNT(*) FROM currency_rates;")
    ).scalar()

print("Database verification completed.")
print("Records stored:", record_count)