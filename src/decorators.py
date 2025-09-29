from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
       Декоратор для логирования выполнения функций.

       Args:
           filename: Имя файла для записи логов. Если None - вывод в консоль.

       Returns:
           Декорированную функцию
       """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            func_name = func.__name__

            try:
                # Выполняется функция
                result = func(*args, **kwargs)

                # Сообщение об успешном выполнении функции
                log_message = f'{func_name} ok\n'

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)

                else:
                    print(log_message)

                return result

            except Exception as e:

                # Формируем сообщение об ошибке
                error_message = (
                    f'{func_name} error: {type(e).__name__}. '
                    f'Inputs: {args}, {kwargs}\n'
                )

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_message)

                else:
                    print(error_message)

                raise

        return wrapper
    return decorator
