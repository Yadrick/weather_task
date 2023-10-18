import geocoder
import my_package
import re
from clear_screen import clear


MENU_TEXT = '''
[1] Узнать погоду в городе (по названию)
[2] Узнать погоду по моему местоположению
[3] Узнать историю запросов

[0] Закрыть программу
'''

QUERY_HISTORY_TEXT = '''
[1] Посмотреть историю последних n запросов (n - количество, выбираете сами)
[2] Удалить историю запросов

[r] Вернуться назад
'''


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

    while True:
        my_package.create_db_weather()
        print(MENU_TEXT)

        action_number = input("Выберите пункт меню: ")
        clear()
        if action_number == "0":
            break

        try:
            
            return_button = "r"
            if action_number in "01":
                city_name = input("\nВведите название города: ")
                pattern = r'\b\w*-?\w*\b'
                city_name = re.search(pattern, city_name).group()
                data_weather = my_package.get_weather_by_region_name(city_name)
                
                if my_package.city_name_validation(data_weather):
                    my_package.information_output_template(data_weather)
                else:
                    print("\nПопробуйте снова\n")
            
                while True:
                    return_button = input('Для возврата в меню введите "r".\n')
                    if return_button == 'r' or return_button == 'к':
                        if return_button == 'к':
                            print("Я знаю, что ты хотел ввести 'r', возвращаю)) ")
                        break

            elif action_number in "02":
                latitude, longitude = get_current_location()

                if my_package.location_validation(latitude, longitude):
                    data_weather = my_package.get_weather_by_lat_lon(latitude, longitude)
                    if my_package.city_name_validation(data_weather):
                        my_package.information_output_template(data_weather)
                    else:
                        print("\nПопробуйте снова\n")

                    while True:
                        return_button = input('Для возврата в меню введите "r".\n')
                        if return_button == 'r' or return_button == 'к':
                            if return_button == 'к':
                                print("Я знаю, что вы хотели ввести 'r', возвращаю))\n ")
                            break
            elif action_number in "03":
                while True:
                    print(QUERY_HISTORY_TEXT)
                    action_number_2 = input("Выберите пункт меню: ")
                    clear()

                    if action_number_2 == 'r' or action_number_2 == 'к':
                        if action_number_2 == 'к':
                            print("Я знаю, что вы хотели ввести 'r', возвращаю))\n ")
                        break
                    elif action_number_2 in "02":
                        my_package.drop_table_weather()
                    elif action_number_2 in "01":
                        
                        max_counts_weather_data = my_package.max_counts_weather_data()
                        print(f"\nВсего записей: {max_counts_weather_data}")
                        
                        if max_counts_weather_data == 0:
                            print("Ничем помочь не могу (´• ω •`)\n")
                            input("Чтобы продолжить, введите что угодно :)")
                            clear()
                            break

                        count_records = input("Сколько последних записей вы хотите увидеть?\n"
                                              "(при введении большего числа записей, чем имеется, покажется максимальное количество)\n ")
                        try:
                            data_from_db = my_package.read_weather_data(int(count_records))
                        
                            for one_of_data in range(len(data_from_db)):
                                my_package.information_output_from_db(data_from_db[one_of_data])
                        except Exception as ex:
                            print(f"Ошибка! {ex}")
                        input("\nЧтобы продолжить, введите что угодно :)")
                        clear()
        except ValueError:
            print("ой")

  
if __name__ == '__main__':
    main()
