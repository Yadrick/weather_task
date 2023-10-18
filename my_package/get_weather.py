import requests


API_KEY = "bbeae2106b4b784ac7fc75027c4886b3"
URL_FOR_DATA_NAME = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
URL_FOR_DATA_COORDS = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"


def get_weather_by_lat_lon(lat: float, lon: float) -> dict:

    try:
        data_from_api = requests.get(URL_FOR_DATA_COORDS.format(lat, lon, API_KEY)).json()
    except (requests.exceptions.ReadTimeout, ValueError) as e:
        print(f'\nОбнаружена ошибка!\n{e}')
        return None

    required_data_from_api = {
        "city_name": data_from_api.get("name"),
        "weather": data_from_api.get("weather")[0].get("description"),
        "temp": round(data_from_api.get("main").get("temp")-273.15, 1),
        "temp_feels": round(data_from_api.get("main").get("feels_like")-273.15, 1),
        "speed_wind": data_from_api.get("wind").get("speed"),
        "time_utc": data_from_api.get("dt"),
        "shift_utc": data_from_api.get("timezone"),
    }
    
    return required_data_from_api


def get_weather_by_region_name(city_name: str) -> dict:
    
    try:
        data_for_lat_and_lon = requests.get(URL_FOR_DATA_NAME.format(city_name, API_KEY)).json()
        
        lat = data_for_lat_and_lon.get("coord").get("lat")
        lon = data_for_lat_and_lon.get("coord").get("lon")
        # коорды общаги))
        # lat = 59.986047
        # lon = 30.3458
        required_data = get_weather_by_lat_lon(lat, lon)

        return required_data
    except (requests.exceptions.ReadTimeout, ValueError) as e:
        print(f'\nОбнаружена ошибка!\n{e}')
        return None
    except Exception:
        print("Данного города нет в базе данных:(")
        return None
