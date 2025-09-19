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
    Args:
        lists: Список словарей с операциями
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
    Возвращает:
        Отсортированный список операций
    Ошибка:
        ValueError: Если встречается некорректный формат даты
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
