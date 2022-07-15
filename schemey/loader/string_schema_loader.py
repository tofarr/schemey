from typing import Optional

from marshy.types import ExternalItemType

from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.string_schema import StringSchema
from schemey.string_format import StringFormat


class StringSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if item.get("type") != "string":
            return None
        loaded = StringSchema(
            min_length=item.get("minLength"),
            max_length=item.get("maxLength"),
            pattern=item.get("pattern"),
            format=StringFormat(item.get("format")) if item.get("format") else None,
            description=item.get("description"),
        )
        return loaded
