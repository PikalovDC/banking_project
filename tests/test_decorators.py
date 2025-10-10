import os
import tempfile
from typing import Any

import pytest

from src.decorators import log

"""Тесты для декоратора log"""


# Тесты для логирования в консоль
def test_log_to_console_success(capsys):
    """Тест успешного выполнения с выводом в консоль"""

    @log()
    def test_function(x: int, y: int) -> int:
        return x + y

    result = test_function(5, 3)

    # Проверяем что функция работает корректно
    assert result == 8

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "test_function ok" in captured.out


def test_log_to_console_error(capsys):
    """Тест ошибки с выводом в консоль"""

    @log()
    def failing_function(a: int, b: int) -> float:
        return a / b

    # Проверяем что исключение пробрасывается
    with pytest.raises(ZeroDivisionError):
        failing_function(10, 0)

    # Проверяем вывод ошибки в консоль
    captured = capsys.readouterr()
    assert "failing_function error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out
    assert "{}" in captured.out  # Проверяем пустые kwargs


def test_log_to_console_with_kwargs(capsys):
    """Тест с ключевыми аргументами"""

    @log()
    def function_with_kwargs(x: int, y: int = 5, z: int = 10) -> int:
        return x + y + z

    result = function_with_kwargs(1, y=2, z=3)
    assert result == 6

    captured = capsys.readouterr()
    assert "function_with_kwargs ok" in captured.out


# Тесты для логирования в файл
def test_log_to_file_success():
    """Тест успешного выполнения с записью в файл"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        temp_filename = f.name

    try:
        @log(filename=temp_filename)
        def test_function(x: str, y: str) -> str:
            return x + y

        result = test_function("Hello, ", "World!")
        assert result == "Hello, World!"

        # Проверяем запись в файл
        with open(temp_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "test_function ok" in content
            assert "error" not in content

    finally:
        os.unlink(temp_filename)


def test_log_to_file_error():
    """Тест ошибки с записью в файл"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        temp_filename = f.name

    try:
        @log(filename=temp_filename)
        def failing_function(data: list, index: int) -> Any:
            return data[index]

        with pytest.raises(IndexError):
            failing_function([1, 2, 3], 10)

        # Проверяем запись ошибки в файл
        with open(temp_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "failing_function error: IndexError" in content
            assert "Inputs: ([1, 2, 3], 10)" in content

    finally:
        os.unlink(temp_filename)


# Тесты для различных типов исключений
def test_log_different_exception_types(capsys):
    """Тест логирования различных типов исключений"""

    @log()
    def value_error_func():
        raise ValueError("Custom error message")

    @log()
    def type_error_func():
        raise TypeError("Type mismatch")

    @log()
    def key_error_func():
        raise KeyError("Missing key")

    # Тестируем ValueError
    with pytest.raises(ValueError):
        value_error_func()
    captured = capsys.readouterr()
    assert "value_error_func error: ValueError" in captured.out

    # Тестируем TypeError
    with pytest.raises(TypeError):
        type_error_func()
    captured = capsys.readouterr()
    assert "type_error_func error: TypeError" in captured.out

    # Тестируем KeyError
    with pytest.raises(KeyError):
        key_error_func()
    captured = capsys.readouterr()
    assert "key_error_func error: KeyError" in captured.out


# Тесты для сохранения метаданных функции
def test_log_preserves_function_metadata():
    """Тест что декоратор сохраняет метаданные функции"""

    @log()
    def original_function(x: int, y: int) -> int:
        """Тестовая функция с документацией"""
        return x * y

    # Проверяем что метаданные сохранились
    assert original_function.__name__ == "original_function"
    assert "Тестовая функция с документацией" in original_function.__doc__
    assert original_function(3, 4) == 12


def test_log_empty_function(capsys):
    """Тест с функцией без аргументов"""

    @log()
    def empty_function() -> str:
        return "empty"

    result = empty_function()
    assert result == "empty"

    captured = capsys.readouterr()
    assert "empty_function ok" in captured.out
    assert "Inputs" not in captured.out  # Не должно быть Inputs для пустых аргументов


def test_log_with_none_result(capsys):
    """Тест функции возвращающей None"""

    @log()
    def none_function() -> None:
        return None

    result = none_function()
    assert result is None

    captured = capsys.readouterr()
    assert "none_function ok" in captured.out
