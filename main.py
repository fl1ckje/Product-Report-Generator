"""Точка входа в программу"""

from sys import exit as sys_exit
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module

from app_props import AppProps
from enums import Marketplace
from gui import MainWindow

if __name__ == '__main__':
    AppProps.set_marketplace(Marketplace.OZON)
    app = QtWidgets.QApplication()  # pylint: disable=c-extension-no-member
    main_win = MainWindow()
    sys_exit(app.exec())
