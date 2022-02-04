from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.array_schema import ArraySchema
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext


class ArraySchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'array':
            return None
        item_schema = None
        if 'items' in item:
            item_schema = json_context.load(item.get('items'))
        loaded = ArraySchema(**filter_none(dict(
            item_schema=item_schema,
            min_items=item.get('minItems'),
            max_items=item.get('maxItems'),
            uniqueness=item.get('uniqueness'),
            default=item.get('default', NoDefault)
        )))
        return loaded
