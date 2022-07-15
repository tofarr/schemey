from typing import Optional

from marshy.types import ExternalItemType

from schemey.enum_schema import EnumSchema
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


class EnumSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if "enum" not in item or "name" not in item:
            return None
        loaded = EnumSchema(
            name=item.get("name"),
            enum=set(item.get("enum")),
            description=item.get("description"),
        )
        return loaded
