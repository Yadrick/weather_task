from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import StrEnum
from typing import Iterator, NamedTuple
import requests
import geocoder
import sqlite3 as sq
from clear_screen import clear


API_KEY = "bbeae2106b4b784ac7fc75027c4886b3"
URL_FOR_DATA_NAME = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
MENU_TEXT = """
[1] Узнать погоду в городе (по названию)
[2] Узнать погоду по моему местоположению
[3] Узнать историю запросов
[4] Удалить историю запросов

[0] Закрыть программу
"""

NAME_DATABASE = "data_weather.db"
NAME_TABLE = "user_weather_data"
NAME_SUPPORTING_TABLE = "sqlite_sequence"


@dataclass
class WeatherReading:
    record_number: int
    city_name: str
    weather: str
    temp: float
    temp_feels: float
    speed_wind: float
    present_time: str

    def __str__(self) -> str:
        return (
            f"\nТекущее время: {self.present_time}\nНазвание города: {self.city_name}\n"
            f"Погодные условия: {self.weather}\nТекущая температура: {self.temp} градусов по цельсию\n"
            f"Ощущается как: {self.temp_feels} градусов по цельсию\n"
            f"Скорость ветра: {self.speed_wind} м/c\n"
        )


class Weather:
    def __init__(self, response: dict) -> None:
        self.city_name = response.get("name")
        self.weather = response.get("weather")[0].get("description")
        self.temp = response.get("main").get("temp")
        self.temp_feels = response.get("main").get("feels_like")
        self.speed_wind = response.get("wind").get("speed")
        self.present_time = time_conversion(
            response.get("dt"), response.get("timezone")
        )

    def __str__(self) -> str:
        return (
            f"Текущее время: {self.present_time}\nНазвание города: {self.city_name}\n"
            f"Погодные условия: {self.weather}\nТекущая температура: {self.temp} градусов по цельсию\n"
            f"Ощущается как: {self.temp_feels} градусов по цельсию\n"
            f"Скорость ветра: {self.speed_wind} м/c"
        )


def time_conversion(time_utc: int, shift_utc: int) -> str:
    """
    Функция получает время в utc с сервера, переводит его в требуемый по ТЗ формат

    Args:
        time_utc(int): время в формате utc
        shift_utc(int): часовой пояс в формате utc

    Returns:
        str: Преобразованное время в формате: 2023-10-03 09:48:47+03:00
    """
    present_shift_hours = datetime.utcfromtimestamp(shift_utc).hour
    present_shift_minutes = datetime.utcfromtimestamp(shift_utc).minute

    present_time = datetime.fromtimestamp(
        time_utc - shift_utc,
        tz=timezone(
            timedelta(hours=present_shift_hours, minutes=present_shift_minutes)
        ),
    )
    return str(present_time)


# Можно message из классов ошибок вынести в отдельный файл, и инициализировать прямо в init,
# не епередавая при ловле исключения


