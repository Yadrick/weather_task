from settings import (
    REQUESTS_EXCEPTION_NOT_FOUND_TEXT,
    REQUESTS_EXCEPTION_CONNECTION_TEXT,
    REQUESTS_UNEXPECTED_ERROR_TEXT,
    GEOCODER_EXCEPTION_TEXT,
    EXIT_EXCEPTIONS_TEXT,
    DATABASE_EXCEPTION_TEXT,
    NEGATIVE_VALUE_ECXEPTION_TEXT,
)


class GeocoderException(Exception):
    def __init__(self) -> None:
        super().__init__(GEOCODER_EXCEPTION_TEXT)


class RequestsExceptionNotFound(Exception):
    def __init__(self) -> None:
        super().__init__(REQUESTS_EXCEPTION_NOT_FOUND_TEXT)


class RequestsExceptionConnection(Exception):
    def __init__(self) -> None:
        super().__init__(REQUESTS_EXCEPTION_CONNECTION_TEXT)


class RequestsExceptionUnexpectedError(Exception):
    def __init__(self) -> None:
        super().__init__(REQUESTS_UNEXPECTED_ERROR_TEXT)


class ExitProgramException(Exception):
    def __init__(self) -> None:
        super().__init__(EXIT_EXCEPTIONS_TEXT)


class DatabaseException(Exception):
    def __init__(self) -> None:
        super().__init__(DATABASE_EXCEPTION_TEXT)


class NegativeValueException(Exception):
    def __init__(self) -> None:
        super().__init__(NEGATIVE_VALUE_ECXEPTION_TEXT)
