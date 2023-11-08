"""Main url-abbreviation service."""
import re

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

import settings
from session import get_session
from src.handlers.generator import generate_hash
from src.handlers.handlers_db import (delete_info_by_hash, get_info_by_hash,
                                      get_info_by_long_url, save_new_url,
                                      update_hash_by_hash)

app = FastAPI(title='url-abbreviation')


@app.post('/url/', status_code=201)
async def create_url(url: str, db: AsyncSession = Depends(get_session)):
    """Сокращение ссылки.

    Args:
        url (str): url
        db (AsyncSession): Depends(get_session).

    Raises:
        HTTPException: не прошла валидация URL

    Returns:
        dict: {'short_url': 'BASE_URL/short/hash_url'}
    """
    tpl = '^https?://[\w.-]+'
    if re.match(tpl, url) is None:
        raise HTTPException(status_code=400, detail='URL должен начинаться с http(s)://')
    urls_res = await get_info_by_long_url(long_url=url, session=db)
    if urls_res:
        old_hash = urls_res.hash
        return {'short_url': f'{settings.BASE_URL}/short/{old_hash}'}
    hash_url = await generate_hash()
    await save_new_url(long_url=url, hash_url=hash_url, session=db)
    return {'short_url': f'{settings.BASE_URL}/short/{hash_url}'}


@app.get('/url/{hash_url}')
async def read_url(hash_url: str, db: AsyncSession = Depends(get_session)):
    """Чтение ссылки.

    Args:
        hash_url (str): hash_url
        db (AsyncSession): Depends(get_session).

    Raises:
        HTTPException: URL не найден

    Returns:
        dict: {'id': 'url_id', 'long_url': 'long_url', 'short_url': 'short_url'}
    """
    urls_res = await get_info_by_hash(hash_url=hash_url, session=db)
    if urls_res is None:
        raise HTTPException(status_code=404, detail='URL не найден')
    url_id = urls_res.id
    long_url = urls_res.long_url
    short_url = f'{settings.BASE_URL}/short/{hash_url}'
    return {'id': url_id, 'long_url': long_url, 'short_url': short_url}


@app.put('/url/{hash_url}')
async def update_url(hash_url: str, db: AsyncSession = Depends(get_session)):
    """Обновление ссылки.

    Args:
        hash_url (str): hash_url
        db (AsyncSession): Depends(get_session).

    Raises:
        HTTPException: URL не найден

    Returns:
        dict: {'short_url': 'BASE_URL/short/hash_url'}
    """
    urls_res = await get_info_by_hash(hash_url=hash_url, session=db)
    if urls_res is None:
        raise HTTPException(status_code=404, detail='URL не найден')
    new_hash = await generate_hash()
    await update_hash_by_hash(hash_url=hash_url, new_hash=new_hash, session=db)
    return {'short_url': f'{settings.BASE_URL}/short/{new_hash}'}


@app.delete('/url/{hash_url}')
async def delete_url(hash_url: str, db: AsyncSession = Depends(get_session)):
    """Удаление ссылки.

    Args:
        hash_url (str): hash_url
        db (AsyncSession): Depends(get_session).

    Raises:
        HTTPException: URL не найден

    Returns:
        dict: {'message': 'hash_url delete'}
    """
    urls_res = await get_info_by_hash(hash_url=hash_url, session=db)
    if urls_res is None:
        raise HTTPException(status_code=404, detail='URL не найден')
    await delete_info_by_hash(hash_url=hash_url, session=db)
    return {'message': f'{hash_url} delete'}


@app.get('/short/{hash_url}')
async def redirect_to_long_url(hash_url: str, db: AsyncSession = Depends(get_session)):
    """Перевод на длинную ссылку.

    Args:
        hash_url (str): хэш
        db (AsyncSession): Depends(get_session).

    Raises:
        HTTPException: URL не найден

    Returns:
        RedirectResponse: редирект
    """
    urls_res = await get_info_by_hash(hash_url=hash_url, session=db)
    if urls_res is None:
        raise HTTPException(status_code=404, detail='URL не найден')
    long_url = urls_res.long_url
    return RedirectResponse(url=long_url, status_code=301)


@app.get('/healthz/ready')
async def ready(db: AsyncSession = Depends(get_session)):
    """ReadynessProbe.

    Args:
        db (AsyncSession): Depends(get_session).

    Raises:
        HTTPException: База Данных не доступна

    Returns:
        status_code: HTTP_200_OK
    """
    try:
        async with db as conn:
            async with conn.begin():
                result = await conn.execute(text('SELECT 1'))
                result.scalar()
        return HTTP_200_OK
    except Exception:
        raise HTTPException(status_code=503, detail='База Данных не доступна')


@app.get('/healthz/up')
async def up():
    """LivenessProbe.

    Returns:
        status_code: HTTP_200_OK
    """
    return HTTP_200_OK


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )
