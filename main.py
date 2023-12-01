from clear_screen import clear
from settings import MENU_TEXT, NAME_DATABASE
from settings import ACTIONS_NOT_FOUND_TEXT, SELECT_ITEM_TEXT, TO_CONTINUE_TEXT

from services.classes import HistoryDB
from services.classes import ExitProgramException
from services.classes import ActionType

from services.modules import (
    get_weather_by_city_name,
    get_weather_by_location,
    find_requests_history,
    delete_query_history,
)
from services.context_managers import sqlite_connection
from services.modules import close_program


actions_map = {
    ActionType.CLOSE_PROGRAMM: close_program,
    ActionType.GET_WEATHER_BY_CITY_NAME: get_weather_by_city_name,
    ActionType.GET_WEATHER_BY_LOCATION: get_weather_by_location,
    ActionType.FIND_REQUESTS_HISTORY: find_requests_history,
    ActionType.DELETE_QUERY_HISTORY: delete_query_history,
}


def main():
    clear()
    with sqlite_connection(NAME_DATABASE) as connect:
        storage__weather_history = HistoryDB(connect)
        while True:
            print(MENU_TEXT)
            action_number = input(SELECT_ITEM_TEXT).strip()
            clear()

            try:
                action_type = ActionType(action_number)
                action = actions_map.get(action_type)
                action(storage__weather_history)
                input(f"\n{TO_CONTINUE_TEXT}")
            except ExitProgramException as ex:
                print(ex)
                break
            except ValueError:
                print(ACTIONS_NOT_FOUND_TEXT)
            except Exception as ex:
                print(ex)


if __name__ == "__main__":
    main()
