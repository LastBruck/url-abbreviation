"""Генератор строки."""
import random
import string

import settings


async def generate_hash():
    """Генерация сокращённой ссылки.

    Returns:
        str: сгенерированная строка
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(settings.HASH_LENGTH))
