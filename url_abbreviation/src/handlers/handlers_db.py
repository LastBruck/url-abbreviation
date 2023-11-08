"""Обработчики БД."""
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ShortUrl


async def save_new_url(long_url: str, hash_url: str, session: AsyncSession):
    """Сохранение URl ссылки и хэш в таблицу БД.

    Args:
        long_url (str): длинная ссылка
        hash_url (str): хэш
        session (AsyncSession): БД
    """
    async with session.begin():
        urls = ShortUrl(
            long_url=long_url,
            hash=hash_url,
        )
        session.add(urls)
        await session.flush()


async def get_info_by_long_url(long_url: str, session: AsyncSession):
    """Получение информации всей строки из таблицы БД по колонке long_url.

    Args:
        long_url (str): длинная ссылка
        session (AsyncSession): БД

    Returns:
        _type_: _description_
    """
    async with session.begin():
        query = select(ShortUrl).where(ShortUrl.long_url == long_url)
        res = await session.execute(query)
        urls_row = res.fetchone()
        if urls_row is not None:
            return urls_row[0]


async def get_info_by_hash(hash_url: str, session: AsyncSession):
    """Получение информации всей строки из таблицы БД по колонке hash.

    Args:
        hash_url (str): хэш
        session (AsyncSession): БД

    Returns:
        _type_: _description_
    """
    async with session.begin():
        query = select(ShortUrl).where(ShortUrl.hash == hash_url)
        res = await session.execute(query)
        urls_row = res.fetchone()
        if urls_row is not None:
            return urls_row[0]


async def delete_info_by_hash(hash_url: str, session: AsyncSession):
    """Удаление всей строки из таблицы БД по колонке hash.

    Args:
        hash_url (str): хэш
        session (AsyncSession): БД
    """
    async with session.begin():
        query = delete(ShortUrl).where(ShortUrl.hash == hash_url)
        await session.execute(query)
        await session.commit()


async def update_hash_by_hash(hash_url: str, new_hash: str, session: AsyncSession):
    """Обновление значения в столбце hash из таблицы БД в строке по колонке hash.

    Args:
        hash_url (str): старый хэш
        new_hash (str): новый хэш
        session (AsyncSession): БД
    """
    async with session.begin():
        card_to_update = await session.execute(select(ShortUrl).filter_by(hash=hash_url))
        card_to_update = card_to_update.scalar_one_or_none()
        if card_to_update:
            card_to_update.hash = new_hash
            await session.commit()
