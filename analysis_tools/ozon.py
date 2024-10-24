"""Функционал анализа данных ОЗОН"""

import numpy as np
import pandas as pd

from data_packs.ozon import OzonData
from .utils import check_missing_columns

_ACCRUAL_DATE = 'Дата начисления'
_ACCRUAL_TYPE = 'Тип начисления'
_ARTICLE = 'Артикул'
_FOR_SALE_BEFORE_FEES = 'За продажу или возврат до вычета комиссий и услуг'
FEE_RATE = 'Ставка комиссии'
_FEE_PER_SALE = 'Комиссия за продажу'
_LAST_MILE = ('Последняя миля (разбивается по товарам пропорционально '
              'доле цены товара в сумме отправления)')
_LOGISTICS = 'Логистика'
LOC_IDX = 'Индекс локализации'
TOTAL = 'Итого'

MID_SELL_PRICE = 'Ср. цена продажи'
FEE_RUB = 'Комиссия, руб'
LAST_MILE_RUB = 'Последняя миля, руб'
LOGISTICS_RUB = 'Логистика, руб'
FEE_PERCENTAGE = 'Комиссия, %'

_analysis_headers = [_ACCRUAL_DATE,
                     _ACCRUAL_TYPE,
                     _ARTICLE,
                     _FOR_SALE_BEFORE_FEES,
                     FEE_RATE,
                     _FEE_PER_SALE,
                     _LAST_MILE,
                     _LOGISTICS,
                     LOC_IDX,
                     TOTAL]


def analyse_data(data: OzonData):
    """Формирует анализ данных ОЗОН"""
    check_missing_columns(data.input, _analysis_headers)

    data.input[LOC_IDX] = data.input[LOC_IDX].replace(np.nan, 0)

    data.totals = data.input.groupby('Тип начисления')[
        'Итого'].sum().abs().reset_index()
    min_date = data.input['Дата начисления'].dt.date.min()
    max_date = data.input['Дата начисления'].dt.date.max()
    data.totals.columns = ['Период',
                           f'{min_date.strftime('%d.%m.%Y')}'
                           f' - {max_date.strftime('%d.%m.%Y')}']

    grouped_sales = data.input[data.input[_ACCRUAL_TYPE]
                               == 'Доставка покупателю'].groupby(_ARTICLE)
    sales = []
    for _, grp in grouped_sales:
        sales.append({
            'Артикул': grp[_ARTICLE].iloc[0],
            'Кол-во продаж': len(grp),
            MID_SELL_PRICE: round(grp[_FOR_SALE_BEFORE_FEES].mean(), 2),
            FEE_PERCENTAGE: round(grp[FEE_RATE].mean() * 100, 2),
            FEE_RUB: abs(round(grp[_FEE_PER_SALE].mean(), 2)),
            LAST_MILE_RUB: abs(round(grp[_LAST_MILE].mean(), 2)),
            LOGISTICS_RUB: abs(round(grp[_LOGISTICS].mean(), 2)),
            LOC_IDX: int(grp[LOC_IDX].mean()),
            TOTAL: round(grp[TOTAL].mean(), 2),
        })
    data.sales = pd.DataFrame(sales)
