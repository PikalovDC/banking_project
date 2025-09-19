import pytest

from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number():
    """Тест правильности маскирования номера карты"""
    assert get_mask_card_number("8888888888888888") == "8888 88** **** 8888"


def test_get_mask_card_number_different_lengths():
    """Обработка номеров карт разной длины"""

    # Тест на обработку слишком короткого номера карты
    with pytest.raises(ValueError):
        get_mask_card_number("123456789")

    # Тест на обработку слишком длинного номера карты
    with pytest.raises(ValueError):
        get_mask_card_number("12345678901234567890")


def test_get_mask_card_number_non_digits():
    """Тест обработки нечисловых входных данных"""
    with pytest.raises(ValueError):
        get_mask_card_number("1234abcd56789012")

    # Обработка пустой строки
    with pytest.raises(ValueError):
        get_mask_card_number("")


# Тесты для get_mask_account

def test_get_mask_account_valid():
    """Тест правильности маскирования номера счета"""
    assert get_mask_account("12345678901234567890") == "**7890"


def test_get_mask_account_different_lengths():
    """Тест обработки номеров счетов разной длины"""
    # Короткий номер
    with pytest.raises(ValueError):
        get_mask_account("1234567890")

    # Длинный номер
    with pytest.raises(ValueError):
        get_mask_account("123456789012345678901234")


def test_get_mask_account_non_digits():
    """Тест обработки нечисловых входных данных"""
    with pytest.raises(ValueError):
        get_mask_account("123456789abcdefghijk")


def test_get_mask_account_empty_string():
    """Тест обработки пустой строки"""
    with pytest.raises(ValueError):
        get_mask_account("")
