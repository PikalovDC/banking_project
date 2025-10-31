# Банковские операции
Это виджет банковских операций клиента, который показывает несколько последних успешных банковских операций.

## Содержание


## Установка
git clone https://github.com/PikalovDC/banking_project.git

## Требования
* Python 3.7+
* Стандартные библиотеки Python

## Функционал

### Маскировка данных:

1. Маскировка номера карты:
get_mask_card_number().
Маскирует номер банковской карты в формате XXXX XX** **** XXXX

#### Пример использования
from masks import get_mask_card_number
* Интерактивный режим
masked_card = get_mask_card_number()
* Прямая передача номера
masked_card = get_mask_card_number("1234567890123456")
* Результат: "1234 56** **** 3456"

2. Маскировка номера счета: get_mask_account().
Маскирует номер счета в формате **XXXX

#### Пример использования
from masks import get_mask_account
* Интерактивный режим
masked_account = get_mask_account()
* Прямая передача номера
masked_account = get_mask_account("12345678901234567890")
* Результат: "**7890"

3. Маскировка данных (номер карты, счета): mask_account_card().
Автоматически определяет тип данных (карта или счет) и применяет соответствующую маску.

#### Пример использования
from main import mask_account_card

* result = mask_account_card("Visa Platinum 7000792289606361")
Результат: "Visa Platinum 7000 79** **** 6361"
* result = mask_account_card("Счет 73654108430135874305")
Результат: "Счет **4305"

### Работа с датами

1. get_date().
Преобразует дату из ISO формата в формат "ДД.ММ.ГГГГ".

#### Пример использования
from main import get_date
* formatted_date = get_date("2024-03-11T02:26:18.671407")
Результат: "11.03.2024"

### Обработка банковских операций

1. filter_by_state().
Фильтрует список операций по статусу выполнения.

#### Пример использования
from main import filter_by_state

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

executed_ops = filter_by_state(operations, 'EXECUTED')
#### Вернет операции со статусом 'EXECUTED'

2. sort_by_date().
Сортирует операции по дате
#### Пример использования

from main import sort_by_date

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

* Сортировка по убыванию (сначала новые)
sorted_ops = sort_by_date(operations, True)

* Сортировка по возрастанию (сначала старые)
sorted_ops = sort_by_date(operations, False)

### Открытие файлов и конвертация валюты 
#### Открытие JSON-файла - load_transactions()
Загружает список транзакций из JSON-файла.
Возвращает список словарей с данными транзакций

from src.load_transactions import load_transactions

#### Пример использования:
transactions = load_json_transactions("../data/operations.json")

if transactions:
    print(f"Успешно загружено {len(transactions)} транзакций")
    # Пример вывода первой транзакции
    first_tx = transactions[0]
    print(f"ID: {first_tx['id']}")
    print(f"Сумма: {first_tx['operationAmount']['amount']} {first_tx['operationAmount']['currency']['code']}")
else:
    print("Не удалось загрузить транзакции или файл пуст")

#### Открытие csv-файла - load_csv_transactions()
Загружает список транзакций из csv-файла.
Возвращает список словарей с данными транзакций

from src.file_handlers import load_csv_transactions

#### Пример использования:
transactions = load_csv_transactions('data/transactions.csv'), где 'transactions.csv' - файл csv с транзакциями

#### Открытие excel-файла - load_excel_transactions()
Загружает список транзакций из excel-файла.
Возвращает список словарей с данными транзакций

from src.file_handlers import load_excel_transactions

#### Пример использования:
transactions = load_excel_transactions('data/transactions.xlsx'), где 'transactions.xlsx' - файл excel с транзакциями


#### Конвертация валюты - get_amount_in_rubles()
Конвертирует сумму транзакции в рубли.

#### Пример использования:
from src.external_api import get_amount_in_rubles

Транзакция в рублях
rub_transaction = {
    "operationAmount": {
        "amount": "1500.75",
        "currency": {"code": "RUB"}
    }
}
result = get_amount_in_rubles(rub_transaction)  # 1500.75

Транзакция в USD (требует API ключ)
usd_transaction = {
    "operationAmount": {
        "amount": "100.00", 
        "currency": {"code": "USD"}
    }
}
result = get_amount_in_rubles(usd_transaction)  # 7500.0 (при курсе 75)



## Декораторы
### Декоратор логирования log()
Декоратор для автоматического логирования выполнения функций
#### Пример использования:
Импорт - from decorators import log

