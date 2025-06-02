"""Логика записи данных WB"""

from pandas import ExcelWriter

from misc.colors import GREY
from datapacks import WbData


def save_data(filepath: str, data: WbData):
    """Сохраняет входные и выходные таблицы в excel файл"""
    with ExcelWriter(path=filepath, engine='xlsxwriter') as writer:
        workbook = writer.book

        def save_input_data(sheet_name):
            data.input.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]

            header_format = workbook.add_format({
                'text_wrap': True,
                'bold': True,
                'align': 'left'
            })
            for col_num, value in enumerate(data.input.columns.values):
                worksheet.write(0, col_num, value, header_format)

        def save_analysis_data(sheet_name):
            data.output.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]

            header_format = workbook.add_format({
                'text_wrap': True,
                'bold': True,
                'align': 'left',
                'bg_color': GREY
            })
            for col_num, value in enumerate(data.output.columns.values):
                worksheet.write(0, col_num, value, header_format)

            worksheet.autofit()

        save_analysis_data('Обработанные данные')
        save_input_data('Исходник')
