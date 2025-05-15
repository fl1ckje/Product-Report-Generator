from os import getcwd
from os.path import dirname

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QListWidget, QGridLayout,
                               QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt


class FilepathBrowser(QWidget):
    """Виджет поля пути к файлу"""

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

    def browse_file(self) -> None:
        """Показывает диалог для получения пути к файлу"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, self.__caption, self.__dir, self.__filter)
        if filepath:
            self.__filepath_input.setText(filepath)
            self.__dir = dirname(filepath)

    def filepath(self) -> str:
        """Возвращает путь к файлу"""
        return self.__filepath_input.text()


class DragAndDropListWithControls(QWidget):
    """Виджет списка с поддержкой drag and drop и управлением элементами"""

    def __init__(self, accepted_format: str = None):
        super().__init__()

        self.accepted_format = accepted_format
        self.__dir = getcwd()

        layout = QGridLayout()
        self.setLayout(layout)

        hint_label = QLabel(
            f'Перетащите {self.accepted_format} файлы в список ниже или используйте кнопку \"+\"')
        layout.addWidget(hint_label, 0, 0)
        self.__file_list = self.FileList(self.accepted_format)
        layout.addWidget(self.__file_list, 1, 0)

        buttons_layout = QVBoxLayout()
        add_button = QPushButton("+")
        add_button.clicked.connect(self.__add_item)
        buttons_layout.addWidget(add_button)
        remove_button = QPushButton("-")
        remove_button.clicked.connect(self.__remove_selected_items)
        buttons_layout.addWidget(remove_button)

        layout.addLayout(buttons_layout, 1, 1, Qt.AlignmentFlag.AlignTop)

    def items(self) -> list[str]:
        return [self.__file_list.item(i).text() for i in range(self.__file_list.count())]

    def __add_item(self) -> None:
        """Показывает диалог для добавления пути к файлу"""
        files, _ = QFileDialog.getOpenFileNames(
            self, f'Укажите путь к 1 или более {self.accepted_format} файлам', self.__dir, f"(*.{self.accepted_format})")
        if files:
            for file in files:
                self.__file_list.addItem(file)
            self.__dir = dirname(files[0])

    def __remove_selected_items(self) -> None:
        self.__file_list.remove_selected_items()

    class FileList(QListWidget):
        """Drag'n'drop список файлов с фильтром по формату"""

        def __init__(self, accepted_format: str):
            super().__init__()

            self.setAcceptDrops(True)
            self.setSelectionMode(
                QAbstractItemView.SelectionMode.ExtendedSelection)
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.accepted_format = accepted_format

        def dragEnterEvent(self, event) -> None:
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

        def dragMoveEvent(self, event) -> None:
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

        def dropEvent(self, event) -> None:
            """Действие при отпускании файлов внутри списка"""
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            for file_path in files:
                self.addItem(file_path)
            event.accept()

        def keyPressEvent(self, event) -> None:
            """Обработка нажатия клавиш на клавиатуре"""
            if event.key() == Qt.Key.Key_Delete:
                selected_items = self.selectedItems()
                for item in selected_items:
                    self.takeItem(self.row(item))
            else:
                super().keyPressEvent(event)

        def remove_selected_items(self) -> None:
            """Удаляет выбранные файлы из списка"""
            selected_items = self.selectedItems()
            for item in selected_items:
                self.takeItem(self.row(item))
