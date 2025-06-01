"""Контейнеры для данных магазинов"""

from pandas import DataFrame


class OzonData:
    """Контейнер для данных ОЗОН"""
    input: DataFrame
    totals: DataFrame
    sales: DataFrame

    def __init__(self, input_data: DataFrame) -> None:
        self.input = input_data


class WbData:
    """Контейнер для данных WB"""
    input: DataFrame
    output: DataFrame

    def __init__(self, input_data: DataFrame) -> None:
        self.input = input_data
