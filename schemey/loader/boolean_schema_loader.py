from typing import Optional

from marshy.types import ExternalItemType

from schemey.boolean_schema import BooleanSchema
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext


class BooleanSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'boolean':
            return None
        loaded = BooleanSchema(item.get('default', NoDefault))
        return loaded
