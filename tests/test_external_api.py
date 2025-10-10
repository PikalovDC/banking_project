import unittest
from unittest.mock import patch

from src.external_api import get_amount_in_rubles

"""
Тесты для функции get_amount_in_rubles
"""


def test_rub_transaction_returns_same_amount():
    """
    ТЕСТ: Транзакция в рублях возвращает ту же сумму
    """
    # Подготовка: создаем тестовую транзакцию в рублях
    rub_transaction = {
        "id": 1,
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    }

    # Вызываем функцию
    result = get_amount_in_rubles(rub_transaction)
    assert result == 1000.50


def test_usd_transaction_calls_api_and_returns_converted_amount():
    usd_transaction = {
        "id": 2,
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }

    # Мокаем requests.get и ПЕРЕЗАГРУЖАЕМ модуль чтобы перехватить API_KEY
    with patch('src.external_api.requests.get') as mock_get:
        # Временно подменяем API_KEY в модуле
        import src.external_api
        original_api_key = src.external_api.API_KEY
        src.external_api.API_KEY = 'test_api_key'

        try:
            # Настраиваем мок для API
            mock_get.return_value.json.return_value = {
                "success": True,
                "result": 7500.0
            }

            # Вызываем функцию
            result = get_amount_in_rubles(usd_transaction)

            # API было вызвано с правильными параметрами
            mock_get.assert_called_once_with(
                "https://api.apilayer.com/exchangerates_data/convert",
                headers={"apikey": "test_api_key"},
                params={
                    "from": "USD",
                    "to": "RUB",
                    "amount": 100.0
                },
                timeout=10
            )

            # Функция вернула конвертированную сумму
            assert result == 7500.0

        finally:
            # Восстанавливаем оригинальный ключ
            src.external_api.API_KEY = original_api_key


def test_api_returns_error_raises_exception():
    usd_transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.requests.get') as mock_get, \
            patch('src.external_api.os.getenv') as mock_getenv:
        mock_getenv.return_value = 'test_api_key'
        mock_get.return_value.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }

        with unittest.TestCase().assertRaises(ValueError) as context:
            get_amount_in_rubles(usd_transaction)

        # Проверяем текст ошибки
        assert "API error" in str(context.exception)


def test_network_error_raises_exception():
    usd_transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    with patch('src.external_api.requests.get') as mock_get:
        # Временно подменяем API_KEY
        import src.external_api
        original_api_key = src.external_api.API_KEY
        src.external_api.API_KEY = 'test_api_key'

        try:
            # ИСПРАВЛЕНИЕ: используем requests.exceptions.RequestException вместо Exception
            import requests.exceptions
            mock_get.side_effect = requests.exceptions.RequestException("Network is down")

            with unittest.TestCase().assertRaises(ValueError) as context:
                get_amount_in_rubles(usd_transaction)

            assert "Request error" in str(context.exception)
            assert "Network is down" in str(context.exception)

        finally:
            src.external_api.API_KEY = original_api_key


def test_invalid_amount_format_raises_exception():
    """
    Неправильный формат суммы вызывает исключение
    """
    invalid_transaction = {
        "operationAmount": {
            "amount": "not_a_number",  # Это не число!
            "currency": {"code": "RUB"}
        }
    }

    with unittest.TestCase().assertRaises(ValueError) as context:
        get_amount_in_rubles(invalid_transaction)

    assert "Invalid amount format" in str(context.exception)


def test_unsupported_currency_raises_exception():
    jpy_transaction = {
        "operationAmount": {
            "amount": "1000.00",
            "currency": {"code": "JPY"}
        }
    }

    with unittest.TestCase().assertRaises(ValueError) as context:
        get_amount_in_rubles(jpy_transaction)

    assert "Currency JPY conversion not supported" in str(context.exception)


def setUpModule():
    """
    Эта функция запускается ПЕРЕД всеми тестами в этом файле
    Устанавливаем тестовый API ключ в переменные окружения
    """
    import os
    os.environ['API_KEY'] = 'test_api_key'


def tearDownModule():
    """
    Эта функция запускается ПОСЛЕ всех тестов в этом файле
    Очищаем тестовые переменные окружения
    """
    import os
    if 'API_KEY' in os.environ:
        del os.environ['API_KEY']


if __name__ == '__main__':
    # Запускаем тесты
    unittest.main()
