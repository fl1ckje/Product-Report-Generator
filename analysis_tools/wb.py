"""Функции для чтения данных"""
from enum import Enum

import numpy as np
from pandas import DataFrame

from datapacks import WbData
from .utils import check_missing_columns


class Headers(Enum):
    NUMBER = '№'
    DELIVERY_NUMBER = 'Номер поставки'
    ITEM = 'Предмет'
    ITEM_CODE = 'Код номенклатуры'
    BRAND = 'Бренд'
    SUPPLY_ARTICLE = 'Артикул поставщика'
    NAME = 'Название'
    SIZE = 'Размер'
    BARCODE = 'Баркод'
    DOC_TYPE = 'Тип документа'
    PAY_JUST = 'Обоснование для оплаты'
    ORDER_DATE = 'Дата заказа покупателем'
    SALE_DATE = 'Дата продажи'
    AMOUNT = 'Кол-во'
    RETAIL_PRICE = 'Цена розничная'
    SOLD_THE_PROD_PR = 'Вайлдберриз реализовал Товар (Пр)'
    PRODUCT_DISCOUNT = 'Согласованный продуктовый дисконт, %'
    PROMO_CODE = 'Промокод %'
    FINAL_DISCOUNT = 'Итоговая согласованная скидка, %'
    RETAIL_PRICE_INC_DISCOUNT = 'Цена розничная с учетом согласованной скидки'
    RATEING_CV_DECREASE = 'Размер снижения кВВ из-за рейтинга, %'
    ACTION_CV_DECREASE = 'Размер снижения кВВ из-за акции, %'
    REGULAR_CUSTOMER_DISCOUNT = 'Скидка постоянного Покупателя (СПП), %'
    KBB_SIZE = 'Размер кВВ, %'
    KBB_SIZE_WOUT_VAT = 'Размер  кВВ без НДС, % Базовый'
    REWARD_FROM_SALES = 'Вознаграждение с продаж до вычета услуг поверенного, без НДС'
    REFUND_FOR_DELIVERY_AND_RETURN = 'Возмещение за выдачу и возврат товаров на ПВЗ'
    ARRANGING_PAYS_FEES = 'Эквайринг/Комиссии за организацию платежей'
    AMOUNT_OF_ARRANGING_PAYS_FEES = 'Размер комиссии за эквайринг/Комиссии за организацию платежей, %'
    TYPE_OF_ARRANGING_PAYS_FEES = 'Тип платежа за Эквайринг/Комиссии за организацию платежей'
    WB_REWARD = 'Вознаграждение Вайлдберриз (ВВ), без НДС'
    VAT_ON_WB_REWARD = 'НДС с Вознаграждения Вайлдберриз'
    SOLD_TRANSFER = 'К перечислению Продавцу за реализованный Товар'
    DELIVERIES_AMOUNT = 'Количество доставок'
    REFUNDS_AMOUNT = 'Количество возврата'
    SERVICES_FOR_DELIVERY = 'Услуги по доставке товара покупателю'
    COMMIT_START_DATE = 'Дата начала действия фиксации'
    COMMIT_END_DATE = 'Дата конца действия фиксации'
    PAID_DELIVERY_SERVICE_SIGN = 'Признак услуги платной доставки'
    TOTAL_FINES_AMOUNT = 'Общая сумма штрафов'
    SURCHARGES = 'Доплаты'
    LOGISTICS_FINES_SURCHARGES_TYPES = 'Виды логистики, штрафов и доплат'
    MP_STICKER = 'Стикер МП'
    ACQUIRING_BANK_NAME = 'Наименование банка-эквайера'
    OFFICE_NUMBER = 'Номер офиса'
    DELIVERY_OFFICE_NAME = 'Наименование офиса доставки'
    PARTNERS_INN = 'ИНН партнера'
    PARTNER = 'Партнер'
    WAREHOUSE = 'Склад'
    COUNTRY = 'Страна'
    BOXES_TYPE = 'Тип коробов'
    CUSTOMS_DECL_NUMB = 'Номер таможенной декларации'
    ASMB_TASK_NUMB = 'Номер сборочного задания'
    MARKING_CODE = 'Код маркировки'
    SHK = 'ШК'
    SRID = 'Srid'
    TRANSPORT_STORAGE_REFUND = 'Возмещение издержек по перевозке/по складским операциям с товаром'
    TRANSPORT_ORGANIZER = 'Организатор перевозки'
    STORING = 'Хранение'
    DEDUCTIONS = 'Удержания'
    PAID_ACCEPTANCE = 'Платная приемка'
    FIXED_WH_SUPL_RATIO = 'Фиксированный коэффициент склада по поставке'
    LEGAL_ENTITY_SALE_SIGN = 'Признак продажи юридическому лицу'
    PAID_ACCEPTANCE_BOX_NUMB = 'Номер короба для платной приемки'

    @staticmethod
    def list() -> list[str]:
        return list(map(lambda h: h.value, Headers))


_SALE = 'Продажа'
_PRODUCT_NAME = 'Наименование товара'
_ARTICLE = 'Артикул'
_SIZE = 'Размер'
_SALES_AMOUNT = 'Количество продаж'
_AVG_SALE_PRICE = 'Средняя цена продажи'
_MP_COMMISSION = 'Комиссия МП'
_LOGISTICS = 'Логистика'


def analyse_data(data: WbData) -> None:
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
