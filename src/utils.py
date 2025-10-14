import json
import logging
import os
from typing import Any, Dict, List

from src.logger_config import setup_logging

# Создан отдельный объект логера для модуля utils
logger = logging.getLogger('utils')


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.
    Возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    # Логирование успешного случая - начало работы функции
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            # Логирование ошибочного случая с уровнем ERROR
            logger.error(f"Файл не найден: {file_path}")
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            # Логирование ошибочного случая с уровнем ERROR
            logger.error(f"Файл пустой: {file_path}")
            return []

        # Открываем и читаем файл
        logger.debug(f"Открытие файла: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            # Логирование успешного случая - результат работы функции
            logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
            return data
        else:
            # Логирование ошибочного случая с уровнем ERROR
            logger.error(f"Файл {file_path} содержит не список, а {type(data).__name__}")
            return []

    except (json.JSONDecodeError, IOError, OSError) as e:
        # Обрабатываем ошибки чтения файла, парсинга JSON и другие системные ошибки
        # Логирование ошибочного случая с уровнем ERROR
        logger.error(f"Ошибка при загрузке файла {file_path}: {e}")
        return []


setup_logging()
