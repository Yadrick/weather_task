from dataclasses import dataclass
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
class Weather:
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
