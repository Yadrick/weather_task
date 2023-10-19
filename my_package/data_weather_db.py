import sqlite3 as sq

NAME_TABLE = "user_weather_data"
NAME_SUPPORTING_TABLE = "sqlite_sequence"


def create_db_weather():

    with sq.connect("data_weather.db") as con:
        cur = con.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {NAME_TABLE} (
            record_number INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT,
            weather TEXT,
            temp REAL,
            temp_feels REAL,
            speed_wind REAL,
            time_utc INTEGER,
            shift_utc INTEGER
            )''')


def drop_table_weather():
    with sq.connect("data_weather.db") as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {NAME_TABLE}")
        print('Данные успешно удалены!')


def insert_weather_data(data_weather: dict):
    with sq.connect("data_weather.db") as con:
        cur = con.cursor()

        cur.execute(f'''INSERT INTO {NAME_TABLE}
                    (city_name, weather, temp, temp_feels, speed_wind, time_utc, shift_utc)
                    VALUES ('{data_weather.get('city_name')}', '{data_weather.get('weather')}', {data_weather.get('temp')},
                    {data_weather.get('temp_feels')}, {data_weather.get('speed_wind')}, {data_weather.get('time_utc')},
                    {data_weather.get('shift_utc')})
                    ''')


def read_weather_data(count_records_output: int) -> list:
    with sq.connect("data_weather.db") as con:
        cur = con.cursor()

        try:
            max_counts = cur.execute(
                f'SELECT seq FROM {NAME_SUPPORTING_TABLE} ').fetchone()[0]
            cur.execute(
                f'SELECT * FROM {NAME_TABLE} LIMIT {count_records_output} OFFSET {max_counts-count_records_output}')
            result = cur.fetchall()
        except Exception:
            result = []
    return result


def max_counts_weather_data():
    with sq.connect("data_weather.db") as con:
        cur = con.cursor()
        try:
            max_counts = cur.execute(
                f'SELECT seq FROM {NAME_SUPPORTING_TABLE} ').fetchone()[0]
        except Exception:
            max_counts = 0
    return max_counts
