from dataclasses import dataclass
from typing import Optional

from marshy.types import ExternalItemType

from schemey.const_schema import ConstSchema
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


@dataclass
class ConstSchemaLoader(SchemaLoaderABC):
    priority: int = 10

    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if "const" not in item:
            return None
        schema = ConstSchema(item["const"], item.get("description"))
        return schema
