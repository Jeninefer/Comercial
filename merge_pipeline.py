"""Merge loan-related CSV files with an auxiliary Google Sheet."""

import argparse
from pathlib import Path

try:
    import pandas as pd
except ModuleNotFoundError as exc:  # pragma: no cover - dependency missing
    raise SystemExit(
        "pandas is required to run this script. Install dependencies with 'pip install -r requirements.txt'."
    ) from exc

from utils.data_loading import load_google_sheet
from utils.cleaning import clean_monetary, clean_percentage, convert_date


CSV_FILES = {
    "loan_data": "Loan Data (2).csv",
    "payment_schedule": "Payment Schedule (2).csv",
    "historical_payment": "Historical Real Payment (2).csv",
    "customer_data": "Customer Data (2).csv",
    "collateral": "Untitled (4).csv",
}

AUX_SHEET_ID = "15FkuqNP-egeLAcMlkp33BpizsOv8hRAJD7m-EXJma-8"


def load_csvs(paths: dict) -> dict:
    """Load all CSV files defined in paths.

    Parameters
    ----------
    paths: dict
        Mapping from logical name to file path.
    """
    data: dict = {}
    for key, filename in paths.items():
        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {filename}")
        data[key] = pd.read_csv(path)
    return data


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df


def apply_basic_cleaning(df: pd.DataFrame, monetary_cols=None, percentage_cols=None, date_cols=None) -> pd.DataFrame:
    monetary_cols = monetary_cols or []
    percentage_cols = percentage_cols or []
    date_cols = date_cols or []
    for col in monetary_cols:
        df = clean_monetary(df, col)
    for col in percentage_cols:
        df = clean_percentage(df, col)
    for col in date_cols:
        df = convert_date(df, col)
    return df


def merge_dataframes(dfs: dict, aux_df: pd.DataFrame) -> pd.DataFrame:
    dfs = {k: v for k, v in dfs.items() if not v.empty}
    if not dfs:
        return pd.DataFrame()
    base_key = 'loan_data' if 'loan_data' in dfs else next(iter(dfs))
    merged = dfs.pop(base_key).copy()
    merged = standardize_columns(merged)
    for name, df in dfs.items():
        df = standardize_columns(df)
        keys = [c for c in ['company', 'loan_id', 'customer_id'] if c in merged.columns and c in df.columns]
        if not keys:
            keys = list(set(merged.columns) & set(df.columns))
        conflicts = [c for c in df.columns if c in merged.columns and c not in keys]
        df = df.rename(columns={c: f'{c}_{name}' for c in conflicts})
        merged = pd.merge(merged, df, on=keys, how='outer')
    if not aux_df.empty:
        aux_df = standardize_columns(aux_df)
        keys = [c for c in ['company', 'loan_id'] if c in merged.columns and c in aux_df.columns]
        merged = pd.merge(merged, aux_df, on=keys, how='left')
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge loan CSVs with Aux sheet")
    parser.add_argument(
        "--output",
        default="merged.csv",
        help="Path for the merged CSV output",
    )
    for key, filename in CSV_FILES.items():
        parser.add_argument(f"--{key}", default=filename, help=f"Path to {filename}")
    args = parser.parse_args()

    csv_paths = {k: getattr(args, k) for k in CSV_FILES}
    dfs = load_csvs(csv_paths)
    aux_df = load_google_sheet(AUX_SHEET_ID, gid="0")
    merged = merge_dataframes(dfs, aux_df)
    merged.to_csv(args.output, index=False)
    print(f"Merged data saved to {args.output}")


if __name__ == "__main__":
    main()

