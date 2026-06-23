# Currency Exchange Business Intelligence Project

## Project Overview

This project develops an automated Business Intelligence solution for collecting, cleaning, storing, analysing, and visualising currency exchange-rate data.

The system extracts live exchange rates from a public API using Python, processes the data with Pandas, stores the cleaned results in PostgreSQL, performs analysis using SQL and Jupyter Notebook, and presents the final insights through an interactive Power BI dashboard.

The complete pipeline is automated using Windows Task Scheduler.

## Project Objectives

* Extract currency exchange-rate data from a public API
* Clean and transform the raw data using Python and Pandas
* Store structured data in PostgreSQL
* Analyse exchange-rate patterns using SQL
* Perform exploratory analysis in Jupyter Notebook
* Create an interactive Power BI dashboard
* Automate the ETL pipeline using Windows Task Scheduler
* Maintain project documentation and code through GitHub

## Data Source

The project uses the Frankfurter currency exchange API.

Base currency:

```text
EUR
```

Target currencies:

```text
AUD
CAD
CHF
GBP
INR
JPY
USD
```

## Technology Stack

* Python
* Pandas
* Requests
* PostgreSQL
* pgAdmin
* SQLAlchemy
* Jupyter Notebook
* Matplotlib
* Power BI
* Windows Task Scheduler
* GitHub
* Visual Studio Code

## Project Architecture

```text
Currency Exchange API
        ↓
Python Data Extraction
        ↓
Raw JSON and CSV Files
        ↓
Pandas Data Cleaning
        ↓
Cleaned CSV File
        ↓
PostgreSQL Database
        ↓
SQL and Jupyter Analysis
        ↓
Power BI Dashboard
        ↓
Windows Task Scheduler Automation
```

## Project Folder Structure

```text
Currency_Exchange_BI_Project
│
├── architecture
│   └── Currency_Exchange_BI_Project_5_Slides_Corrected.pptx
│
├── dashboard
│   └── Currency_Exchange_Dashboard.pbix
│
├── Data
│   ├── Raw
│   └── Processed
│       └── cleaned_currency_rates.csv
│
├── logs
│   └── sample_pipeline_success.log
│
├── notebooks
│   └── currency_analysis.ipynb
│
├── screenshots
│   ├── 01_api_extraction.png
│   ├── 02_cleaned_data.png
│   ├── 03_postgresql_table.png
│   ├── 04_sql_analysis.png
│   ├── 05_jupyter_analysis.png
│   ├── 06_powerbi_overview.png
│   ├── 07_powerbi_comparison.png
│   ├── 08_pipeline_success.png
│   ├── 09_task_scheduler.png
│   └── 10_pipeline_log.png
│
├── Scripts
│   ├── extract_currency_data.py
│   ├── clean_currency_data.py
│   ├── load_currency_to_postgresql.py
│   └── run_pipeline.py
│
├── sql
│   ├── database_setup.sql
│   └── currency_analysis_queries.sql
│
├── .gitignore
├── README.md
├── requirements.txt
└── run_pipeline.bat
```

## ETL Pipeline

### 1. Extract

The extraction script connects to the currency exchange API and downloads the latest EUR-based exchange rates.

The raw response is stored as JSON and CSV files in:

```text
Data/Raw
```

### 2. Transform

The cleaning script:

* removes unnecessary fields
* checks for missing values
* converts exchange rates into numeric format
* calculates inverse exchange rates
* creates rate-strength categories
* adds collection date and time fields

The cleaned data is saved as:

```text
Data/Processed/cleaned_currency_rates.csv
```

### 3. Load

The loading script connects to PostgreSQL and inserts the cleaned data into:

```text
public.currency_rates
```

## Database Table

The PostgreSQL table contains the following fields:

| Column                 | Description                          |
| ---------------------- | ------------------------------------ |
| base_currency          | Base currency used for comparison    |
| target_currency        | Target currency code                 |
| exchange_rate          | Exchange rate against EUR            |
| inverse_rate           | Reciprocal of the exchange rate      |
| rate_date              | Date of the exchange rate            |
| collected_at           | Data collection timestamp            |
| collection_hour        | Hour when the data was collected     |
| rate_strength_category | Category based on the numerical rate |
| source                 | Source API name                      |

## Analysis Results

The project collected seven target currencies.

Key findings from the dataset include:

* JPY had the highest numerical exchange-rate value
* GBP had the lowest numerical exchange-rate value
* Three currencies were between 1 and 10
* Two currencies were below 1
* Two currencies were above 100
* The average numerical exchange rate was approximately 42.75

The highest numerical value should not automatically be interpreted as the strongest currency because currencies use different unit denominations.

## Power BI Dashboard

The Power BI report contains two pages.

### Page 1: Currency Overview

* Total currencies
* Highest exchange rate
* Lowest exchange rate
* Average exchange rate by currency
* Currency category distribution
* Currency slicer

### Page 2: Currency Comparison

* Exchange-rate comparison
* Inverse-rate comparison
* Detailed currency table
* Currency slicer
* Rate-strength-category slicer

## Automation

The complete ETL pipeline is executed using:

```text
run_pipeline.py
```

A Windows batch file is used to start the pipeline:

```text
run_pipeline.bat
```

Windows Task Scheduler runs the batch file automatically every day.

The automated process performs:

1. API data extraction
2. Data cleaning
3. PostgreSQL loading
4. Log-file creation

## How to Run the Project

### Install the required libraries

```bash
pip install -r requirements.txt
```

### Create the environment file

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=currency_exchange_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRESQL_PASSWORD
```

The `.env` file is excluded from GitHub for security.

### Create the PostgreSQL database

Run:

```text
sql/database_setup.sql
```

in pgAdmin.

### Run the complete pipeline

```bash
python Scripts/run_pipeline.py
```

Alternatively, run:

```text
run_pipeline.bat
```

## Security

Database passwords and environment variables are stored locally in the `.env` file.

The following files and folders are excluded through `.gitignore`:

* `.env`
* Python cache files
* Jupyter checkpoint folders
* temporary files
* local IDE settings
* unnecessary pipeline logs

## Business Value

The project demonstrates how an organisation can automate the collection and monitoring of exchange-rate information.

The dashboard can support:

* international pricing decisions
* foreign-currency monitoring
* budgeting and financial planning
* travel-cost analysis
* import and export planning
* currency-risk awareness

## Author

**Pakala Tarun Reddy**

Business Intelligence Final Project
