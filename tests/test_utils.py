import json
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_valid_transactions():
    """
    Загрузка валидного JSON файла с транзакциями
    """
    # Подготовка: создаем тестовые данные транзакций
    test_transactions = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "RUB"}
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "USD"}
            }
        }
    ]

    # Мокаем ВСЕ зависимости: os.path.exists, os.path.getsize, open и json.load
    with patch('os.path.exists') as mock_exists, \
            patch('os.path.getsize') as mock_getsize, \
            patch('builtins.open', mock_open()) as mock_file, \
            patch('json.load') as mock_json_load:
        # Настраиваем моки для проверок файла
        mock_exists.return_value = True  # Файл существует
        mock_getsize.return_value = 100  # Файл не пустой
        mock_json_load.return_value = test_transactions  # Возвращаем тестовые данные

        # Действие: вызываем функцию
        result = load_transactions('test_path.json')

        # Проверка 1: файл был открыт с правильными параметрами
        mock_file.assert_called_once_with('test_path.json', 'r', encoding='utf-8')

        # Проверка 2: функция вернула правильные данные
        assert result == test_transactions
        assert isinstance(result, list)


def test_file_not_found_returns_empty_list():
    """
    Если файл не существует, возвращается пустой список
    """
    # Мокаем os.path.exists чтобы вернуть False (файл не существует)
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False

        # Действие: пытаемся загрузить несуществующий файл
        result = load_transactions('nonexistent.json')

        # Проверка: должен вернуться пустой список
        assert result == []
        assert isinstance(result, list)


def test_empty_file_returns_empty_list():
    """
    Если файл пустой, возвращается пустой список
    """
    # Мокаем os.path.exists и os.path.getsize
    with patch('os.path.exists') as mock_exists, \
            patch('os.path.getsize') as mock_getsize:
        mock_exists.return_value = True
        mock_getsize.return_value = 0  # Файл пустой

        # Действие: пытаемся загрузить пустой файл
        result = load_transactions('empty.json')

        # Проверка: должен вернуться пустой список
        assert result == []


def test_json_decode_error_returns_empty_list():
    """
    Если JSON невалидный, возвращается пустой список
    """
    with patch('os.path.exists') as mock_exists, \
            patch('os.path.getsize') as mock_getsize, \
            patch('builtins.open', mock_open(read_data='invalid json')), \
            patch('json.load') as mock_json_load:
        mock_exists.return_value = True
        mock_getsize.return_value = 100  # Файл не пустой
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)  # Ошибка парсинга

        # Действие: пытаемся загрузить файл с невалидным JSON
        result = load_transactions('invalid.json')

        # Проверка: должен вернуться пустой список
        assert result == []


def test_not_list_data_returns_empty_list():
    """
    Если JSON содержит не список, возвращается пустой список
    """
    # Подготовка: создаем JSON объект (словарь), а не список
    not_list_data = {"transaction": {"id": 1, "amount": "100"}}

    with patch('os.path.exists') as mock_exists, \
            patch('os.path.getsize') as mock_getsize, \
            patch('builtins.open', mock_open()), \
            patch('json.load') as mock_json_load:
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_json_load.return_value = not_list_data  # Возвращаем словарь, а не список

        # Действие: пытаемся загрузить файл с неправильной структурой
        result = load_transactions('not_list.json')

        # Проверка: должен вернуться пустой список
        assert result == []


def test_realistic_transaction_structure():
    """
    Загрузка транзакций с реальной структурой из operations.json
    """
    # Подготовка: создаем данные с реальной структурой
    realistic_transactions = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }
    ]

    with patch('os.path.exists') as mock_exists, \
            patch('os.path.getsize') as mock_getsize, \
            patch('builtins.open', mock_open()), \
            patch('json.load') as mock_json_load:
        mock_exists.return_value = True
        mock_getsize.return_value = 1000
        mock_json_load.return_value = realistic_transactions

        # Действие: загружаем транзакции
        result = load_transactions('real_operations.json')

        # Проверка 1: вернулись правильные данные
        assert len(result) == 1
        assert result[0]['id'] == 441945886

        # Проверка 2: структура транзакции сохранена
        transaction = result[0]
        assert 'operationAmount' in transaction
        assert 'currency' in transaction['operationAmount']
        assert transaction['operationAmount']['currency']['code'] == 'RUB'


def test_io_error_returns_empty_list():
    """
    Если ошибка ввода-вывода, возвращается пустой список
    """
    with patch('os.path.exists') as mock_exists, \
            patch('os.path.getsize') as mock_getsize, \
            patch('builtins.open') as mock_open_func:
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_open_func.side_effect = IOError("Disk error")

        # Действие: пытаемся загрузить файл с ошибкой IO
        result = load_transactions('error_file.json')

        # Проверка: должен вернуться пустой список
        assert result == []


if __name__ == '__main__':
    # Запускаем тесты
    unittest.main()
