"""Функции для чтения данных"""
import tempfile
import zipfile
import pandas as pd
from pathlib import Path
from typing import List

from pandas import DataFrame, read_excel


def read_excel_data(path: str) -> DataFrame | None:
    """Читает данные из excel файла в датафрейм"""
    return read_excel(path, engine='calamine')


def extract_zip_to_temp(path: str) -> Path:
    """Извлекает содержимое zip архивов во временные директории"""
    temp_dir = tempfile.mkdtemp(prefix='xlsx_data')
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return Path(temp_dir)


def read_ozon_data(path: str) -> DataFrame | None:
    """Читает данные из excel файла маркетплейса ozon в датафрейм"""
    return read_excel_data(path)


def read_wb_data(paths: List[str]) -> DataFrame | None:
    """
    Распаковывает zip архивы с excel файлами маркетплейса
    wb и читает из них данные в один датафрейм
    """
    dfs = []
    for path in paths:
        temp_dir = extract_zip_to_temp(path)
        xlsx_files = list(temp_dir.glob('*.xlsx'))
        try:
            if not xlsx_files:
                raise ValueError(f'XLSX файлы не найдены в {temp_dir}')
            if len(xlsx_files) > 1:
                raise ValueError(
                    f'Несколько XLSX файлов найдено в {temp_dir}, ожидается только один')
            df = read_excel_data(xlsx_files[0])
            dfs.append(df)
        finally:
            from shutil import rmtree
            rmtree(str(temp_dir))
    return pd.concat(dfs, ignore_index=True)
