"""Функции для чтения данных"""

from pandas import DataFrame, read_excel
from misc.formats import DATE_FORMAT


def read_excel_data(filepath: str) -> DataFrame | None:
    """Читает данные из excel файла в датафрейм"""
    return read_excel(filepath, engine='calamine', date_format=DATE_FORMAT)
