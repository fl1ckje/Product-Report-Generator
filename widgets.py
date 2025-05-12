from os.path import dirname
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFileDialog)

class ExcelFilepathBrowser(QWidget):
    """Виджет установки и показа пути к excel файлу"""

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