import pandas as pd
from dateutil import parser

from cfg import Config


def analyse_ozon_data(df: pd.DataFrame):
    missing_headers = []
    for header in Config.items_headers().keys():
        if header not in df.columns.values:
            missing_headers.append(header)
    if missing_headers:
        raise Exception('Analysis data error: The following headers are not in data file:<br>'
                        f' {", ".join(missing_headers)}.<br>'
                        'Possible issues:<br>'
                        '1) Outdated app (update the app or leave a bug report)<br>'
                        '2) Check your data file for suitable columns by name')
    df['Дата начисления'] = df['Дата начисления'].dt.strftime('%d.%m.%Y')
    period = f'{df['Дата начисления'].min()} - {df['Дата начисления'].max()}'
    article = df['Артикул'][0]

    sales_df = df[(df['Тип начисления'] == 'Доставка покупателю')]
    sales_count = len(sales_df)
    avg_sell_price = round(float(sales_df['За продажу или возврат до вычета комиссий и услуг'].mean()), 2)
    fee_percent = round(float(sales_df['Ставка комиссии'].mean()), 2) * 100
    fee_amount = abs(round(float(sales_df['Комиссия за продажу'].mean()), 2))
    last_mile = abs(round(float(sales_df[(
        'Последняя миля (разбивается по товарам пропорционально '
        'доле цены товара в сумме ' 'отправления)')].mean()), 2))
    logistics = abs(round(float(sales_df['Логистика'].mean()), 2))
    loc_idx = int(sales_df['Индекс локализации'].mean())
    total = round(float(sales_df['Итого'].mean()), 2)

    ad_df = df[(df['Тип начисления'] == 'Трафареты')]
    ad = abs(round(float(ad_df['Итого'].sum()), 2))

    summary_df = pd.DataFrame([{
        'Период': period,
        'Артикул': article,
        'Кол-во продаж': sales_count,
        'Средняя цена продажи': avg_sell_price,
        'Комиссия, %': fee_percent,
        'Комиссия, руб': fee_amount,
        'Последняя миля, руб': last_mile,
        'Логистика, руб': logistics,
        'Индекс локализации': loc_idx,
        'ИТОГО': total,
        'Реклама': ad
    }]).T

    return {
        'items': df,
        'summary': summary_df
    }
