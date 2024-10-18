from os.path import join, dirname
from dataclasses import dataclass
from typing import Dict, Any
from enums import Marketplace
import sys
import json


@dataclass
class Config:
    __marketplace: Marketplace

    __items_headers: Dict[str, Any]
    __items_headers_fmt: Dict[str, Any]

    def __init__(self, filename):
        filepath = _get_config_path(filename)
        cfg_json = _read_config_json(filepath)

        Config.__marketplace = _parse_enum(cfg_json.pop('marketplace'))

        Config.__items_headers = cfg_json['items_headers']
        Config.__items_headers_fmt = cfg_json['items_headers_fmt']

    @staticmethod
    def marketplace():
        return Config.__marketplace

    @staticmethod
    def items_headers():
        return Config.__items_headers

    @staticmethod
    def items_headers_fmt():
        return Config.__items_headers_fmt


def _read_config_json(filepath: str):
    required_keys = ['marketplace', 'items_headers', 'items_headers_fmt']
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
            if not all(key in json_content for key in required_keys):
                raise ValueError("Missing required keys in JSON")
            return json_content
    except FileNotFoundError:
        raise FileNotFoundError("Error: Config file not found.")
    except json.JSONDecodeError:
        raise Exception("Error: Invalid JSON format in the config file.")


def _get_config_path(filename: str):
    if getattr(sys, 'frozen', False):
        # noinspection PyProtectedMember
        return join(sys._MEIPASS, 'cfg', filename)
    else:
        return join(dirname(__file__), 'cfg', filename)


def _parse_enum(value: str) -> Marketplace:
    try:
        return Marketplace[value.upper()]
    except KeyError:
        raise ValueError(f"Invalid marketplace value in config: '{value}'.")
