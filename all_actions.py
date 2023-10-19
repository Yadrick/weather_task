import my_package
import re
from clear_screen import clear


QUERY_HISTORY_TEXT = '''
[1] Посмотреть историю последних n запросов (n - количество, выбираете сами)
[2] Удалить историю запросов

[r] Вернуться назад
'''


def find_weather_by_city_name():
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


def find_weather_by_location():
    latitude, longitude = my_package.get_current_location()

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


def find_request_history():
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
                    my_package.information_output_from_db(
                        data_from_db[one_of_data])
            except ValueError:
                print("Ошибка! Это не число :(")
            except Exception as ex:
                print(f"Ошибка! {ex}")
            input("\nЧтобы продолжить, введите что угодно :)")
            clear()
