from datetime import timedelta, timezone, datetime
import my_package


def information_output_from_db(data: tuple):

    city_name = data[1]
    weather = data[2]
    temp = data[3]
    temp_feels = data[4]
    speed_wind = data[5]
    time_utc = data[6]
    shift_utc = data[7]

    hours_shift = datetime.utcfromtimestamp(shift_utc).hour
    minutes_shift = datetime.utcfromtimestamp(shift_utc).minute
    timezone_1 = timezone(timedelta(hours=hours_shift, minutes=minutes_shift))
    dt_object = datetime.fromtimestamp(time_utc-shift_utc, timezone_1)

    template = f'''
    Текущее время: {dt_object}\n    Название города: {city_name}\n\
    Погодные условия: {weather}\n    Текущая температура: {temp} градусов по цельсию\n\
    Ощущается как: {temp_feels} градусов по цельсию \n\
    Скорость ветра: {speed_wind} м/c
    '''
    print(template)


def information_output_template(data: dict):

    my_package.insert_weather_data(data)

    hours_shift = datetime.utcfromtimestamp(data.get("shift_utc")).hour
    minutes_shift = datetime.utcfromtimestamp(data.get("shift_utc")).minute
    timezone_1 = timezone(timedelta(hours=hours_shift, minutes=minutes_shift))
    dt_object = datetime.fromtimestamp(data.get("time_utc")-data.get("shift_utc"), timezone_1)

    template = f'''
    Текущее время: {dt_object}\n    Название города: {data.get("city_name")}\n\
    Погодные условия: {data.get("weather")}\n    Текущая температура: {data.get("temp")} градусов по цельсию\n\
    Ощущается как: {data.get("temp_feels")} градусов по цельсию \n\
    Скорость ветра: {data.get("speed_wind")} м/c
    '''
    print(template)
