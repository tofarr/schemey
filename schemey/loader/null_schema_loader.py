from typing import Optional

from marshy.types import ExternalItemType

from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.null_schema import NullSchema


class NullSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        loaded = NullSchema(item.get('default', NoDefault)) if item.get('type') == 'null' else None
        return loaded
