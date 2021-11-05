from datetime import datetime

from marshy.types import ExternalItemType

from schemey.datetime_schema import DatetimeSchema
from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC, TYPE
from schemey.marshaller.string_schema_marshaller import STRING, FORMAT
from schemey.marshaller.util import filter_none
from schemey.string_format import StringFormat


class DatetimeSchemaMarshaller(SchemaMarshallerABC[DatetimeSchema]):
    priority = 200

    def __init__(self):
        super().__init__(DatetimeSchema)

    def can_load(self, item: ExternalItemType) -> bool:
        return item.get(TYPE) == STRING and item.get(FORMAT) == StringFormat.DATE_TIME.value

    def load(self, item: ExternalItemType) -> DatetimeSchema:
        return DatetimeSchema(
            minimum=datetime.fromisoformat(item['minimum']) if item.get('minimum') is not None else None,
            exclusive_minimum=item.get('exclusiveMinimum') is True,
            maximum=datetime.fromisoformat(item['maximum']) if 'maximum' in item else None,
            exclusive_maximum=item.get('exclusiveMaximum') in [True, None],
        )

    def dump(self, item: DatetimeSchema) -> ExternalItemType:
        exclusive_minimum = item.exclusive_minimum
        exclusive_maximum = item.exclusive_maximum
        return filter_none(dict(
            type='string',
            format=StringFormat.DATE_TIME.value,
            minimum=item.minimum.isoformat() if item.minimum is not None else None,
            exclusiveMinimum=exclusive_minimum if exclusive_minimum != DatetimeSchema.exclusive_minimum else None,
            maximum=item.maximum.isoformat() if item.maximum is not None else None,
            exclusiveMaximum=exclusive_maximum if exclusive_maximum != DatetimeSchema.exclusive_maximum else None
        ))
