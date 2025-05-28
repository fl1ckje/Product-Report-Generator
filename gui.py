"""Представляет графический интерфейс приложения"""
from os import getcwd
from PySide6.QtWidgets import (
    QWidget,  QVBoxLayout, QTabWidget, QPushButton, QMessageBox)
from PySide6.QtCore import Qt

from widgets import FilepathBrowser, DragAndDropListWithControls
from enums import MessageType
from readers import read_ozon_data, read_wb_data
import analysis_tools.ozon
import datapacks
import writers.ozon


class MainWindow(QWidget):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setWindowTitle('Анализ финансового отчёта')
        self.setBaseSize(640, 200)
        self.setMinimumSize(640, 200)
        self.setMaximumSize(800, 600)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        tab_widget = QTabWidget()

        """
        OZON tab
        """
        ozon_tab = QWidget()
        tab_widget.addTab(ozon_tab, 'ОЗОН')
        ozon_layout = QVBoxLayout(ozon_tab)
        ozon_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # input file field
        self.__input_file_browser = FilepathBrowser(
            'Файл с данными:', 'Укажите путь к файлу с данными магазина ОЗОН',
            getcwd(), 'Файл Excel (*.xls *.xlsx)')
        ozon_layout.addWidget(self.__input_file_browser)

        # generate report button
        ozon_report_button = QPushButton('Проанализировать')
        ozon_report_button.clicked.connect(self.generate_ozon_report)
        ozon_layout.addWidget(ozon_report_button,
                              alignment=Qt.AlignmentFlag.AlignHCenter)

        """
        WB tab
        """
        wb_tab = QWidget()
        tab_widget.addTab(wb_tab, "Wildberries")
        wb_layout = QVBoxLayout(wb_tab)

        # zip files drag and drop list
        self.__wb_list = DragAndDropListWithControls('zip')
        wb_layout.addWidget(self.__wb_list)

        # generate report button
        wb_report_button = QPushButton('Проанализировать')
        wb_report_button.clicked.connect(self.generate_wb_report)
        wb_layout.addWidget(
            wb_report_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(tab_widget)

    def generate_ozon_report(self) -> None:
        """Читает и анализирует отчёт с маркетплейса ozon"""
        try:
            df = read_ozon_data(self.__input_file_browser.filepath())
            data = datapacks.OzonData(df)

            analysis_tools.ozon.analyse_data(data)
            writers.ozon.save_data(self.__input_file_browser.filepath(), data)

            self.show_message(MessageType.INFO, 'Результат',
                              'Анализ проведён успешно!')

        except (ValueError, KeyError, FileNotFoundError,
                PermissionError) as e:
            self.show_message(MessageType.ERROR, 'Ошибка', str(e))

    def generate_wb_report(self) -> None:
        """Читает и анализирует отчёты с маркетплейса wildberries"""
        try:
            df = read_wb_data(self.__wb_list.items())
            self.show_message(MessageType.INFO, 'Результат',
                              str(df.head()))
        except (ValueError, KeyError, FileNotFoundError,
                PermissionError) as e:
            self.show_message(MessageType.ERROR, 'Ошибка', str(e))

    def show_message(self, msg_type: MessageType, title: str, text: str):
        """Выводит сообщение в окне"""
        if msg_type == MessageType.INFO:
            return QMessageBox.information(self, title, text)
        elif msg_type == MessageType.ERROR:
            return QMessageBox.critical(self, title, text)

        raise NotImplementedError('Тип MessageBox не реалиован')
