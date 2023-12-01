from settings import (
    NAME_TABLE,
    NAME_SUPPORTING_TABLE,
    CREATE_DATABASE_REQUEST,
    DELETE_FROM_REQUEST,
    SUCCESSFUL_DELETE_TEXT,
    INSERT_INTO_TABLE_REQUEST,
    SELECT_SEQ_FROM_REQUEST,
    SELECT_ALL_SEQ_FOR_USER_REQUEST,
)
from .exceptions import DatabaseException
from .Weathers import WeatherReading, Weather


class HistoryDB:
    def create_db_weather(self) -> None:
        """
        Функция создает базу данных, если она еще не создана в каталоге.

        Returns:
            None
        """
        cur = self.connection.cursor()
        cur.execute(f"{CREATE_DATABASE_REQUEST.format(NAME_TABLE)}")

    def __init__(self, connection) -> None:
        self.connection = connection
        self.create_db_weather()

    def drop_table_weather(self) -> None:
        """
        Функция очищает таблицы с данными.

        Returns:
            None

        Raise:
            DatabaseException - райзит, когда возникают проблемы с БД
        """
        try:
            cur = self.connection.cursor()
            cur.execute(f"{DELETE_FROM_REQUEST.format(NAME_TABLE)}")
            cur.execute(f"{DELETE_FROM_REQUEST.format(NAME_SUPPORTING_TABLE)}")
            self.connection.commit()
            print(SUCCESSFUL_DELETE_TEXT)
        except Exception:
            raise DatabaseException()

    def insert_weather_data(self, data_weather_object: Weather) -> None:
        """
        Функция получает объект погоды и извлекает из него необходимые данные для сохранения.

        Args:
            data_weather_object(Weather): объект Погоды, который содержит данные для вывода.

        Returns:
            None

        Raise:
            DatabaseException - райсит, если случается ошибка при работе с БД
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                f"{INSERT_INTO_TABLE_REQUEST.format(NAME_TABLE)}",
                (
                    data_weather_object.city_name,
                    data_weather_object.weather,
                    data_weather_object.temp,
                    data_weather_object.temp_feels,
                    data_weather_object.speed_wind,
                    data_weather_object.present_time,
                ),
            )
            self.connection.commit()
        except Exception:
            raise DatabaseException()

    def processing_data_from_db(
        self, weather_data_list: list[tuple]
    ) -> list[WeatherReading]:
        """
        Функция получает данные о погоде в виде списка кортежей. Возвращает список объектов Погоды,
        готовые для вывода пользователю.

        Args:
            weather_data_list(list[tuple])): список данных о погоде

        Returns:
            list[WeatherReading] - возвращает список обьектов погоды для чтения.
        """
        list_weather_object = []

        for weather_data_tuple in weather_data_list:
            weather_data = WeatherReading(*weather_data_tuple)

            list_weather_object.append(weather_data)

        return list_weather_object

    def read_weather_data(self, count_records_output: int) -> list[WeatherReading]:
        """
        Функция получает данные из Базы Данных в количестве {count_records_output} последних штук.
        Если данных меньше, чем {count_records_output}, то вернутся просто все имеющиееся данные.

        Args:
            count_records_output(int): количество строк, необходимое для просмотра пользователю

        Returns:
            list[WeatherReading] - возвращает список Объектов Погоды, готовые для вывода пользователю.

        Raises:
            DatabaseException: на случай ошибок во время работы с Базой Данных.
        """

        cur = self.connection.cursor()
        try:
            cur.execute(
                f"{SELECT_ALL_SEQ_FOR_USER_REQUEST.format(NAME_TABLE, count_records_output)}"
            )
            result = cur.fetchall()
            return self.processing_data_from_db(result)
        except Exception:
            raise DatabaseException()

    def max_counts_weather_data(self) -> int:
        """
        Функция получает количество записей в Базе.

        Returns:
            int - возвращает количество записей в БД

        Raises:
            DatabaseException: на случай ошибок во время работы с Базой Данных.
        """
        cur = self.connection.cursor()
        try:
            result_row = cur.execute(
                f"{SELECT_SEQ_FROM_REQUEST}{NAME_SUPPORTING_TABLE}"
            ).fetchone()
            max_counts = result_row[0] if result_row is not None else 0
            return max_counts
        except Exception:
            raise DatabaseException()
