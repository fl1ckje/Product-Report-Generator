"""Типы перечислений"""
from enum import Enum, auto


class MessageType(Enum):
    """Тип сообщения для MessageBox"""
    INFO = auto()
    ERROR = auto()


class Marketplace(Enum):
    """Маркетплейс для анализа данных"""
    OZON = 'ОЗОН'
    WB = 'Wildberries'
