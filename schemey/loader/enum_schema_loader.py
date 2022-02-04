from typing import Optional

from marshy.types import ExternalItemType

from schemey.enum_schema import EnumSchema
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext


class EnumSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        if 'enum' not in item:
            return None
        loaded = EnumSchema(item.get('enum'), item.get('default', NoDefault))
        return loaded
