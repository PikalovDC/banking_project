# src/main.py
import os
from typing import Any, Dict, List

from src.external_api import get_amount_in_rubles
from src.processing import filter_by_description, filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def main() -> None:
    """
    Основная функция программы для работы с банковскими транзакциями.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор типа файла
    file_path = get_file_type_choice()
    transactions = load_transactions_from_file(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершена.")
        return

    # Фильтрация по статусу
    filtered_transactions = filter_by_status(transactions)

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Дополнительные фильтры и сортировка
    final_transactions = apply_additional_filters(filtered_transactions)

    # Вывод результатов
    print_transactions(final_transactions)


def get_file_type_choice() -> str:
    """Получает выбор типа файла от пользователя."""
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return get_file_path("JSON", ".json")
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            return get_file_path("CSV", ".csv")
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return get_file_path("XLSX", ".xlsx")
        else:
            print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")


def get_file_path(file_type: str, extension: str) -> str:
    """Получает путь к файлу от пользователя."""
    # Предлагаем стандартные пути, но позволяем изменить
    default_paths = {
        ".json": "data/operations.json",
        ".csv": "data/transactions.csv",
        ".xlsx": "data/transactions.xlsx"
    }

    default_path = default_paths.get(extension, f"data/transactions{extension}")

    print(f"Рекомендуемый путь: {default_path}")
    print("Нажмите Enter для использования рекомендуемого пути или введите свой путь:")

    while True:
        file_path = input("Путь к файлу: ").strip()

        # Если пользователь нажал Enter, используем путь по умолчанию
        if not file_path:
            file_path = default_path

        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл '{file_path}' не существует.")
            continue

        # Проверяем расширение
        if not file_path.lower().endswith(extension.lower()):
            print(f"Файл должен иметь расширение {extension}")
            continue

        return file_path


def load_transactions_from_file(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из файла."""
    transactions = load_transactions(file_path)
    print(f"Загружено {len(transactions)} транзакций")
    return transactions


def filter_by_status(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            filtered = filter_by_state(transactions, status)
            print(f'Операции отфильтрованы по статусу "{status}"')
            return filtered
        else:
            print(f'Статус операции "{status}" недоступен.')


def apply_additional_filters(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Применяет дополнительные фильтры и сортировку."""
    result = transactions

    # Сортировка по дате
    if ask_yes_no("Отсортировать операции по дате?"):
        sort_order = get_sort_order()
        result = sort_by_date(result, reverse=sort_order)

    # Фильтрация рублевых транзакций
    if ask_yes_no("Выводить только рублевые транзакции?"):
        result = [t for t in result if is_ruble_transaction(t)]

    # Фильтрация по описанию
    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска в описании: ").strip()
        result = filter_by_description(result, search_word)

    return result


def ask_yes_no(question: str) -> bool:
    """Задает вопрос Да/Нет и возвращает boolean."""
    while True:
        answer = input(f"{question} Да/Нет: ").strip().lower()
        if answer in ["да", "д", "yes", "y"]:
            return True
        elif answer in ["нет", "н", "no", "n"]:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def get_sort_order() -> bool:
    """Получает порядок сортировки от пользователя."""
    while True:
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if order in ["по убыванию", "убыванию", "убывание", "desc"]:
            return True  # reverse=True для убывания
        elif order in ["по возрастанию", "возрастанию", "возрастание", "asc"]:
            return False  # reverse=False для возрастания
        else:
            print("Пожалуйста, укажите 'по возрастанию' или 'по убыванию'")


def is_ruble_transaction(transaction: Dict[str, Any]) -> bool:
    """Проверяет, является ли транзакция рублевой."""
    currency_code = transaction.get('operationAmount', {}).get('currency', {}).get('code', '')
    return currency_code.upper() == 'RUB'


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит транзакции в отформатированном виде."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        print_transaction(transaction)
        print()  # Пустая строка между транзакциями


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Выводит одну транзакцию в отформатированном виде."""
    # Дата
    date = get_date(transaction['date'])
    print(date, transaction['description'])

    # Откуда
    if transaction.get('from'):
        from_masked = mask_account_card(transaction['from'])
        print(from_masked, end="")

    # Стрелка если есть "откуда"
    if transaction.get('from') and transaction.get('to'):
        print(" -> ", end="")

    # Куда
    to_masked = mask_account_card(transaction['to'])
    print(to_masked)

    # Сумма
    try:
        amount_rub = get_amount_in_rubles(transaction)
        currency_info = transaction['operationAmount']['currency']
        currency_name = currency_info.get('name', 'руб.')

        if currency_info.get('code', 'RUB') == 'RUB':
            print(f"Сумма: {amount_rub:.2f} {currency_name}")
        else:
            original_amount = transaction['operationAmount']['amount']
            print(f"Сумма: {original_amount} {currency_name} ({amount_rub:.2f} руб.)")
    except Exception:
        print(f"Сумма: {transaction['operationAmount']['amount']} (ошибка конвертации)")


if __name__ == "__main__":
    main()
