"""Логика записи данных ОЗОН"""

from pandas import ExcelWriter

from misc.formats import DATE_FORMAT, CURRENCY_FORMAT, PERCENTAGE_FORMAT
from datapacks import OzonData
from analysis_tools.ozon import FEE_PERCENTAGE, FEE_RATE, FEE_RUB, LAST_MILE_RUB, LOGISTICS_RUB, MID_SELL_PRICE, LOC_IDX, TOTAL


def save_data(filepath: str, data: OzonData):
    """Сохраняет входные и выходные таблицы в excel файл"""
    with ExcelWriter(path=filepath, engine='xlsxwriter',
                     date_format=DATE_FORMAT, datetime_format=DATE_FORMAT) as writer:
        workbook = writer.book

        def save_input_data(sheet_name):
            data.input.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]

            # header formatting
            header_format = workbook.add_format({
                'text_wrap': True,
                'bold': True,
                'align': 'left'
            })
            for col_num, value in enumerate(data.input.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # fee rate column formatting
            percentage_format = workbook.add_format(
                {'num_format': PERCENTAGE_FORMAT})
            fee_rate_col = data.input.columns.get_loc(FEE_RATE)
            worksheet.set_column(fee_rate_col, fee_rate_col,
                                 None, percentage_format)

            worksheet.autofit()

        def save_analysis_data(sheet_name):
            data.totals.to_excel(writer, sheet_name=sheet_name, index=False)

            sales_start_row = len(data.totals)+2
            data.sales.to_excel(writer, sheet_name=sheet_name, index=False,
                                startrow=sales_start_row)
            worksheet = writer.sheets[sheet_name]

            # totals header formatting
            period_format = workbook.add_format(
                {'bold': True, 'align': 'left'})
            worksheet.write(0, 0, data.totals.columns[0], period_format)

            align_left_format = workbook.add_format({'align': 'left'})
            worksheet.write(0, 1, data.totals.columns[1], align_left_format)

            # totals values formatting
            currency_format = workbook.add_format(
                {'num_format': CURRENCY_FORMAT})
            write_column(
                worksheet, data.totals.iloc[:, 1], 1, 1, currency_format)

            # sales header formatting
            sales_header_format = workbook.add_format(
                {'bold': True, 'align': 'left', 'bg_color': '#D9D9D9'})
            for col_num, value in enumerate(data.sales.columns.values):
                worksheet.write(sales_start_row, col_num,
                                value, sales_header_format)

            # fee percentage formatting
            start_row = sales_start_row+1
            fee_percentage_col = data.sales.columns.get_loc(FEE_PERCENTAGE)
            write_column(worksheet, data.sales[FEE_PERCENTAGE],
                         start_row, fee_percentage_col, currency_format)

            # mid sell price formatting
            mid_price_col = data.sales.columns.get_loc(MID_SELL_PRICE)
            write_column(worksheet, data.sales[MID_SELL_PRICE],
                         start_row, mid_price_col, currency_format)

            # fee rub formatting
            fee_rub_col = data.sales.columns.get_loc(FEE_RUB)
            write_column(worksheet, data.sales[FEE_RUB],
                         start_row, fee_rub_col, currency_format)

            # last mile rub formatting
            last_mile_rub_col = data.sales.columns.get_loc(LAST_MILE_RUB)
            write_column(worksheet, data.sales[LAST_MILE_RUB],
                         start_row, last_mile_rub_col, currency_format)

            # logistics rub formatting
            logistics_rub_col = data.sales.columns.get_loc(LOGISTICS_RUB)
            write_column(worksheet, data.sales[LOGISTICS_RUB],
                         start_row, logistics_rub_col, currency_format)

            # loc idx formatting
            loc_idx_col = data.sales.columns.get_loc(LOC_IDX)
            write_column(worksheet, data.sales[LOC_IDX],
                         start_row, loc_idx_col, currency_format)

            # total formatting
            total_col = data.sales.columns.get_loc(TOTAL)
            write_column(worksheet, data.sales[TOTAL],
                         start_row, total_col, currency_format)

            worksheet.autofit()

        save_input_data('Начисления')
        save_analysis_data('ИТОГО')


def write_column(worksheet, values, start_row, start_col, fmt):
    """Записывает колонку ячеек с заданным форматом"""
    for i, val in enumerate(values):
        worksheet.write(start_row+i, start_col, val, fmt)
