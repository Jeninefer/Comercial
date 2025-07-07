import pandas as pd


def clean_monetary(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Remove currency symbols and cast to numeric."""
    if column in df.columns:
        df[column] = (
            df[column].astype(str)
            .str.replace('#VALUE!', '', regex=False)
            .str.replace(r'[\$,()]', '', regex=True)
        )
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


def clean_percentage(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column in df.columns:
        df[column] = (
            df[column].astype(str)
            .str.replace('%', '', regex=False)
        )
        df[column] = pd.to_numeric(df[column], errors='coerce') / 100
    return df


def convert_date(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column].astype(str).str.replace('#VALUE!', '', regex=False),
            errors='coerce'
        )
    return df

