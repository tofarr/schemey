from datetime import datetime
from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_output_context import JsonOutputContext
from schemey.number_schema import NumberSchema
from schemey.string_format import StringFormat


class DatetimeSchema(NumberSchema[datetime]):
    """
    This schema defines some attributes not available in json schema. (Since we serialize dates to iso format rather
    than numeric timestamps - it is just easier to read)
    """

    def __init__(self,
                 minimum: Optional[datetime] = None,
                 exclusive_minimum: bool = False,
                 maximum: Optional[datetime] = None,
                 exclusive_maximum: bool = True,
                 default_value: Optional[datetime] = None):
        super().__init__(datetime, minimum, exclusive_minimum, maximum, exclusive_maximum, default_value)

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        exclusive_minimum = self.exclusive_minimum
        exclusive_maximum = self.exclusive_maximum
        return filter_none(dict(
            type='string',
            format=StringFormat.DATE_TIME.value,
            minimum=self.minimum.isoformat() if self.minimum is not None else None,
            exclusiveMinimum=exclusive_minimum if exclusive_minimum != DatetimeSchema.exclusive_minimum else None,
            maximum=self.maximum.isoformat() if self.maximum is not None else None,
            exclusiveMaximum=exclusive_maximum if exclusive_maximum != DatetimeSchema.exclusive_maximum else None
        ))
