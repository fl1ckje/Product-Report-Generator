"""Функции для чтения данных"""
import numpy as np
from pandas import DataFrame

from datapacks import WbData
from .utils import check_missing_columns

_NAME = 'Название'
_PAY_JUST = 'Обоснование для оплаты'
_SALE = 'Продажа'
_LOGISTICS = 'Логистика'
_SUPPLY_ARTICLE = 'Артикул поставщика'
_SIZE = 'Размер'
_AMOUNT = 'Кол-во'
_RETAIL_PRICE = 'Цена розничная'
_SOLD_TRANSFER = 'К перечислению Продавцу за реализованный Товар'
_SERVICES_FOR_DELIVERY = 'Услуги по доставке товара покупателю'

_analysis_headers = [_NAME,
                     _PAY_JUST,
                     _SUPPLY_ARTICLE,
                     _SIZE,
                     _AMOUNT,
                     _RETAIL_PRICE,
                     _SOLD_TRANSFER,
                     _SERVICES_FOR_DELIVERY]


def analyse_data(data: WbData):
    """Формирует анализ данных WB"""
    check_missing_columns(data.input, _analysis_headers)

    data.input = data.input.replace(np.nan, 0)
    data.input = data.input[data.input[_NAME] != np.nan]
    sale_groups = data.input[data.input[_PAY_JUST] == _SALE].groupby(_NAME)
    logistics_groups = data.input[data.input[_PAY_JUST]
                                  == _LOGISTICS].groupby(_NAME)
    result = []
    for name, grp in sale_groups:
        result.append({
            'Наименование товара': grp[_NAME].iloc[0],
            'Артикул': grp[_SUPPLY_ARTICLE].iloc[0],
            _SIZE: grp[_SIZE].iloc[0],
            'Количество продаж': grp[_AMOUNT].sum(),
            'Средняя цена продажи': round(grp[_RETAIL_PRICE].mean(), 2),
            'Комиссия МП': round(grp[_RETAIL_PRICE].mean(), 2) - round(grp[_SOLD_TRANSFER].mean(), 2),
            _LOGISTICS: logistics_groups[_SERVICES_FOR_DELIVERY].sum()[
                name] / grp[_AMOUNT].sum()
        })

    data.output = DataFrame(result)
