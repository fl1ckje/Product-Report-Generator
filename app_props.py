"""Свойства приложения"""

from enums import Marketplace


class AppProps:
    """Свойства приложения"""
    __marketplace: Marketplace

    @staticmethod
    def set_marketplace(marketplace: Marketplace):
        """Устанавливает маркетплейс приложения"""
        AppProps.__marketplace = marketplace

    @staticmethod
    def marketplace():
        """Возвращает маркетплейс приложения"""
        return AppProps.__marketplace
