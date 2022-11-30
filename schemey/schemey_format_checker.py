from datetime import datetime

from jsonschema import FormatChecker


class SchemeyFormatChecker(FormatChecker):
    """
    As of right now, the standard jsonschema format checker does not do date-time, so we add it
    """

    def __init__(self):
        super().__init__()
        # noinspection PyTypeChecker
        self.checkers["date-time"] = (is_datetime, ValueError)


def is_datetime(value: str):
    return value and datetime.fromisoformat(value)
