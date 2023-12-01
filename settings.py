"Модуль для хранения констант"

# REQUESTS
API_KEY = "bbeae2106b4b784ac7fc75027c4886b3"
URL_FOR_DATA_NAME = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"


# WEATHER OUTPUT TEXT
CURRENT_TIME = "Текущее время: "
CITY_NAME = "Название города: "
WEATHER_CONDITION = "Погодные условия: "
TEMPERATURE = "Текущая температура: "
TEMPERATURE_FEELS = "Ощущается как: "
CELSIUS = " градусов по цельсию"
WIND_SPEED = "Скорость ветра: "
MS = " м/c"


# OUTPUT TEXT
MENU_TEXT = """
[1] Узнать погоду в городе (по названию)
[2] Узнать погоду по моему местоположению
[3] Узнать историю запросов
[4] Удалить историю запросов

[0] Закрыть программу
"""

SELECT_ITEM_TEXT = "Выберите пункт меню: "
INPUT_CITY_NAME_TEXT = "Введите название города: "
TO_CONTINUE_TEXT = "Чтобы продолжить, введите что угодно :)"
TOTAL_RECORDS_TEXT = "Всего {} записей в базе."
RECORDS_TO_VIEW_TEXT = "Сколько последних записей вы хотите увидеть?"
EXPLANATIONS_TORECORDS_TEXT = "(при введении большего числа записей, чем имеется, покажется максимальное количество)"
ACTIONS_NOT_FOUND_TEXT = (
    "Данного действия не существует. Пожалуйста, выберите что-то из списка."
)


# DATABASE
NAME_DATABASE = "data_weather.db"
NAME_TABLE = "user_weather_data"
NAME_SUPPORTING_TABLE = "sqlite_sequence"

CREATE_DATABASE_REQUEST = """CREATE TABLE IF NOT EXISTS {} (
            record_number INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT,
            weather TEXT,
            temp REAL,
            temp_feels REAL,
            speed_wind REAL,
            present_time TEXT
            )"""
INSERT_INTO_TABLE_REQUEST = """INSERT INTO {}
                        (city_name, weather, temp, temp_feels, speed_wind, present_time)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """
DELETE_FROM_REQUEST = "DELETE FROM {}"
SELECT_SEQ_FROM_REQUEST = "SELECT seq FROM "
SELECT_ALL_SEQ_FOR_USER_REQUEST = (
    "SELECT * FROM {} ORDER BY record_number DESC LIMIT {}"
)
SUCCESSFUL_DELETE_TEXT = "Данные успешно удалены!"


# EXCEPTIONS
VALUE_ERROR_TEXT = "Ошибка! Это не число :("
NEGATIVE_VALUE_ECXEPTION_TEXT = "Принимаем только положительные числа!"
DATABASE_EXCEPTION_TEXT = "У нас пролемы в работе с базами данных. Уже решаем!"
REQUESTS_EXCEPTION_NOT_FOUND_TEXT = "Запрашиваемый город не найден."
REQUESTS_EXCEPTION_CONNECTION_TEXT = (
    "Превышено время ожидания ответа. Попробуйте позже."
)
REQUESTS_UNEXPECTED_ERROR_TEXT = "Произошла непредвиденная ошибка. Попробуйте позже."
GEOCODER_EXCEPTION_TEXT = "Не удалось определить ваше местоположение, попробуйте позже"
EXIT_EXCEPTIONS_TEXT = "To be continued."
