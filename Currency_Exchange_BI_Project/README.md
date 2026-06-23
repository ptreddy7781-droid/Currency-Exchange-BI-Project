# Currency Exchange Business Intelligence Dashboard

## Project Overview

This project develops an automated Business Intelligence pipeline for collecting, cleaning, storing, analysing, and visualising currency exchange-rate data.

The pipeline extracts exchange rates using a public currency exchange API, processes the data using Python and Pandas, stores the cleaned records in PostgreSQL, performs SQL and Jupyter Notebook analysis, and presents the results through an interactive Power BI dashboard.

The project was completed by **Pakala Tarun Reddy**.

---

## Business Problem

Currency exchange rates differ significantly across international currencies and can be difficult to compare without a structured reporting system.

The objective of this project is to create an automated solution that:

- collects current currency exchange-rate data;
- cleans and transforms the extracted data;
- stores the information in a relational database;
- provides SQL and Python-based analysis;
- displays exchange-rate comparisons in an interactive dashboard;
- runs automatically using Windows Task Scheduler.

---

## Project Objectives

The main objectives are:

1. Extract exchange-rate data from a public API.
2. Store raw data in JSON and CSV formats.
3. Clean and transform the data using Pandas.
4. Load the processed data into PostgreSQL.
5. Analyse the data using SQL and Jupyter Notebook.
6. Build an interactive Power BI dashboard.
7. Automate the complete ETL pipeline.
8. Document and publish the project on GitHub.

---

## Data Source

The project uses a public currency exchange API to collect exchange rates using EUR as the base currency.

### Base Currency

```text
EUR
