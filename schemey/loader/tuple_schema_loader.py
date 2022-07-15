from dataclasses import dataclass
from typing import Optional

from marshy.types import ExternalItemType

from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.tuple_schema import TupleSchema


@dataclass
class TupleSchemaLoader(SchemaLoaderABC):
    priority: int = 10

    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if (
            item.get("type") != "array"
            or item.get("prefixItems") is None
            or item.get("items") is not False
        ):
            return None
        schemas = tuple(json_context.load(s) for s in item.get("prefixItems"))
        loaded = TupleSchema(schemas, description=item.get("description"))
        return loaded
