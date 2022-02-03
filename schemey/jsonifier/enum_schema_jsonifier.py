from typing import Optional

from marshy.types import ExternalItemType

from schemey.boolean_schema import BooleanSchema
from schemey.enum_schema import EnumSchema
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC


class EnumSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if 'enum' not in item:
            return None
        loaded = EnumSchema(item.get('enum'), item.get('default', NoDefault))
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, EnumSchema):
            return None
        dumped = dict(enum=item.enum)
        if item.default_value is not NoDefault:
            dumped['default'] = item.default_value
        return dumped
