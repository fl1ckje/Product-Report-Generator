from os.path import dirname
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QFileDialog)
from PySide6.QtCore import Qt


class FilepathBrowser(QWidget):
    """Виджет установки и показа пути к файлу"""

    def __init__(self, widget_caption: str, dialog_caption: str, file_dir, filter: str):
        super().__init__()

        self.__caption = dialog_caption
        self.__dir = file_dir
        self.__filter = filter

        layout = QHBoxLayout()
        self.setLayout(layout)

        # подпись виджета
        label = QLabel(widget_caption)
        layout.addWidget(label)

        self.__filepath_input = QLineEdit()
        layout.addWidget(self.__filepath_input)

        # кнопка обзора файла
        browse_button = QPushButton('Обзор...')
        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

    def browse_file(self):
        """Показывает диалог для получения пути к файлу"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, self.__caption, self.__dir, self.__filter)
        if filepath:
            self.__filepath_input.setText(filepath)
            self.__dir = dirname(filepath)

    def filepath(self):
        """Возвращает путь к файлу"""
        return self.__filepath_input.text()


class DragAndDropList(QListWidget):
    """Виджет списка с поддержкой drag and drop и управлением элементами"""

    def __init__(self, accepted_format=None):
        super().__init__()

        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.accepted_format = accepted_format

    def dragEnterEvent(self, event):
        """Действие при перетаскивании файлов внутрь списка"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if not urls:
                return

            extensions = [url.toLocalFile().lower().split('.')[-1]
                          for url in urls]

            accept = not bool(self.accepted_format) or all(
                ext in self.accepted_format for ext in extensions)
            event.accept() if accept else event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Действие при перетаскивании файлов внутри списка"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if not urls:
                return

            extensions = [url.toLocalFile().lower().split('.')[-1]
                          for url in urls]

            accept = not bool(self.accepted_format) or all(
                ext in self.accepted_format for ext in extensions)

            event.accept() if accept else event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Действие при отпускании файлов внутри списка"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        for file_path in files:
            self.addItem(file_path)
        event.accept()

    def keyPressEvent(self, event):
        """Обработка нажатия клавиш на клавиатуре"""
        if event.key() == Qt.Key.Key_Delete:
            selected_items = self.selectedItems()
            for item in selected_items:
                self.takeItem(self.row(item))
        else:
            super().keyPressEvent(event)

    def remove_selected(self):
        """Удаляет выбранные файлы из списка"""
        selected_items = self.selectedItems()
        for item in selected_items:
            self.takeItem(self.row(item))
