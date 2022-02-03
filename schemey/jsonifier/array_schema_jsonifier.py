from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.array_schema import ArraySchema
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC


class ArraySchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'array':
            return None
        item_schema = None
        if 'items' in item:
            item_schema = json_load.load(item.get('items'))
        loaded = ArraySchema(**filter_none(dict(
            item_schema=item_schema,
            min_items=item.get('minItems'),
            max_items=item.get('maxItems'),
            uniqueness=item.get('uniqueness'),
            default_value=item.get('default', NoDefault)
        )))
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, ArraySchema):
            return None
        items = None
        if item.item_schema:
            items = json_dump.dump(item.item_schema)
        dumped = filter_none(dict(
            type='array',
            items=items,
            minItems=item.min_items,
            maxItems=item.max_items,
            uniqueness=item.uniqueness
        ))
        if item.default_value is not NoDefault:
            dumped['default'] = item.default_value
        return dumped
