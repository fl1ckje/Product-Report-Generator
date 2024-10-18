from PySide6 import QtWidgets
from sys import exit
from cfg import Config
from gui import MainWindow

if __name__ == '__main__':
    _ = Config('ozon.json')
    app = QtWidgets.QApplication()
    main_win = MainWindow()
    exit(app.exec())
