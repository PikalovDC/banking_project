def get_mask_card_number() -> str:
    """
    Запрашивает номер карты, проверяет, что введены только цифры,
    и возвращает маску номера в формате XXXX XX** **** XXXX.
    """

    while True:
        card_number = input("Введите номер карты (16 цифр без пробелов):").strip()

        # Проверяем, что строка состоит только из цифр и имеет длину в 16 символов
        if card_number.isdigit() and len(card_number) == 16:
            break
        print("Ошибка! Номер карты должен состоять из 16 цифр. Попробуйте ещё раз.")

    # Берем первые 6 и последние 4 цифры
    first_part = card_number[:6]
    last_part = card_number[-4:]
    mask = f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"
    return mask


def get_mask_account() -> str:
    """
    Запрашивает номер счета, проверяет, что введены только цифры,
    и возвращает маску номера в формате **XXXX.
    """

    while True:
        account_number = input("Введите номер счета (20 цифр без пробелов):").strip()

        # Проверяем, что строка состоит только из цифр и имеет длину в 20 символов
        if account_number.isdigit() and len(account_number) == 20:
            break
        print("Ошибка! Номер счета должен состоять из 20 цифр. Попробуйте ещё раз.")

    account_mask = f"**{account_number[-4:]}"
    return account_mask
