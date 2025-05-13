"""Точка входа в программу"""

from sys import exit as sys_exit
from PySide6 import QtWidgets

from gui import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    main_win = MainWindow()
    main_win.show()
    sys_exit(app.exec())
