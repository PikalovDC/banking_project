import csv
import os
import tempfile
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.file_handlers import load_csv_transactions, load_excel_transactions


@pytest.fixture
def sample_csv_data():
    return """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;
Счет 39745660563456619397;Перевод организации
3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;
Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту
5380041;CANCELED;2021-02-01T11:54:58Z;23789;Peso;UYU;;
Счет 23294994494356835683;Открытие вклада"""


def test_load_csv_transactions_success(sample_csv_data):
    """Тест успешной загрузки CSV"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(sample_csv_data)
        temp_path = f.name

    try:
        result = load_csv_transactions(temp_path)
        assert len(result) == 3
        assert result[0]['id'] == 650703
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['operationAmount']['amount'] == '16210'
        assert result[0]['operationAmount']['currency']['code'] == 'PEN'
        assert result[2]['from'] is None
    finally:
        os.unlink(temp_path)


def test_load_csv_transactions_file_not_found():
    """Тест загрузки несуществующего CSV файла"""
    result = load_csv_transactions('nonexistent.csv')
    assert result == []


def test_load_csv_transactions_empty_file():
    """Тест загрузки пустого CSV файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_path = f.name

    try:
        result = load_csv_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


@patch('src.file_handlers.os.path.exists')
@patch('src.file_handlers.os.path.getsize')
@patch('builtins.open', new_callable=mock_open)
@patch('csv.DictReader')
def test_load_csv_transactions_with_mock(mock_dict_reader, mock_file, mock_getsize, mock_exists):
    """Тест загрузки CSV с использованием Mock"""
    # Настраиваем моки для проверки файла
    mock_exists.return_value = True
    mock_getsize.return_value = 100

    # Настраиваем DictReader чтобы возвращал тестовые данные
    mock_dict_reader.return_value = [
        {
            'id': '123',
            'state': 'EXECUTED',
            'date': '2023-01-01',
            'amount': '1000',
            'currency_name': 'RUB',
            'currency_code': 'RUB',
            'from': 'Card 1234567812345678',
            'to': 'Account 12345678901234567890',
            'description': 'Test'
        }
    ]

    result = load_csv_transactions('test.csv')

    assert len(result) == 1
    assert result[0]['id'] == 123
    assert result[0]['state'] == 'EXECUTED'
    assert result[0]['operationAmount']['amount'] == '1000'
    # Проверяем что файл открывался
    mock_file.assert_called_once_with('test.csv', 'r', encoding='utf-8')


def test_load_csv_transactions_invalid_data():
    """Тест загрузки CSV с некорректными данными"""
    invalid_data = """id;state;date;amount;currency_name;currency_code;from;to;description
invalid;EXECUTED;2023-01-01;1000;RUB;RUB;Card 1234;Account 1234;Test"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(invalid_data)
        temp_path = f.name

    try:
        result = load_csv_transactions(temp_path)
        assert len(result) == 0
    finally:
        os.unlink(temp_path)


@pytest.fixture
def sample_excel_data():
    return pd.DataFrame({
        'id': [650703, 3598919, 5380041],
        'state': ['EXECUTED', 'EXECUTED', 'CANCELED'],
        'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z', '2021-02-01T11:54:58Z'],
        'amount': ['16210', '29740', '23789'],
        'currency_name': ['Sol', 'Peso', 'Peso'],
        'currency_code': ['PEN', 'COP', 'UYU'],
        'from': ['Счет 58803664561298323391', 'Discover 3172601889670065', None],
        'to': ['Счет 39745660563456619397', 'Discover 0720428384694643', 'Счет 23294994494356835683'],
        'description': ['Перевод организации', 'Перевод с карты на карту', 'Открытие вклада']
    })


def test_load_excel_transactions_success(sample_excel_data):
    """Тест успешной загрузки Excel"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        temp_path = f.name

    try:
        sample_excel_data.to_excel(temp_path, index=False, engine='openpyxl')
        result = load_excel_transactions(temp_path)

        assert len(result) == 3
        assert result[0]['id'] == 650703
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['operationAmount']['amount'] == '16210'
        assert result[2]['from'] is None
    finally:
        os.unlink(temp_path)


def test_load_excel_transactions_file_not_found():
    """Тест загрузки несуществующего Excel файла"""
    result = load_excel_transactions('nonexistent.xlsx')
    assert result == []


def test_load_excel_transactions_empty_file():
    """Тест загрузки пустого Excel файла"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        temp_path = f.name

    try:
        result = load_excel_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


@patch('src.file_handlers.os.path.exists')
@patch('src.file_handlers.os.path.getsize')
@patch('src.file_handlers.pd.read_excel')
def test_load_excel_transactions_with_mock(mock_read_excel, mock_getsize, mock_exists):
    """Тест загрузки Excel с использованием Mock"""
    # Настраиваем моки для проверки файла
    mock_exists.return_value = True
    mock_getsize.return_value = 100

    # Создаем реальный DataFrame для теста
    test_data = {
        'id': [123],
        'state': ['EXECUTED'],
        'date': ['2023-01-01'],
        'amount': ['1000'],
        'currency_name': ['RUB'],
        'currency_code': ['RUB'],
        'from': ['Card 1234'],
        'to': ['Account 1234'],
        'description': ['Test']
    }
    mock_df = pd.DataFrame(test_data)
    mock_read_excel.return_value = mock_df

    result = load_excel_transactions('test.xlsx')

    assert len(result) == 1
    assert result[0]['id'] == 123
    assert result[0]['state'] == 'EXECUTED'
    mock_read_excel.assert_called_once_with('test.xlsx')


@patch('src.file_handlers.os.path.exists')
@patch('src.file_handlers.os.path.getsize')
@patch('src.file_handlers.pd.read_excel')
def test_load_excel_transactions_invalid_data(mock_read_excel, mock_getsize, mock_exists):
    """Тест загрузки Excel с некорректными данными"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100

    # DataFrame с невалидными данными
    test_data = {
        'id': ['invalid'],  # Невалидный ID
        'state': ['EXECUTED'],
        'date': ['2023-01-01'],
        'amount': ['1000'],
        'currency_name': ['RUB'],
        'currency_code': ['RUB'],
        'from': ['Card 1234'],
        'to': ['Account 1234'],
        'description': ['Test']
    }
    mock_df = pd.DataFrame(test_data)
    mock_read_excel.return_value = mock_df

    result = load_excel_transactions('test.xlsx')

    # Должен пропустить строку с невалидным ID
    assert len(result) == 0
