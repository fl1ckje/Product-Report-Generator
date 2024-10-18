from os import getcwd
from os.path import dirname
from pathlib import Path
from sys import exception

import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, \
    QMessageBox
from PySide6.QtCore import Qt

from analysis_tools import analyse_ozon_data
from cfg import Config
from enums import Marketplace
from readers import read_excel_data
from writers import write_ozon_items, excel_file_filter


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cwd = getcwd()
        self.save_filepath = self.cwd

        self.setWindowTitle(f'Marketplace product report generator for {Config.marketplace().name}')
        self.setFixedSize(640, 0)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.input_file_browser = FilepathBrowser('Input data filepath:',
                                                  'Select marketplace data file', self.cwd)
        layout.addWidget(self.input_file_browser)

        generate_report_button = QPushButton("Generate report")
        generate_report_button.clicked.connect(self.generate_report)
        layout.addWidget(generate_report_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # self.saveDialog = QFileDialog(self)
        # self.saveDialog.setFileMode(QFileDialog.FileMode.AnyFile)

        self.show()

    def generate_report(self):
        try:
            df = read_excel_data(self.input_file_browser.filepath)
            print(df.head(1))
            if Config.marketplace() == Marketplace.OZON:
                data = analyse_ozon_data(df)
                self.get_save_filepath(data)
            # elif Config.marketplace() == Marketplace.WB:
        except (ValueError, KeyError, FileNotFoundError,
                PermissionError, Exception) as e:
            QMessageBox.critical(self, 'Error', str(e))
            return

    def get_save_filepath(self, data: dict[str, pd.DataFrame]):
        self.save_filepath = str(Path(self.input_file_browser.file_dir, 'output.xlsx'))
        self.save_filepath, _ = QFileDialog().getSaveFileName(self,
                                                              'Save report as',
                                                              self.save_filepath,
                                                              excel_file_filter)
        if self.save_filepath:
            write_ozon_items(self.save_filepath, data)
            QMessageBox().information(self, 'Result', 'Report is saved!')


class FilepathBrowser(QWidget):
    def __init__(self, label_caption, dialog_caption, file_dir):
        super().__init__()
        self.__caption = dialog_caption
        self.file_dir = file_dir
        self.filepath = ''

        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel(label_caption)
        layout.addWidget(label)

        self.__path_input = QLineEdit()
        self.__path_input.setReadOnly(True)
        layout.addWidget(self.__path_input)

        browse_button = QPushButton('Browse...')
        browse_button.clicked.connect(self.get_filepath)
        layout.addWidget(browse_button)

    def get_filepath(self):
        self.filepath, _ = QFileDialog.getOpenFileName(self, self.__caption, self.file_dir, excel_file_filter)
        if self.filepath:
            self.__path_input.setText(self.filepath)
            self.file_dir = dirname(self.filepath)
