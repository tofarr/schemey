from typing import Optional

from marshy.types import ExternalItemType

from schemey.integer_schema import IntegerSchema
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


class IntegerSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if item.get("type") != "integer":
            return None
        loaded = IntegerSchema(
            minimum=item.get("minimum"),
            exclusive_minimum=item.get("exclusiveMinimum"),
            maximum=item.get("maximum"),
            exclusive_maximum=item.get("exclusiveMaximum"),
            description=item.get("description"),
        )
        return loaded
