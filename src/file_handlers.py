import csv
import logging
import os
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger('file_handlers')


def load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из CSV-файла.
    """
    logger.info(f"Начало загрузки транзакций из CSV файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"CSV файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        logger.error(f"CSV файл пустой: {file_path}")
        return []

    transactions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')

            for row_num, row in enumerate(csv_reader, 1):
                try:
                    # Пропускаем пустые ID
                    if not row.get('id') or not row['id'].strip():
                        continue

                    transaction = {
                        'id': int(row['id']),
                        'state': row.get('state', ''),
                        'date': row.get('date', ''),
                        'operationAmount': {
                            'amount': row.get('amount', '0'),
                            'currency': {
                                'name': row.get('currency_name', ''),
                                'code': row.get('currency_code', 'RUB')
                            }
                        },
                        'description': row.get('description', ''),
                        'from': row.get('from') or None,
                        'to': row.get('to', '')
                    }
                    transactions.append(transaction)

                except (ValueError, KeyError) as e:
                    logger.warning(f"Ошибка в строке {row_num}: {e}")
                    continue

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при загрузке CSV файла: {e}")
        return []


def load_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из Excel-файла.
    """
    logger.info(f"Начало загрузки транзакций из Excel файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Excel файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        logger.error(f"Excel файл пустой: {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        transactions = []

        for index, row in df.iterrows():
            try:
                # Пропускаем пустые ID
                if pd.isna(row.get('id')):
                    continue

                transaction = {
                    'id': int(row['id']),
                    'state': str(row.get('state', '')),
                    'date': str(row.get('date', '')),
                    'operationAmount': {
                        'amount': str(row.get('amount', '0')),
                        'currency': {
                            'name': str(row.get('currency_name', '')),
                            'code': str(row.get('currency_code', 'RUB'))
                        }
                    },
                    'description': str(row.get('description', '')),
                    'from': str(row['from']) if pd.notna(row.get('from')) else None,
                    'to': str(row.get('to', ''))
                }
                transactions.append(transaction)

            except (ValueError, KeyError) as e:
                logger.warning(f"Ошибка в строке {index + 1}: {e}")
                continue

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel файла: {e}")
        return []
