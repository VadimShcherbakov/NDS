"""Указаны отдельные вспомогательные скрипты"""

import json


def read_json(file_name: str) -> None:
    """Функция для чтения json"""
    with open(file_name, 'r', encoding='utf-8', newline='') as file:
        data = json.loads(file.read())
    return data

