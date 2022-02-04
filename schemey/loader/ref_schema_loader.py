from typing import Optional

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC


class RefSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        if '$ref' not in item:
            return None
        ref = item['$ref']
        if not ref.startswith(json_context.defs_path):
            return None  # We don't support loading from anywhere in the document for now...
        ref = ref[len(json_context.defs_path):]
        schema = json_context.defs[ref]
        schema.num_usages += 1
        return schema
