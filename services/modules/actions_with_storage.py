from ..classes.HistoryDBs import HistoryDB
from ..classes.exceptions import NegativeValueException, DatabaseException
from settings import (
    VALUE_ERROR_TEXT,
    RECORDS_TO_VIEW_TEXT,
    EXPLANATIONS_TORECORDS_TEXT,
    TOTAL_RECORDS_TEXT,
)


def find_requests_history(storage__weather_history: HistoryDB) -> None:
    """
    Производит поиск истории прогнозов в БД. Когда находит, выводит информацию пользователю.

    Args:
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

    Returns:
        None

    Raises:
        NegativeValueException: Вылазит на ввод отрицательных чисел
        ValueError: выходит при вводе НЕ чисел
        DatabaseException: на случай непредвиденных ошибок при работе с БД
    """
    print(
        f"{TOTAL_RECORDS_TEXT.format(storage__weather_history.max_counts_weather_data())}"
    )
    count_records = input(
        f"{RECORDS_TO_VIEW_TEXT}\n{EXPLANATIONS_TORECORDS_TEXT}\n"
    ).strip()

    try:
        if int(count_records) < 0:
            raise NegativeValueException()

        list_weather_object = storage__weather_history.read_weather_data(
            int(count_records)
        )

        for weather_object in list_weather_object:
            print(weather_object)

    except NegativeValueException:
        raise NegativeValueException()
    except ValueError:
        print(VALUE_ERROR_TEXT)
    except Exception:
        raise DatabaseException()


def delete_query_history(storage__weather_history: HistoryDB) -> None:
    """
    Удаляет данные из таблиц в БД.

    Args:
        storage__weather_history(HistoryDB): объект по работе с Базой данных.

    Returns:
        None
    """
    storage__weather_history.drop_table_weather()
