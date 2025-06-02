"""Функции для чтения данных"""
from enum import Enum

import numpy as np
from pandas import DataFrame

from datapacks import WbData
from .utils import check_missing_columns


class Headers(Enum):
    NUMBER = '№'
    DELIVERY_NUMBER = 'Номер поставки'
    NAME = 'Название'
    PAY_JUST = 'Обоснование для оплаты'
    SUPPLY_ARTICLE = 'Артикул поставщика'
    SIZE = 'Размер'
    AMOUNT = 'Кол-во'
    RETAIL_PRICE = 'Цена розничная'
    SOLD_TRANSFER = 'К перечислению Продавцу за реализованный Товар'
    SERVICES_FOR_DELIVERY = 'Услуги по доставке товара покупателю'

    @staticmethod
    def list():
        return list(map(lambda h: h.value, Headers))


_SALE = 'Продажа'
_PRODUCT_NAME = 'Наименование товара'
_ARTICLE = 'Артикул'
_SIZE = 'Размер'
_SALES_AMOUNT = 'Количество продаж'
_AVG_SALE_PRICE = 'Средняя цена продажи'
_MP_COMMISSION = 'Комиссия МП'
_LOGISTICS = 'Логистика'


def analyse_data(data: WbData):
    """Формирует анализ данных WB"""
    check_missing_columns(data.input, Headers.list())
    data.input = data.input.replace(np.nan, '')

    sale_groups = data.input[data.input[Headers.PAY_JUST.value]
                             == _SALE].groupby(Headers.NAME.value)
    logistics_groups = data.input[data.input[Headers.PAY_JUST.value]
                                  == _LOGISTICS].groupby(Headers.NAME.value)
    totals = []
    for name, grp in sale_groups:
        totals.append({
            _PRODUCT_NAME:
                grp[Headers.NAME.value].iloc[0],
            _ARTICLE:
                grp[Headers.SUPPLY_ARTICLE.value].iloc[0],
            _SIZE:
                grp[Headers.SIZE.value].iloc[0],
            _SALES_AMOUNT:
                grp[Headers.AMOUNT.value].sum(),
            _AVG_SALE_PRICE:
                round(grp[Headers.RETAIL_PRICE.value].mean(), 2),
            _MP_COMMISSION:
                round(grp[Headers.RETAIL_PRICE.value].mean(), 2) -
                round(grp[Headers.SOLD_TRANSFER.value].mean(), 2),
            _LOGISTICS:
                logistics_groups[Headers.SERVICES_FOR_DELIVERY.value].sum()[name] /
                grp[Headers.AMOUNT.value].sum()
        })

    data.output = DataFrame(totals)
