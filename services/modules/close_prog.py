from ..classes.exceptions import ExitProgramException
from ..classes.HistoryDBs import HistoryDB


def close_program(storage__weather_history: HistoryDB) -> None:
    """
    Нужна для завершения работы программы.

    Args:
        storage__weather_history(HistoryDB): объект по работе с Базой данных. В методе не используется.

    Returns:
        None

    Raises:
        ExitProgramException: выводит завершающий текст.
    """
    raise ExitProgramException()
