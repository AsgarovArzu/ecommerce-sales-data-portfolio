# E-commerce Sales Data Cleaning Pipeline

## Project Overview

This project processes a synthetic e-commerce sales dataset containing duplicate records, missing values, and inconsistent text formatting.

The Python pipeline cleans and validates the data, separates rejected records, and calculates revenue, total cost, and profit for analysis.

## Data Quality Issues

- The raw dataset contained 4 exact duplicate rows.
- The Email column contained 6 missing values.
- The Quantity column contained 5 missing values.
- The Region and Customer Name columns had inconsistent capitalization.
- Some Category and Email values contained extra whitespace.

## Data Cleaning Steps

1. Loaded the raw CSV file into a pandas DataFrame.
2. Converted the Order Date column to a datetime data type.
3. Identified and removed 4 exact duplicate rows.
4. Standardized Region, Category, Customer Name, and Email values.
5. Separated 5 records with missing Quantity values into a rejected-records dataset.
6. Converted valid Quantity values from float to integer.
7. Validated quantities, unit prices, and unit costs using business rules.
8. Calculated Revenue, Total Cost, and Profit.
9. Reconciled all input, accepted, rejected, and duplicate rows.
10. Exported and validated the clean and rejected CSV files.

## Project Structure

```text
ecommerce-sales-data-portfolio/
├── data/
│   └── raw_ecommerce_sales.csv
├── outputs/
│   ├── clean_ecommerce_sales.csv
│   └── rejected_records.csv
├── src/
│   └── clean_data.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the data-cleaning pipeline:

```bash
python src/clean_data.py
```

The generated files will be available in the `outputs/` directory:

- `clean_ecommerce_sales.csv`
- `rejected_records.csv`

## Technologies

- Python 3.9
- pandas 2.3.3
- Git and GitHub
- CSV data processing

## Key Results

- Processed 244 raw records.
- Removed 4 exact duplicate rows.
- Separated 5 rejected records with missing quantities.
- Produced 235 analysis-ready sales records.
- Standardized text and date fields.
- Added Revenue, Total Cost, and Profit calculations.
- Confirmed that all input rows were reconciled.

## Data Privacy

This project uses fully synthetic data. It does not contain real customer, company, or confidential information.