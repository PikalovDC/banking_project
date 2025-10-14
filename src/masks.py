import logging

from src.logger_config import setup_logging

# Создан отдельный объект логера для модуля masks
logger = logging.getLogger('masks')


def get_mask_card_number(card_number: str | None = None) -> str:
    """
    Запрашивает номер карты, проверяет, что введены только цифры,
    и возвращает маску номера в формате XXXX XX** **** XXXX.
    """
    # Логирование успешного случая - вызов функции
    logger.info("Функция get_mask_card_number вызвана")

    if card_number is None:
        # Интерактивный режим (если номер не передан как аргумент в функцию)
        logger.debug("Запущен интерактивный режим для ввода номера карты")
        while True:
            card_number = input("Введите номер карты (16 цифр без пробелов):").strip()

            # Проверяем, что строка состоит только из цифр и имеет длину в 16 символов
            if card_number.isdigit() and len(card_number) == 16:
                # Логирование успешного случая - корректный ввод
                logger.info("Номер карты успешно введен пользователем")
                break
            # Логирование ошибочного случая - неверный ввод
            logger.warning(f"Неверный ввод номера карты: '{card_number}' (ожидается 16 цифр)")
            print("Ошибка! Номер карты должен состоять из 16 цифр. Попробуйте ещё раз.")

    # Номер передан как аргумент в функцию
    if not card_number.isdigit() or len(card_number) != 16:
        # Логирование ошибочного случая с уровнем ERROR
        error_msg = f"Некорректный номер карты: '{card_number}' (ожидается 16 цифр)"
        logger.error(error_msg)
        raise ValueError("Номер карты должен состоять из 16 цифр")

    # Берем первые 6 и последние 4 цифры
    first_part = card_number[:6]
    last_part = card_number[-4:]
    mask = f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"
    # Логирование успешного случая - результат работы функции
    logger.info(f"Сгенерирована маска карты: {mask}")
    return mask


def get_mask_account(account_number: str | None = None) -> str:
    """
    Запрашивает номер счета, проверяет, что введены только цифры,
    и возвращает маску номера в формате **XXXX.
    """
    # Логирование успешного случая - вызов функции
    logger.info("Функция get_mask_account вызвана")

    if account_number is None:

        # Интерактивный режим
        logger.debug("Запущен интерактивный режим для ввода номера счета")
        while True:
            account_number = input("Введите номер счета (20 цифр без пробелов):").strip()

            # Проверяем, что строка состоит только из цифр и имеет длину в 20 символов
            if account_number.isdigit() and len(account_number) == 20:
                # Логирование успешного случая - корректный ввод
                logger.info("Номер счета успешно введен пользователем")
                break
            # Логирование ошибочного случая - неверный ввод
            logger.warning(f"Неверный ввод номера счета: '{account_number}' (ожидается 20 цифр)")
            print("Ошибка! Номер счета должен состоять из 20 цифр. Попробуйте ещё раз.")

    # Прямая передача номера
    if not account_number.isdigit() or len(account_number) != 20:
        # Логирование ошибочного случая с уровнем ERROR
        error_msg = f"Некорректный номер счета: '{account_number}' (ожидается 20 цифр)"
        logger.error(error_msg)
        raise ValueError("Номер счета должен состоять из 20 цифр")

    account_mask = f"**{account_number[-4:]}"
    # Логирование успешного случая - результат работы функции
    logger.info(f"Сгенерирована маска счета: {account_mask}")
    return account_mask


setup_logging()
