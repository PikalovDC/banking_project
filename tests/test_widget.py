import pytest

from src.widget import get_date, mask_account_card


# Тесты для mask_account_card
@pytest.mark.parametrize("input_data, expected", [
    ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Maestro 9876543210987654", "Maestro 9876 54** **** 7654"),
    ("МИР 1111222233334444", "Мир 1111 22** **** 4444"),
])
def test_mask_account_card_different_types(input_data, expected):
    """Тест распознавания разных типов карт и счетов"""
    assert mask_account_card(input_data) == expected


def test_mask_account_card_invalid_input():
    """Тест обработки некорректных входных данных"""
    # Недостаточно данных
    with pytest.raises(ValueError):
        mask_account_card("Visa")

    # Только номер без типа
    with pytest.raises(ValueError):
        mask_account_card("1234567890123456")


def test_mask_account_card_case_insensitive():
    """Тест чувствительности к регистру"""
    result1 = mask_account_card("СЧЕТ 12345678901234567890")
    result2 = mask_account_card("счет 12345678901234567890")
    result3 = mask_account_card("Счет 12345678901234567890")

    assert "**7890" in result1
    assert "**7890" in result2
    assert "**7890" in result3


# Тесты для get_date
@pytest.mark.parametrize("input_date, expected", [
    ("2025-03-11T02:26:18.671407", "11.03.2025"),
    ("2025-12-31T23:59:59.999999", "31.12.2025"),
    ("2026-01-01T00:00:00.000000", "01.01.2026"),
])
def test_get_date_valid_formats(input_date, expected):
    """Тест правильности преобразования даты"""
    assert get_date(input_date) == expected


def test_get_date_invalid_formats():
    """Тест обработки некорректных форматов даты"""
    invalid_dates = [
        "invalid-date",  # не формат даты
        "2024-13-45T25:61:99.999999",  # несуществующая дата/время
        "",  # пустая строка
        "just-text",  # произвольный текст
        "2024-02-30T12:00:00.000000",  # 30 февраля
    ]

    for invalid_date in invalid_dates:
        with pytest.raises(ValueError):
            get_date(invalid_date)


def test_get_date_leap_year():
    """Тест високосного года"""
    assert get_date("2024-02-29T12:00:00.000000") == "29.02.2024"
