from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from settings import (
    CURRENT_TIME,
    CITY_NAME,
    WEATHER_CONDITION,
    TEMPERATURE,
    TEMPERATURE_FEELS,
    CELSIUS,
    WIND_SPEED,
    MS,
)


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
            f"\n{CURRENT_TIME}{self.present_time}\n{CITY_NAME}{self.city_name}\n"
            f"{WEATHER_CONDITION}{self.weather}\n{TEMPERATURE}{self.temp}{CELSIUS}\n"
            f"{TEMPERATURE_FEELS}{self.temp_feels}{CELSIUS}\n"
            f"{WIND_SPEED}{self.speed_wind}{MS}\n"
        )


class Weather:
    def time_conversion(self, time_utc: int, shift_utc: int) -> str:
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

    def __init__(self, response: dict) -> None:
        self.city_name = response.get("name")
        self.weather = response.get("weather")[0].get("description")
        self.temp = response.get("main").get("temp")
        self.temp_feels = response.get("main").get("feels_like")
        self.speed_wind = response.get("wind").get("speed")
        self.present_time = self.time_conversion(
            response.get("dt"), response.get("timezone")
        )

    def __str__(self) -> str:
        return (
            f"\n{CURRENT_TIME}{self.present_time}\n{CITY_NAME}{self.city_name}\n"
            f"{WEATHER_CONDITION}{self.weather}\n{TEMPERATURE}{self.temp}{CELSIUS}\n"
            f"{TEMPERATURE_FEELS}{self.temp_feels}{CELSIUS}\n"
            f"{WIND_SPEED}{self.speed_wind}{MS}\n"
        )
