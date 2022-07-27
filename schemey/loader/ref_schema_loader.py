from typing import Optional

from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.loader.schema_loader_abc import SchemaLoaderABC


class RefSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if "$ref" not in item:
            return None
        ref = item["$ref"]
        if not ref.startswith(json_context.defs_path):
            return None  # We don't support loading from anywhere in the document for now...
        ref = ref[len(json_context.defs_path):]
        schema = json_context.defs[ref]
        schema.num_usages += 1
        return schema