class GeocoderException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RequestsExceptionNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RequestsExceptionConnection(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RequestsExceptionUnexpectedError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ExitProgramException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DatabaseException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


# class NoActionException(Exception):
#     def __init__(self, message: str) -> None:
#         super().__init__(message)


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
    create_db_weather(connect)
    yield connect
    connect.close()


def create_db_weather(connection: sq.Connection) -> None:
    cur = connection.cursor()
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {NAME_TABLE} (
        record_number INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT,
        weather TEXT,
        temp REAL,
        temp_feels REAL,
        speed_wind REAL,
        present_time TEXT
        )"""
    )


def drop_table_weather(connection: sq.Connection) -> None:
    try:
        cur = connection.cursor()
        cur.execute(f"DELETE FROM {NAME_TABLE}")
        cur.execute(f"DELETE FROM {NAME_SUPPORTING_TABLE}")
        connection.commit()
        print("Данные успешно удалены!")
    except Exception:
        raise DatabaseException("У нас пролемы с базами данных. Уже решаем!")


def insert_weather_data(data_weather_object: Weather, connection: sq.Connection):
    try:
        cur = connection.cursor()
        cur.execute(
            f"""INSERT INTO {NAME_TABLE}
                    (city_name, weather, temp, temp_feels, speed_wind, present_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
            (
                data_weather_object.city_name,
                data_weather_object.weather,
                data_weather_object.temp,
                data_weather_object.temp_feels,
                data_weather_object.speed_wind,
                data_weather_object.present_time,
            ),
        )
        connection.commit()
    except Exception:
        raise DatabaseException("У нас пролемы с базами данных. Уже решаем!")


def processing_data_from_db(weather_data_list: list[tuple]) -> list[WeatherReading]:
    """
    Функция получает данные о погоде в виде списка кортежей. Возвращает список именнованных кортежей.

    Args:
        weather_data_list(list[tuple])): список данных о погоде

    Returns:
        list[WeatherReading] - возвращает список обьектов погоды для чтения.

    Raises:
        None
    """
    list_weather_object = []

    for weather_data_tuple in weather_data_list:
        weather_data = WeatherReading(*weather_data_tuple)

        list_weather_object.append(weather_data)

    return list_weather_object


def read_weather_data(
    count_records_output: int, connection: sq.Connection
) -> list[WeatherReading]:
    """
    Функция получает данные из Базы Данных в количестве {count_records_output} последних штук.
    Если данных меньше, чем {count_records_output}, то вернутся просто все имеющиееся данные.

    Args:
        count_records_output(int): количество строк, необходимое для просмотра пользователю
        connection(sq.Connection): соединение с БД

    Returns:
        list[WeatherNamedTuple] - возвращает список именнованных кортежей, полученных из метода processing_data_from_db().

    Raises:
        DatabaseException: на случай ошибок во время работы с Базой Данных.
    """
    cur = connection.cursor()
    try:
        cur.execute(
            f"SELECT * FROM {NAME_TABLE} ORDER BY record_number DESC LIMIT {count_records_output}"
        )
        result = cur.fetchall()
        return processing_data_from_db(result)
    except Exception:
        raise DatabaseException("У нас проблемы с базами данных. Уже решаем!")


def max_counts_weather_data(connection: sq.Connection) -> int:
    cur = connection.cursor()
    try:
        max_counts = cur.execute(f"SELECT seq FROM {NAME_SUPPORTING_TABLE}").fetchone()[
            0
        ]
        return max_counts
    except Exception:
        raise DatabaseException("У нас пролемы с базами данных. Уже решаем!")


def data_processing(response: dict, connection: sq.Connection) -> None:
    """
    Функция создает объект Погоды, после чего выводит его строковое представление.
    Передает объект в функцию сохранения.

     Args:
        response(dict): необработанные данные с сервера
        connection(sq.Connection): соединение с БД

    Returns:
        None

    """
    data_from_api_object = Weather(response)
    print(data_from_api_object)
    insert_weather_data(data_from_api_object, connection)


def get_data_from_api(city_name: str, connection: sq.Connection):
    """
    Функция получает данные с API. После чего передает их на обработку.

    Args:
        city_name(str): название города, которое вводит пользователб

    Returns:
        None

    Raises:
        RequestsExceptionNotFound: выбрасывается когда сервер не понимает запроса. Например, несуществующий город

        RequestsExceptionConnection: выбрасывается, когда превышается время ожидания ответа от сервера.
        Или какие-то проблемы с соединением

        RequestsExceptionUnexpectedError: на случай непредвиденных ошибок
    """
    try:
        response = requests.get(
            URL_FOR_DATA_NAME.format(city_name, API_KEY),
            params={"units": "metric", "lang": "ru"},
            timeout=3,
        )
        response.raise_for_status()
        data_processing(response.json(), connection)

    except requests.exceptions.HTTPError:
        raise RequestsExceptionNotFound("Запрашиваемый город не найден.")
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        raise RequestsExceptionConnection(
            "Превышено время ожидания ответа. Попробуйте позже."
        )
    except Exception:
        raise RequestsExceptionUnexpectedError(
            "Произошла непредвиденная ошибка. Попробуйте позже."
        )


def find_current_location() -> str:
    """
    Функция определяет текущее еместоположение по ip пользователя.

    Args:
        None

    Returns:
        str: возвращает название города текущего местоположения

    Raises:
        GeocoderException: сообщает пользователю об ошибке при попытке получить текущее местоположение
    """
    try:
        return geocoder.ip("me").city
    except Exception:
        raise GeocoderException(
            "Не удалось определить ваше местоположение, попробуйте позже"
        )


def get_weather_by_city_name(connection: sq.Connection) -> None:
    """
    Функция запрашивает название города у пользователя и передает его в функцию по получению данных с сервера.

    Args:
        None

    Returns:
        None
    """
    city_name = input("Введите название города: ").strip()
    get_data_from_api(city_name, connection)
    input("Чтобы продолжить, введите что угодно :)")


def get_weather_by_location(connection: sq.Connection) -> None:
    """
    Функция получает данные о текущем местоположении и передает его в функцию по получению данных с сервера.

    Args:
        None

    Returns:
        None
    """
    city_name = find_current_location()
    get_data_from_api(city_name, connection)
    input("Чтобы продолжить, введите что угодно :)")


def find_requests_history(connection: sq.Connection):
    count_records = input(
        "Сколько последних записей вы хотите увидеть?\n"
        "(при введении большего числа записей, чем имеется, покажется максимальное количество)\n "
    )
    try:
        list_weather_object = read_weather_data(int(count_records), connection)

        for weather_object in list_weather_object:
            print(weather_object)
        input("\nЧтобы продолжить, введите что угодно :)")
    except ValueError:
        print("Ошибка! Это не число :(")
    except Exception:
        raise DatabaseException("У нас пролемы в работе с базами данных. Уже решаем!")


class ActionType(StrEnum):
    CLOSE_PROGRAMM = "0"
    GET_WEATHER_BY_CITY_NAME = "1"
    GET_WEATHER_BY_LOCATION = "2"
    FIND_REQUESTS_HISTORY = "3"
    DELETE_QUERY_HISTORY = "4"


def close_program(connection: sq.Connection):
    raise ExitProgramException("To be continued.")


actions_map = {
    ActionType.CLOSE_PROGRAMM: close_program,
    ActionType.GET_WEATHER_BY_CITY_NAME: get_weather_by_city_name,
    ActionType.GET_WEATHER_BY_LOCATION: get_weather_by_location,
    ActionType.FIND_REQUESTS_HISTORY: find_requests_history,
    ActionType.DELETE_QUERY_HISTORY: drop_table_weather,
}


def main():
    clear()
    with sqlite_connection(NAME_DATABASE) as connect:
        while True:
            print(MENU_TEXT)
            action_number = input("Выберите пункт меню: ").strip()
            clear()

            try:
                action_type = ActionType(action_number)
                action = actions_map.get(action_type)
                action(connect)
            except ExitProgramException as ex:
                print(ex)
                break
            except ValueError:
                print(
                    "Данного действия не существует. Пожалуйста, выберите что-то из списка."
                )
            except Exception as ex:
                print(ex)


if __name__ == "__main__":
    main()

# get_data_from_api("Москва")
