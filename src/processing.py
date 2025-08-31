from typing import List, Dict, Any
from datetime import datetime

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
    Args:
        lists: Список словарей с операциями
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
    Возвращает отсортированный список операций
    """

    sorted_list = sorted(lists, key = lambda operation: datetime.fromisoformat(operation['date']) if 'date' in operation else datetime.min, reverse = reverse)
    return sorted_list
