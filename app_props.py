from enums import Marketplace


class AppConfig:
    __marketplace: Marketplace

    def __init__(self, marketplace: Marketplace):
        self.__marketplace = marketplace

    @staticmethod
    def marketplace():
        return AppConfig.__marketplace
