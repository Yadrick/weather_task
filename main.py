import requests
import geocoder
import my_package
from datetime import timedelta, timezone, datetime


MENU_TEXT = '''
[1] Узнать погоду в городе (по названию / широте и долготе)
[2] Узнать погоду по моему местоположению
[3] Посмотреть историю запросов

[0] Закрыть программу
'''


def information_output_template(data: dict):

    hours_shift = datetime.utcfromtimestamp(data.get("shift_utc")).hour
    minutes_shift = datetime.utcfromtimestamp(data.get("shift_utc")).minute
    timezone_1 = timezone(timedelta(hours=hours_shift, minutes=minutes_shift))
    dt_object = datetime.fromtimestamp(data.get("time_utc"), timezone_1)

    template = f'''
Текущее время: {dt_object}\nНазвание города: {data.get("city_name")}\n\
Погодные условия: {data.get("weather")}\nТекущая температура: {data.get("temp")} градусов по цельсию\n\
Ощущается как: {data.get("temp_feels")} градусов по цельсию \n\
Скорость ветра: {data.get("speed_wind")} м/c
'''
    print(template)


def get_current_location() -> list:
    location = geocoder.ip('me')

    if location.ok:
        latitude, longitude = location.latlng
        print(f"\nВаше местоположение успешно определено!\nКоординаты: Широта {latitude}, Долгота {longitude}")
        return location.latlng
    else:
        print("Не удалось определить местоположение.")
        return [1000, 1000]


def main():

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
                return_button = "r"
                if action_number in "01":
                    city_name = input("\nВведите название города: ")
                    data_weather = my_package.get_weather_by_region_name(city_name)
                    
                    if my_package.city_name_validation(data_weather):
                        information_output_template(data_weather)
                    else:
                        break
                
                    return_button = input('Для возврата в меню введите "r".\nЧтобы продолжить узнавать погоду, введите что угодно :)\n')

                elif action_number in "02":
                    latitude, longitude = get_current_location()

                    if my_package.location_validation(latitude, longitude):
                        data_weather = my_package.get_weather_by_lat_lon(latitude, longitude)
                        if my_package.city_name_validation(data_weather):
                            information_output_template(data_weather)
                        else:
                            break
                    else:
                        break


                    return_button = input('Для возврата в меню введите "r".\n')
                elif action_number in "03":
                    pass


                if return_button == 'r' or return_button == 'к':
                    if return_button == 'к':
                        print("Я знаю, что ты хотел ввести 'r', возвращаю)) ")    
                    break
        except ValueError:
            print("ошибка")



if __name__ == '__main__':
    main()

