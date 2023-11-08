"""Настройки и переменные окружения."""
from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    'REAL_DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@postgres:5432/postgres'
)

BASE_URL = env.str('BASE_URL', default='http://localhost:8080')
APP_HOST = env.str('APP_HOST', default='0.0.0.0')
APP_PORT = env.int('APP_PORT', default=8080)

HASH_LENGTH = env.int('HASH_LENGTH', default=6)