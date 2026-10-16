# Financial Transactions & Fraud Trends Analysis

## Project Overview

This project analyzes financial transaction patterns using SQL, Python, and an interactive Streamlit dashboard. It explores transaction behaviour, fraud-labelled activity, transaction amounts, and the relationship between high-value transactions and fraud labels in a synthetic financial dataset.

## Business Objective

To identify transaction patterns associated with fraud-labelled activity and evaluate how effectively the dataset's system flag corresponds to the fraud labels.

## Technology Stack

- **SQL (MySQL):** Data querying, aggregation, transaction segmentation, and fraud-rate analysis
- **Python:** Data analysis and reporting
- **Pandas:** Data manipulation and analysis
- **Plotly:** Interactive visualizations
- **Streamlit:** Interactive dashboard
- **MySQL Connector:** Database connectivity

## Key Analysis Areas

- Transaction volume and distribution
- Fraud-labelled versus non-fraud-labelled transactions
- Average transaction amount comparisons
- Fraud rates across transaction types
- Sender and receiver balance patterns
- High-value versus other transactions
- Comparison of `isFraud` and `isFlaggedFraud`

## Dataset

The project uses the PaySim synthetic financial transaction dataset.

The dataset includes transaction type, amount, sender and receiver balances, fraud labels, and system-flag information.

The original dataset is not included in this repository because of its large file size.

## Key Findings

- The dataset contains 6,362,620 transactions.
- There are 8,213 fraud-labelled transactions, approximately 0.1291% of the dataset.
- Fraud-labelled transactions have a higher average transaction amount than non-fraud-labelled transactions.
- Transactions with amounts of at least 1,000,000 show a higher fraud-labelled rate than lower-value transactions in this dataset.
- The dataset's `isFraud` label and `isFlaggedFraud` system flag represent different concepts and should be evaluated separately.

These findings describe patterns in a synthetic dataset and should not be interpreted as proof of real-world financial fraud.

## Project Structure

- `sql queries.sql` — SQL analysis queries
- `python_analysis/fraud_analysis.py` — Python analysis and chart generation
- `python_analysis/dashboard.py` — Streamlit dashboard
- `python_analysis/test_connection.py` — Database connection test
- `python_analysis/requirements.txt` — Python dependencies
- `python_analysis/charts/` — Generated charts

## Running the Dashboard

1. Install Python and MySQL.
2. Install the required Python packages:

   `python -m pip install -r python_analysis/requirements.txt`

3. Create and populate the MySQL database using the dataset and SQL setup.
4. Configure the database connection using your own local credentials.
5. From the project root, run:

   `python -m streamlit run python_analysis/dashboard.py`

6. Open `http://localhost:8501` in your browser.

## Limitations

- PaySim is a synthetic dataset, not a record of actual bank transactions.
- Observed associations do not establish causation.
- The results depend on the dataset's generated patterns and labels.

## Future Improvements

- Add automated data-quality checks
- Improve transaction-type and time-based analysis
- Add dashboard filters and exportable summaries
- Deploy a publicly accessible dashboard using a secure data source

## Author

Vani Sharma