# Сервис для скоращения URL.

Данный сервис написан на языке **Python**.  
Использует framework **FastAPI**, СУБД **PostgreSQL** и несколько библиотек:

- **uvicorn** = "0.22.0"
- **fastapi** = "0.81"
- **envparse** = "0.2.0"
- **starlette** = "0.19.1"
- **pydantic** = "1.10.6"
- **anyio** = "3.7.0"
- **psycopg2-binary** = "2.9.9"
- **alembic** = "1.12.1"
- **asyncpg** = "0.28.0"

## Запуск приложения:

- _Предварительно на компьютер должен быть установлен Docker_

В директории, где находится Dockerfile, запустить в консоли:

```sh
docker compose up -d
```

Во время запуска устанавливаются все настройки и утилиты в систему,  
устанавливаются все зависимости в poetry,  
запускается База Данных, pgAdmin, приложение Salary-service, и выполняются миграции в alembic_migrations

## Описание работы приложения

### Url-abbreviation

После запуска её можно открыть по ссылке <http://0.0.0.0:8080>.  
Для запуска Swagger UI, после запуска приложения, нужно в адресной строке дописать: `/docs`

#### create_url

Принимает на вход ссылку, создаёт хэш, сохраняет в ссылку и хэщ в БД, на выход выдаёт {'short_url': 'http://0.0.0.0:8080/short/<хэш>'}

#### read_url

Выдаёт всю информацию из БД по хэшу.

#### update_url

Принимает на вход хэш, находит его в БД и меняет на новый.

#### delete

Принимает на вход хэш, удаляет всю строку из БД.

#### redirect_to_long_url

Перенаправляет пользователя, который ввёл в адресной строке http://0.0.0.0:8080/short/<хэш>, на ссылку, которая сохранена в БД с этим хэшем.
