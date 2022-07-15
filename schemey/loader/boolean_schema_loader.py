from typing import Optional

from marshy.types import ExternalItemType

from schemey.boolean_schema import BooleanSchema
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


class BooleanSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if item.get("type") != "boolean":
            return None
        loaded = BooleanSchema(item.get("description"))
        return loaded
