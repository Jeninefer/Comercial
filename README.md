# Comercial

This repository provides a small pipeline to merge loan and payment data from CSV files and an auxiliary Google Sheet.

## Setup

1. Place the required CSV files in the repository root:
   - `Loan Data (2).csv`
   - `Payment Schedule (2).csv`
   - `Historical Real Payment (2).csv`
   - `Customer Data (2).csv`
   - `Untitled (4).csv`
2. Ensure Python 3 is available.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the pipeline:

```bash
python merge_pipeline.py --output merged.csv
```

You can override the default CSV file names using command-line arguments, e.g. `--loan_data my_loans.csv`.

The script loads the CSVs and the *Aux* sheet from Google Sheets, cleans the data and merges them into `merged.csv`.

## Utilities

- `utils/data_loading.py` – helper to load Google Sheets via CSV export.
- `utils/cleaning.py` – common cleaning functions for monetary, percentage and date columns.
- `analysis/metrics.py` – utilities to compute totals, repayment rates, and identify low-performing customers.

You can import these modules in notebooks for further analysis.

