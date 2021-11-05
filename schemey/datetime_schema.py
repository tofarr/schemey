from datetime import datetime
from typing import Optional

from schemey.number_schema import NumberSchema


class DatetimeSchema(NumberSchema[datetime]):
    """
    This schema defines some attributes not available in json schema. (Since we serialize dates to iso format rather
    than numeric timestamps - it is just easier to read)
    """

    def __init__(self,
                 minimum: Optional[datetime] = None,
                 exclusive_minimum: bool = False,
                 maximum: Optional[datetime] = None,
                 exclusive_maximum: bool = True):
        super().__init__(datetime, minimum, exclusive_minimum, maximum, exclusive_maximum)
