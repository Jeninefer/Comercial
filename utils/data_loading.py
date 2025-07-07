import pandas as pd
from typing import Optional


def load_google_sheet(sheet_id: str, gid: str = "0") -> pd.DataFrame:
    """Load a Google Sheet as a DataFrame via CSV export."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        return pd.read_csv(url)
    except Exception as exc:
        raise RuntimeError(f"Failed to load Google Sheet: {exc}")


