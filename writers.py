import pandas as pd
from cfg import Config

excel_file_filter = 'Excel File (*xls *.xlsx *.csv)'

def write_ozon_items(filepath: str, data: dict[str, pd.DataFrame]):
    with pd.ExcelWriter(path=filepath, engine='xlsxwriter') as writer:
        sheet_name = 'Данные'
        data['items'].to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        header_format = workbook.add_format(Config.items_headers_fmt())
        for col_num, value in enumerate(data['items'].columns.values):
            worksheet.write(0, col_num, value, header_format)

        sheet_name = 'ИТОГО'
        data['summary'].to_excel(writer, sheet_name=sheet_name, header=False)
        # workbook = writer.book
        # worksheet = writer.sheets[sheet_name]