* Логирование в файл:
@log(filename="operations.log")
def process_transaction(amount: float, currency: str) -> dict:
    """Обработка банковской транзакции"""
    return {"status": "success", "amount": amount, "currency": currency}

* Логирование в консоль:
@log()
def validate_card(card_number: str) -> bool:
    """Валидация номера карты"""
    return len(card_number) == 16 and card_number.isdigit()

* Использование: 
process_transaction(1000.0, "USD")  # Запись в operations.log
validate_card("1234567890123456")   # Вывод в консоль

Формат логов:

Успешное выполнение: function_name ok

Ошибка: function_name error: ErrorType. Inputs: (args), {kwargs}


## Генераторы
### Фильтрация банковских операций

1. `filter_by_currency()`
Фильтрует транзакции по коду валюты и возвращает итератор.
#### Пример использования
from generators import filter_by_currency

transactions = [
    {
        "id": 939719570,
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        }
    },
    {
        "id": 873106923,
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "RUB", "code": "RUB"}
        }
    }
]

#### Получение USD транзакций
usd_transactions = filter_by_currency(transactions, "USD")

#### Использование next() для получения транзакций по одной
print(next(usd_transactions))  # Первая USD транзакция
print(next(usd_transactions))  # Вторая USD транзакция

2. `transaction_descriptions()`
Возвращает итератор с описаниями транзакций
#### Пример использования
from generators import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"}
]

#### Получение итератора описаний
descriptions = transaction_descriptions(transactions)

#### Поочередное получение описаний
print(next(descriptions))  # "Перевод организации"
print(next(descriptions))  # "Перевод со счета на счет"
print(next(descriptions))  # "Перевод с карты на карту"

3. `card_number_generator()`
Генерирует номера банковских карт в заданном диапазоне
#### Пример использования
from generators import card_number_generator

#### Генерация первых 5 номеров карт
for card_number in card_number_generator(1, 5):
    print(card_number)

Результат:

0000 0000 0000 0001

0000 0000 0000 0002

0000 0000 0000 0003

0000 0000 0000 0004

0000 0000 0000 0005

#### Генерация конкретного диапазона
for card_number in card_number_generator(1234567890123456, 1234567890123458):
    print(card_number)

Результат:

1234 5678 9012 3456

1234 5678 9012 3457

1234 5678 9012 3458

## Дополнительные возможности
### Поиск операций по описанию

`filter_by_description()` - позволяет фильтровать транзакции по ключевым словам в описании
#### Пример использования:
from src.processing import filter_by_description

operations = [
    {"description": "Перевод организации"},
    {"description": "Оплата услуг"},
    {"description": "Перевод другу"}
]

Поиск операций с "перевод" в описании
result = filter_by_description(operations, "перевод")
Результат: 2 операции

`count_operations_by_category` - подсчитывает количество операций по заданным категориям
#### Пример использования:
from src.processing import count_operations_by_category

operations = [
    {"description": "Перевод организации"},
    {"description": "Оплата услуг"},
    {"description": "Перевод другу"},
    {"description": "Оплата налогов"}
]

categories = ["Перевод", "Оплата", "Пополнение"]
result = count_operations_by_category(operations, categories)
Результат: {"Перевод": 2, "Оплата": 2, "Пополнение": 0}

# Разработка
Проект находится в активной разработке.

# Тестирование
## Установка Pytest
Если Pytest еще не установлен, установите его с помощью poetry:
`poetry add --group dev pytest`

Запустите тесты используя команду `pytest`

## Структура тестов
Тесты организованы в соответствии со структурой проекта - находятся в папке 'tests'.

Каждый тестовый файл соответствует отдельному модулю и содержит:
+ Фикстуры (fixtures) для подготовки тестовых данных

+ Тестовые функции с префиксом test_

+ Параметризованные тесты для проверки различных сценариев

+ Тесты обработки ошибок с использованием pytest.raises

## Покрытие тестами
В pytest для анализа покрытия кода надо поставить библиотеку 
pytest-cov:

`# Через poetry с добавлением в отдельную группу
poetry add --group dev pytest-cov`

Чтобы запустить тесты с оценкой покрытия, можно воспользоваться следующими командами:

+ `pytest --cov` — при активированном виртуальном окружении.
+ `poetry run pytest --cov` — через poetry.
+ `pytest --cov=src --cov-report=html` — чтобы сгенерировать отчет о покрытии в HTML-формате, где 
src — пакет c модулями, которые тестируем. Отчет будет сгенерирован в папке 
htmlcov и храниться в файле с названием index.html
