import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях.
    """
    # Получаем информацию о сумме и валюте
    operation_amount = transaction.get('operationAmount', {})
    amount_str = operation_amount.get('amount', '0')
    currency_info = operation_amount.get('currency', {})
    currency_code = currency_info.get('code', 'RUB')

    # Преобразуем сумму в float
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid amount format: {amount_str}")

    # Если валюта уже в рублях, возвращаем как есть
    if currency_code == "RUB":
        return amount

    # Если валюта USD или EUR, конвертируем через API
    if currency_code in ["USD", "EUR"]:
        if not API_KEY:
            raise ValueError("API key not found. Please check your .env file")

        headers = {"apikey": API_KEY}
        params = {
            "from": currency_code,
            "to": "RUB",
            "amount": amount
        }

        try:
            response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("success", False):
                return data["result"]
            else:
                raise ValueError(f"API error: {data.get('error', {}).get('info', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request error: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Data parsing error: {e}")

    # Для других валют не поддерживаем конвертацию
    raise ValueError(f"Currency {currency_code} conversion not supported")
