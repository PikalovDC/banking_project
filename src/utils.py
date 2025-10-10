import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.
    Возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, IOError, OSError):
        # Обрабатываем ошибки чтения файла, парсинга JSON и другие системные ошибки
        return []


# Пример использования кода
file_path = "../data/operations.json"
transactions = load_transactions(file_path)
print(f"Загружено транзакций: {len(transactions)}")

for i, transaction in enumerate(transactions[:3]):
    print(f"\nТранзакция {i + 1}:")
    print(f"ID: {transaction.get('id')}")
    print(f"Описание: {transaction.get('description')}")
