from ..classes.HistoryDBs import HistoryDB
from ..classes.Weathers import Weather
from ..classes.exceptions import (
    GeocoderException,
    RequestsExceptionNotFound,
    RequestsExceptionConnection,
    RequestsExceptionUnexpectedError,
)
from settings import API_KEY, URL_FOR_DATA_NAME
from settings import INPUT_CITY_NAME_TEXT
from datetime import datetime, timezone, timedelta

import requests
import geocoder


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
        time_utc,
        tz=timezone(
            timedelta(hours=present_shift_hours, minutes=present_shift_minutes)
        ),
    )
    return str(present_time)


def data_pre_processing(response: dict, storage__weather_history: HistoryDB) -> None:
    """
    Функция забирает нужные данные из ответа с API. Передает их на обработку.

     Args:
        response(dict): необработанные данные с сервера
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

    Returns:
        None

    """
    city_name = response.get("name")
    weather = response.get("weather")[0].get("description")
    temp = response.get("main").get("temp")
    temp_feels = response.get("main").get("feels_like")
    speed_wind = response.get("wind").get("speed")
    present_time = time_conversion(response.get("dt"), response.get("timezone"))
    response_tuple = (city_name, weather, temp, temp_feels, speed_wind, present_time)

    data_processing(response_tuple, storage__weather_history)


def data_processing(required_data: tuple, storage__weather_history: HistoryDB) -> None:
    """
    Функция создает объект Погоды, после чего выводит его строковое представление.
    Сохраняет в БД.

     Args:
        required_data(tuple): необработанные данные с сервера
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

    Returns:
        None

    """
    data_from_api_object = Weather(*required_data)
    print(data_from_api_object)
    storage__weather_history.insert_weather_data(data_from_api_object)


def get_data_from_api(city_name: str, storage__weather_history: HistoryDB) -> None:
    """
    Функция получает данные с API. После чего передает их на обработку.

    Args:
        city_name(str): название города, которое вводит пользователю
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

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
        data_pre_processing(response.json(), storage__weather_history)

    except requests.exceptions.HTTPError:
        raise RequestsExceptionNotFound()
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        raise RequestsExceptionConnection()
    except Exception:
        raise RequestsExceptionUnexpectedError()


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
        raise GeocoderException()


def get_weather_by_city_name(storage__weather_history: HistoryDB) -> None:
    """
    Функция запрашивает название города у пользователя и передает его в функцию по получению данных с сервера.

    Args:
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

    Returns:
        None
    """
    city_name = input(INPUT_CITY_NAME_TEXT).strip()
    get_data_from_api(city_name, storage__weather_history)


def get_weather_by_location(storage__weather_history: HistoryDB) -> None:
    """
    Функция получает данные о текущем местоположении и передает его в функцию по получению данных с сервера.

    Args:
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

    Returns:
        None
    """
    city_name = find_current_location()
    get_data_from_api(city_name, storage__weather_history)
