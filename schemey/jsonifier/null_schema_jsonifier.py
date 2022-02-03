from typing import Optional

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC
from schemey.null_schema import NullSchema


class NullSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        loaded = NullSchema(item.get('default', NoDefault)) if item.get('type') == 'null' else None
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, NullSchema):
            return None
        dumped = dict(type='null')
        if item.default_value is not NoDefault:
            dumped['default'] = item.default_value
        return dumped
