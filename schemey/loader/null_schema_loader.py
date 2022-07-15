from typing import Optional

from marshy.types import ExternalItemType

from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.null_schema import NullSchema


class NullSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        loaded = NullSchema() if item.get("type") == "null" else None
        return loaded
