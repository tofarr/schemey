from typing import Optional

from marshy.types import ExternalItemType

from schemey.any_of_schema import AnyOfSchema
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


class AnyOfSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        any_of = item.get("anyOf")
        if any_of is None:
            return
        schemas = tuple(json_context.load(a) for a in any_of)
        loaded = AnyOfSchema(
            **dict(
                schemas=schemas,
                name=item.get("name"),
                description=item.get("description"),
            )
        )
        return loaded
