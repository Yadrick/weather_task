from contextlib import contextmanager
from typing import Iterator
import sqlite3 as sq


@contextmanager
def sqlite_connection(name_db: str) -> Iterator[sq.Connection]:
    """
    Функция использует декоратор contextmanager для создания контекстногго менеджера для работы с БД sqlite3.
    Запускает функцию create_db_weather() для создания БД (если её еще нет)

    Args:
        name_db(str): название базы данных

    Yield:
        Iterator[sq.Connection] - Обьект соединения с базой даных

    """
    connect = sq.connect(name_db)
    yield connect
    connect.close()
