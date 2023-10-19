import my_package
import all_actions
from clear_screen import clear


MENU_TEXT = '''
[1] Узнать погоду в городе (по названию)
[2] Узнать погоду по моему местоположению
[3] Узнать историю запросов

[0] Закрыть программу
'''


def main():

    while True:
        my_package.create_db_weather()
        print(MENU_TEXT)

        action_number = input("Выберите пункт меню: ")
        clear()
        if action_number == "0":
            break

        try:
            if action_number in "01":
                all_actions.find_weather_by_city_name()

            elif action_number in "02":
                all_actions.find_weather_by_location()

            elif action_number in "03":
                all_actions.find_request_history()
        except ValueError:
            print("ой")


if __name__ == '__main__':
    main()
