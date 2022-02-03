from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.integer_schema import IntegerSchema
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC


class IntegerSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'integer':
            return None
        loaded = IntegerSchema(
            minimum=item.get('minimum'),
            exclusive_minimum=item.get('exclusiveMinimum'),
            maximum=item.get('maximum'),
            exclusive_maximum=item.get('exclusiveMaximum'),
            default_value=item.get('default', NoDefault)
        )
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        # noinspection PyTypeChecker
        return dump_schema(item, IntegerSchema, 'integer')


def dump_schema(item, expected_type, type_name: str) -> Optional[ExternalItemType]:
    if not isinstance(item, expected_type):
        return None
    dumped = filter_none(dict(
        type=type_name,
        minimum=item.minimum,
        exclusiveMinimum=item.exclusive_minimum,
        maximum=item.maximum,
        exclusiveMaximum=item.exclusive_maximum,
    ))
    if item.default_value is not NoDefault:
        dumped['default'] = item.default_value
    return dumped
