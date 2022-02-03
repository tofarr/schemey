from typing import Optional

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.integer_schema_jsonifier import dump_schema
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC
from schemey.number_schema import NumberSchema


class NumberSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'number':
            return None
        loaded = NumberSchema(
            minimum=item.get('minimum'),
            exclusive_minimum=item.get('exclusiveMinimum'),
            maximum=item.get('maximum'),
            exclusive_maximum=item.get('exclusiveMaximum'),
            default_value=item.get('default', NoDefault)
        )
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        return dump_schema(item, NumberSchema, 'number')
