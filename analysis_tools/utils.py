"""Вспомогательные функции для анализа данных"""

from pandas import DataFrame


def check_missing_columns(df: DataFrame, columns: list[str]):
    """Проверяет, какие столбцы отсутствуют в датафрейме"""
    missing_cols = []
    for col in columns:
        if col not in df.columns.values:
            missing_cols.append(col)
    if missing_cols:
        raise ValueError('Ошибка анализа данных: следующие столбцы отсутствуют в таблице:<br>'
                         f' {', '.join(missing_cols)}.<br>'
                         'Possible issues:<br>'
                         '1) Outdated app (update the app or leave a bug report)<br>'
                         '2) Check your data file for suitable columns by name')
