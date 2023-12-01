from enum import StrEnum


class ActionType(StrEnum):
    CLOSE_PROGRAMM = "0"
    GET_WEATHER_BY_CITY_NAME = "1"
    GET_WEATHER_BY_LOCATION = "2"
    FIND_REQUESTS_HISTORY = "3"
    DELETE_QUERY_HISTORY = "4"
