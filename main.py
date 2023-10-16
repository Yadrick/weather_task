import requests
from datetime import timedelta, timezone, datetime


API_KEY = "e64b43795e646238889944a550c9bbb4"
MAKE_API_CALL = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}"
URL_FOR_DATA = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"

MENU_TEXT = '''
[1] Узнать погоду в городе (по названию / широте и долготе)
[2] Узнать погоду по моему местоположению
[3] Посмотреть историю запросов

[0] Закрыть программу
'''


def get_weather_by_lat_lon(lat: int, lon: int) -> dict:

    data_from_api = requests.get(URL_FOR_DATA.format(lat, lon, API_KEY)).json()

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

    data_for_lat_and_lon = requests.get(MAKE_API_CALL.format(city_name, API_KEY)).json()[0]

    lat = data_for_lat_and_lon.get("lat")
    lon = data_for_lat_and_lon.get("lon")
    # коорды общаги))
    # lat = 59.986047
    # lon = 30.3458
    required_data = get_weather_by_lat_lon(lat, lon)
    # time_ours_days = datetime.utcfromtimestamp(time_utc + shift_utc)

    return required_data


def information_output_template(data: dict):

    hours_shift = datetime.utcfromtimestamp(data.get("shift_utc")).hour
    minutes_shift = datetime.utcfromtimestamp(data.get("shift_utc")).minute
    timezone_1 = timezone(timedelta(hours=hours_shift, minutes=minutes_shift))
    dt_object = datetime.fromtimestamp(data.get("time_utc"), timezone_1)

    template = f'''
    \nТекущее время: {dt_object}\nНазвание города: {data.get("city_name")}\n\
Погодные условия: {data.get("weather")}\nТекущая температура: {data.get("temp")} градусов по цельсию\n\
Ощущается как: {data.get("temp_feels")} градусов по цельсию \n\
Скорость ветра: {data.get("speed_wind")} м/c
'''

    print(template)


# def get_info_by_ip(ip='127.0.0.1'):
#     try:
#         response = requests.get(url=f'http://ip-api.com/json/{ip}').json()

#         data = {
#             'latitude:': response.get('lat'),
#             'longitude:': response.get('lon'),
#         }

#         print(data)
#     except requests.exceptions.ConnectionError:
#         print("[!] Please check your connection!")

#     return data


def main():
    # ip = input("Пожалуйста, введите IP adress: ")
    program_work = True
    while True:
        if program_work:
            print(MENU_TEXT)

        action_number = input("Выберите пункт меню: ")

        if not int(action_number):
            break


# В return_button можно прикольюхи вставить, чтобы при введении любых слов, символов и тп,
# в ответ пользователь получал прикольное сообщение))

        try:
            while True:

                if action_number in "01":
                    city_name = input("\nВведите название города: ")
                    data_weather = get_weather_by_region_name(city_name)
                    information_output_template(data_weather)
                
                    return_button = input('Для возврата в меню введите "r".\nЧтобы продолжить узнавать погоду, введите что угодно :)')
                
                if return_button == 'r':
                    break
        except ValueError:
            print("ошибка")

    # get_info_by_ip(ip=ip)


if __name__ == '__main__':
    main()
