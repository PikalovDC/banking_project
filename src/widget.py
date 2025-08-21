from masks import get_mask_card_number, get_mask_account
from datetime import datetime

def mask_account_card(bank_data: str = None) -> str:

    if bank_data is None:

        bank_data = input("Введите тип карты (Visa, Master Card) и номер карты или 'Счет' и его номер:").strip()


    # Разделяем строку на слова
    input_data = bank_data.split()
    if len(input_data) < 2:
        raise ValueError("Строка должна содержать тип и номер (например: 'Visa Platinum 1234567890123456')")

    # Извлекаем номер (последнюю часть входных данных)
    number = input_data[-1]

    # Определяем тип данных по первому слову/словам (переведем все слова в нижний регистр)
    data_type = " ".join(input_data[: -1]).lower()

    # Проверяем, это счет или карта
    if "счет" in data_type:
        # Это счет, используем функцию get_mask_account()
        masked_number = get_mask_account(number)
        return f"{' '.join(input_data[: -1]).title()} {masked_number}"
    else:
        # Это карта, используем get_mask_card_number()
        masked_number = get_mask_card_number(number)
        return f"{' '.join(input_data[: -1]).title()} {masked_number}"


def get_date(input_date: str) -> str:
    # Здесь на вход подается дата в формате "2024-03-11T02:26:18.671407"
    # Парсим исходную дату

    try:
        date_only = datetime.fromisoformat(input_date)

    # Форматируем в нужный формат
        return date_only.strftime("%d.%m.%Y")

    #Добавил блок обработки ошибок на случай некорректного формата даты
    except ValueError:
        raise ValueError("Неверный формат даты. Ожидается формат: '2024-03-11T02:26:18.671407'")

print(get_date("2024-03-11T02:26:18.671407"))