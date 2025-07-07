import pandas as pd


def calculate_total_paid(df: pd.DataFrame) -> pd.DataFrame:
    if 'customer_id' not in df.columns or 'true_total_payment' not in df.columns:
        raise KeyError('customer_id and true_total_payment columns required')
    temp = df[['customer_id', 'true_total_payment']].copy()
    temp['true_total_payment'] = pd.to_numeric(temp['true_total_payment'], errors='coerce')
    result = temp.groupby('customer_id', dropna=False)['true_total_payment'].sum().reset_index()
    result.rename(columns={'true_total_payment': 'total_amount_paid'}, inplace=True)
    return result


def calculate_total_disbursed(df: pd.DataFrame) -> pd.DataFrame:
    if 'customer_id' not in df.columns or 'disbursement_amount' not in df.columns:
        raise KeyError('customer_id and disbursement_amount columns required')
    temp = df[['customer_id', 'disbursement_amount']].copy()
    temp['disbursement_amount'] = pd.to_numeric(temp['disbursement_amount'], errors='coerce')
    result = temp.groupby('customer_id', dropna=False)['disbursement_amount'].sum().reset_index()
    result.rename(columns={'disbursement_amount': 'total_amount_disbursed'}, inplace=True)
    return result


def calculate_repayment_rate(total_paid: pd.DataFrame, total_disbursed: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(total_paid, total_disbursed, on='customer_id', how='left')
    df['repayment_rate'] = df['total_amount_paid'] / df['total_amount_disbursed'].replace(0, pd.NA)
    return df


def customers_below_threshold(repayment_df: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    """Return customers with repayment rate below the given threshold."""
    if 'repayment_rate' not in repayment_df.columns:
        raise KeyError('repayment_rate column required')
    return repayment_df[repayment_df['repayment_rate'] < threshold]


def loans_per_prefix(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the count of unique loans per prefix of loan_id."""
    if 'loan_id' not in df.columns:
        raise KeyError('loan_id column required')
    temp = df['loan_id'].astype(str).str.split('-', n=1).str[0]
    result = temp.value_counts().reset_index()
    result.columns = ['loan_prefix', 'loan_count']
    result['avg_loans_per_prefix'] = result['loan_count'].mean()
    return result

