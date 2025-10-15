import logging
import os
from pathlib import Path


def setup_logging():
    """Настройка логирования для всего проекта"""

    # Создаем папку logs в корне проекта
    log_dir = Path("..") / "logs"  # ../logs из папки src
    log_dir.mkdir(exist_ok=True)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Конфигурация логгера для модуля masks
    masks_logger = logging.getLogger('masks')
    masks_logger.setLevel(logging.DEBUG)

    # File handler для masks (путь ../logs/masks.log)
    masks_file_handler = logging.FileHandler('../logs/masks.log', mode='w', encoding='utf-8')
    masks_file_handler.setFormatter(formatter)
    masks_logger.addHandler(masks_file_handler)

    # Конфигурация логгера для модуля utils
    utils_logger = logging.getLogger('utils')
    utils_logger.setLevel(logging.DEBUG)

    # File handler для utils (путь ../logs/utils.log)
    utils_file_handler = logging.FileHandler('../logs/utils.log', mode='w', encoding='utf-8')
    utils_file_handler.setFormatter(formatter)
    utils_logger.addHandler(utils_file_handler)
