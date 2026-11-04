from pathlib import Path

import pandas as pd

def get_data(xlsx_raw_data_path: Path) -> pd.DataFrame:
    df_users = pd.read_excel(xlsx_raw_data_path, sheet_name="Пользователи") # type: ignore
    df_payments = pd.read_excel(xlsx_raw_data_path, sheet_name="Платежи") # type: ignore

    df = df_payments.merge(df_users, how='inner', on=['user_id', 'group'], validate='m:1')
    df["age"] = df["age"].where(df["age"].between(0, 100), df.loc[df["age"].between(0, 100), "age"].median())

    assert df.payment_id.isna().sum() == 0, f'Присутствуют None в платежах: {df.payment_id.isna().sum()} шт.'
    assert df.user_id.isna().sum() == 0, f'Присутствуют None в пользователях: {df.user_id.isna().sum()} шт.'
    assert df.group.isna().sum() == 0, f'Присутствуют None в группах: {df.group.isna().sum()} шт.'
    assert df["age"].between(0, 100).all()

    return df