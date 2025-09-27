from datetime import datetime

import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры для тестовых данных
@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми операциями"""
    return [
        {'id': 1258, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 1887, 'state': 'CANCELED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 175, 'state': 'EXECUTED', 'date': '2025-01-20T08:45:00.000000'},
        {'id': 18453, 'state': 'CANCELED', 'date': '2025-01-05T09:15:00.000000'},
        {'id': 2818, 'state': 'EXECUTED', 'date': '2024-01-25T16:10:00.000000'},
    ]


@pytest.fixture
def operations_with_same_dates():
    """Фикстура с операциями с одинаковыми датами"""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2024-01-15T10:30:00.000000'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2024-01-15T10:30:00.000000'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2024-01-15T10:30:00.000000'},
    ]


@pytest.fixture
def operations_without_state():
    """Фикстура с операциями без state"""
    return [
        {'id': 12845817, 'date': '2024-01-15T10:30:00.828288'},
        {'id': 1259287, 'date': '2024-01-10T14:20:00.000000'},
    ]


@pytest.fixture
def operations_with_invalid_dates():
    """Фикстура с операциями с некорректными датами"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': 'invalid-date'},  # Некорректный формат
        {'id': 2, 'state': 'EXECUTED', 'date': '2024-01-10T14:20:00.000000'},  # Корректная дата
    ]


@pytest.fixture
def operations_without_date():
    """Фикстура с операциями без даты"""
    return [
        {'id': 1, 'state': 'EXECUTED'},  # Нет даты
        {'id': 2, 'state': 'EXECUTED', 'date': '2024-01-10T14:20:00.000000'},  # Корректная дата
    ]


@pytest.fixture
def operations_with_wrong_date_type():
    """Фикстура с операциями с некорректным типом даты"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': 12345},  # Число вместо строки
        {'id': 2, 'state': 'EXECUTED', 'date': '2024-01-10T14:20:00.000000'},  # Корректная дата
    ]


# Тесты для filter_by_state
def test_filter_by_state_executed(sample_operations):
    """Тест фильтрации по EXECUTED"""
    assert len(filter_by_state(sample_operations, 'EXECUTED')) == 3


def test_filter_by_state_canceled(sample_operations):
    """Тест фильтрации по CANCELED"""
    assert len(filter_by_state(sample_operations, 'CANCELED')) == 2


def test_filter_by_state_default(sample_operations):
    """Тест фильтрации со значением по умолчанию"""
    assert len(filter_by_state(sample_operations)) == 3


def test_filter_by_state_no_matches(sample_operations):
    """Тест фильтрации когда нет совпадений"""
    assert len(filter_by_state(sample_operations, 'NONEXISTENT')) == 0


def test_filter_by_state_empty_list():
    """Тест фильтрации пустого списка"""
    assert len(filter_by_state([], 'EXECUTED')) == 0


def test_filter_by_state_no_state_key(operations_without_state):
    """Тест фильтрации когда нет ключа state"""
    assert len(filter_by_state(operations_without_state, 'EXECUTED')) == 0


# Тесты для sort_by_date
def test_sort_by_date_descending(sample_operations):
    """Тест сортировки по убыванию даты"""
    result = sort_by_date(sample_operations, reverse=True)
    dates = [op['date'] for op in result]
    assert dates == sorted(dates, key=lambda x: datetime.fromisoformat(x), reverse=True)


def test_sort_by_date_ascending(sample_operations):
    """Тест сортировки по возрастанию даты"""
    result = sort_by_date(sample_operations, reverse=False)
    dates = [op['date'] for op in result]
    assert dates == sorted(dates, key=lambda x: datetime.fromisoformat(x))


def test_sort_by_date_same_dates(operations_with_same_dates):
    """Тест сортировки при одинаковых датах"""
    result = sort_by_date(operations_with_same_dates)

    # При одинаковых датах порядок должен сохраниться
    ids = [op['id'] for op in result]
    assert ids == [41428829, 939719570, 594226727]  # Исходный порядок


def test_sort_by_date_raises_on_invalid_date_format(operations_with_invalid_dates):
    """Тест что функция выбрасывает ValueError при некорректном формате даты"""
    with pytest.raises(ValueError, match="Некорректный формат даты: 'invalid-date'"):
        sort_by_date(operations_with_invalid_dates)


def test_sort_by_date_raises_on_missing_date(operations_without_date):
    """Тест что функция выбрасывает ValueError при отсутствии даты"""
    with pytest.raises(ValueError, match="Отсутствует ключ 'date' в операции"):
        sort_by_date(operations_without_date)


def test_sort_by_date_raises_on_wrong_date_type(operations_with_wrong_date_type):
    """Тест что функция выбрасывает ValueError при некорректном типе даты"""
    with pytest.raises(ValueError, match="Некорректный тип даты:"):
        sort_by_date(operations_with_wrong_date_type)
