"""Функционал анализа данных ОЗОН"""
from enum import Enum

import numpy as np
from pandas import DataFrame

from datapacks import OzonData
from .utils import check_missing_columns


class Headers(Enum):
    ACCRUAL_DATE = 'Дата начисления'
    ACCRUAL_TYPE = 'Тип начисления'
    ARTICLE = 'Артикул'
    FOR_SALE_BEFORE_FEES = 'За продажу или возврат до вычета комиссий и услуг'
    FEE_RATE = 'Ставка комиссии'
    FEE_PER_SALE = 'Комиссия за продажу'
    LAST_MILE = ('Последняя миля (разбивается по товарам пропорционально '
                 'доле цены товара в сумме отправления)')
    LOGISTICS = 'Логистика'
    LOC_IDX = 'Индекс локализации'
    TOTAL = 'Итого'

    @staticmethod
    def list()-> list[str]:
        return list(map(lambda h: h.value, Headers))


_ARTICLE = 'Артикул'
_SALES_AMOUNT = 'Кол-во продаж'
MID_SELL_PRICE = 'Ср. цена продажи'
FEE_PERCENTAGE = 'Комиссия, %'
FEE_RATE = 'Ставка комиссии'
FEE_RUB = 'Комиссия, руб'
LAST_MILE_RUB = 'Последняя миля, руб'
LOGISTICS_RUB = 'Логистика, руб'
LOC_IDX = 'Индекс локализации'
TOTAL = 'Итого'


def analyse_data(data: OzonData) -> None:
    """Формирует анализ данных ОЗОН"""
    check_missing_columns(data.input, Headers.list())

    data.input[Headers.LOC_IDX.value] = \
        data.input[Headers.LOC_IDX.value].replace(np.nan, 0)

    data.totals = data.input.groupby(
        Headers.ACCRUAL_TYPE.value)[Headers.TOTAL.value].sum().abs().reset_index()
    min_date = data.input[Headers.ACCRUAL_DATE.value].dt.date.min()
    max_date = data.input[Headers.ACCRUAL_DATE.value].dt.date.max()
    data.totals.columns = ['Период',
                           f'{min_date.strftime('%d.%m.%Y')}'
                           f' - {max_date.strftime('%d.%m.%Y')}']

    sales_groups = data.input[
        data.input[Headers.ACCRUAL_TYPE.value] == 'Доставка покупателю'].groupby(Headers.ARTICLE.value)
    sales = []
    for _, grp in sales_groups:
        sales.append({
            _ARTICLE:
                grp[Headers.ARTICLE.value].iloc[0],
            _SALES_AMOUNT:
                len(grp),
            MID_SELL_PRICE:
                round(grp[Headers.FOR_SALE_BEFORE_FEES.value].mean(), 2),
            FEE_PERCENTAGE:
                round(grp[Headers.FEE_RATE.value].mean() * 100, 2),
            FEE_RUB:
                abs(round(grp[Headers.FEE_PER_SALE.value].mean(), 2)),
            LAST_MILE_RUB:
                abs(round(grp[Headers.LAST_MILE.value].mean(), 2)),
            LOGISTICS_RUB:
                abs(round(grp[Headers.LOGISTICS.value].mean(), 2)),
            LOC_IDX:
                int(grp[Headers.LOC_IDX.value].mean()),
            TOTAL:
                round(grp[Headers.TOTAL.value].mean(), 2),
        })
    data.sales = DataFrame(sales)
