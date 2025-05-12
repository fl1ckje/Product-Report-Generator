"""Представляет графический интерфейс приложения"""

from os import getcwd
from os.path import dirname

from PySide6.QtWidgets import (QWidget,  QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
                               QPushButton, QFileDialog, QMessageBox, QComboBox, QGroupBox)
from PySide6.QtCore import Qt

from enums import Marketplace, MessageType
from readers import read_excel_data
import analysis_tools.ozon
import datapacks
import writers
import writers.ozon


class MainWindow(QWidget):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Анализ финансового отчёта')
        self.setFixedSize(640, 0)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        marketplace_groupbox = QGroupBox()
        marketplace_groupbox.setTitle('Магазин')
        marketplace_layout = QHBoxLayout()
        self.__marketplace_combobox = QComboBox()
        self.__marketplace_combobox.addItems(
            [item.value for item in Marketplace])
        marketplace_layout.addWidget(self.__marketplace_combobox)
        marketplace_groupbox.setLayout(marketplace_layout)
        main_layout.addWidget(marketplace_groupbox)

        self.input_file_browser = FilepathBrowser(
            'Файл с данными:', 'Укажите путь к файлу с данными', getcwd())
        main_layout.addWidget(self.input_file_browser)

        generate_report_button = QPushButton('Проанализировать')
        generate_report_button.clicked.connect(self.analyse_data)
        main_layout.addWidget(generate_report_button,
                              alignment=Qt.AlignmentFlag.AlignHCenter)

        self.show()

    def analyse_data(self):
        """
        Читает и анализирует отчёт в
        зависимости от выбранного магазина
        """
        try:
            df = read_excel_data(self.input_file_browser.filepath())

            marketplace = Marketplace(self.__marketplace_combobox.currentText())
            if marketplace == Marketplace.OZON:
                data = datapacks.OzonData(df)
                analysis_tools.ozon.analyse_data(data)
                writers.ozon.save_data(
                    self.input_file_browser.filepath(), data)
            elif marketplace == Marketplace.WILDBERRIES:
                # data = data_packs.WildberriesData(df)
                pass

            self.show_message(MessageType.INFO, 'Результат',
                              'Анализ проведён успешно!')
        except (ValueError, KeyError, FileNotFoundError,
                PermissionError) as e:
            self.show_message(MessageType.ERROR, 'Ошибка', str(e))

    def show_message(self, msg_type: MessageType, title: str, text: str):
        """Выводит сообщение в окне"""
        if msg_type == MessageType.INFO:
            return QMessageBox.information(self, title, text)

        if msg_type == MessageType.ERROR:
            return QMessageBox.critical(self, title, text)

        raise NotImplementedError('Тип MessageBox не реалиован')


class FilepathBrowser(QWidget):
    """Виджет установки и показа пути к файлу"""

    def __init__(self, widget_caption, dialog_caption, file_dir):
        super().__init__()

        self.__caption = dialog_caption
        self.__file_dir = file_dir

        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel(widget_caption)
        layout.addWidget(label)

        self.__path_input = QLineEdit()
        layout.addWidget(self.__path_input)

        browse_button = QPushButton('Обзор...')
        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

    def browse_file(self):
        """Показывает диалог для установки пути к файлу"""
        filepath, _ = QFileDialog.getOpenFileName(self, self.__caption, self.__file_dir,
                                                  'Файл Excel (*.xls *.xlsx)')
        if filepath:
            self.__path_input.setText(filepath)
            self.__file_dir = dirname(filepath)

    def filepath(self):
        """Возвращает путь к файлу"""
        return self.__path_input.text()
