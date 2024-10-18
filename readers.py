import pandas as pd


def read_excel_data(filepath: str):
    df = pd.read_excel(filepath)
    return df.fillna('')
