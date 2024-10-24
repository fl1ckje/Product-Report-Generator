"""Контейнеры для данных ОЗОН"""

from pandas import DataFrame
# pylint: disable=too-few-public-methods


class OzonData:
    """Контейнер для данных ОЗОН"""
    input: DataFrame
    totals: DataFrame
    sales: DataFrame

    def __init__(self, input_data: DataFrame) -> None:
        self.input = input_data
