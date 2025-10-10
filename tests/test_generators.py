from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def transactions_with_missing_data():
    """Фикстура с транзакциями с отсутствующими данными"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            # Нет operationAmount
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "100",
                # Нет currency
            }
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "200",
                "currency": {
                    "name": "USD"
                    # Нет code
                }
            }
        }
    ]


"""Тесты для функции filter_by_currency"""


def test_filter_usd_transactions(sample_transactions):
    """Тест фильтрации USD транзакций"""

    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

    assert len(usd_transactions) == 3
    assert all(t['operationAmount']['currency']['code'] == 'USD' for t in usd_transactions)
    assert {t['id'] for t in usd_transactions} == {939719570, 142264268, 895315941}


def test_filter_nonexistent_currency(sample_transactions):
    """Тест фильтрации несуществующей валюты"""
    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(eur_transactions) == 0


def test_filter_empty_list():
    """Тест фильтрации пустого списка"""
    result = list(filter_by_currency([], "USD"))
    assert len(result) == 0


def test_filter_transactions_missing_data(transactions_with_missing_data):
    """Тест фильтрации транзакций с отсутствующими данными"""
    result = list(filter_by_currency(transactions_with_missing_data, "USD"))
    assert len(result) == 0


"""Тесты для функции transaction_descriptions"""


def test_descriptions_extraction(sample_transactions):
    """Тест извлечения описаний"""
    descriptions = list(transaction_descriptions(sample_transactions))

    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]

    assert descriptions == expected


def test_descriptions_empty_list():
    """Тест с пустым списком транзакций"""
    result = list(transaction_descriptions([]))
    assert result == []


def test_descriptions_missing_field(transactions_with_missing_data):
    """Тест с транзакциями без описания"""
    descriptions = list(transaction_descriptions(transactions_with_missing_data))
    assert descriptions == ['', '', '']  # Пустые строки для отсутствующих описаний


"""Тесты для функции card_number_generator"""


def test_generator_basic_range():
    """Тест генерации базового диапазона"""
    result = list(card_number_generator(1, 5))

    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]

    assert result == expected


def test_generator_single_number():
    """Тест генерации одного номера"""
    result = list(card_number_generator(123, 123))
    assert result == ["0000 0000 0000 0123"]


def test_generator_large_numbers():
    """Тест генерации больших номеров"""
    result = list(card_number_generator(9999999999999995, 9999999999999999))

    expected = [
        "9999 9999 9999 9995",
        "9999 9999 9999 9996",
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999"
    ]

    assert result == expected


def test_generator_format():
    """Тест формата номеров карт"""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    card_number = next(generator)

    # Проверяем формат
    assert len(card_number) == 19  # 16 цифр + 3 пробела
    assert card_number.replace(" ", "").isdigit()
    assert card_number == "1234 5678 9012 3456"


def test_generator_invalid_range():
    """Тест обработки неверного диапазона"""
    with pytest.raises(TypeError):
        list(card_number_generator(0, 5))  # start < 1

    with pytest.raises(TypeError):
        list(card_number_generator(1, 10000000000000000))  # end > max

    with pytest.raises(TypeError):
        list(card_number_generator(10, 5))  # start > end


def test_generator_invalid_types():
    """Тест обработки неверных типов"""
    with pytest.raises(TypeError):
        list(card_number_generator("1", 5))  # start не int

    with pytest.raises(TypeError):
        list(card_number_generator(1, "5"))  # end не int
