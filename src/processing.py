import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    Args:
        operations: Список словарей для фильтрации
        state: Значение для фильтрации (по умолчанию "EXECUTED")
    Возвращает отфильтрованный список словарей
    """

    new_list: List[Dict[str, Any]] = []
    for dict_ in operations:
        if "state" in dict_ and state == dict_["state"]:
            new_list.append(dict_)
    return new_list


def sort_by_date(lists: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.
    Выбрасывает ValueError при некорректном формате даты.
    """

    def get_date_key(operation: Dict[str, Any]) -> datetime:
        """Вспомогательная функция для получения даты с проверкой"""
        if 'date' not in operation:
            raise ValueError(f"Отсутствует ключ 'date' в операции: {operation}")

        try:
            return datetime.fromisoformat(operation['date'])
        except ValueError:
            raise ValueError(f"Некорректный формат даты: '{operation['date']}' в операции: {operation}")
        except TypeError:
            raise ValueError(f"Некорректный тип даты: {type(operation['date'])} в операции: {operation}")

    return sorted(lists, key=get_date_key, reverse=reverse)


def filter_by_description(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует банковские операции по строке поиска в описании.
    """
    if not search:
        return data

    filtered_operations = []

    for operation in data:
        description = operation.get('description', '')

        # Используем re.search для поиска с игнорированием регистра
        if re.search(search, description, re.IGNORECASE):
            filtered_operations.append(operation)

    return filtered_operations


def count_operations_by_category(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.
    """
    all_found_categories = []

    for operation in data:
        description = operation.get('description', '')

        for category in categories:
            escaped_category = re.escape(category)
            pattern = rf'(^|\s){escaped_category}($|\s|[,\.!?])'
            if re.search(pattern, description, re.IGNORECASE):
                all_found_categories.append(category)
                break

    category_counter = Counter(all_found_categories)

    # Используем defaultdict для автоматических нулей
    result = defaultdict(int)
    result.update(category_counter)  # Добавляем подсчитанные значения

    # Возвращаем обычный словарь с гарантированно всеми категориями
    return {category: result[category] for category in categories}
