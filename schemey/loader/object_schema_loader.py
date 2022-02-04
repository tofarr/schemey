from typing import Optional

from marshy.types import ExternalItemType

from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.object_schema import ObjectSchema


class ObjectSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'object':
            return None
        name = item.get('name')
        properties = item.get('properties') or {}
        properties = {k: json_context.load(s) for k, s in properties.items()}
        loaded = ObjectSchema(
            name=name,
            properties=properties,
            additional_properties=item.get('additionalProperties'),
            required=item.get('required')
        )
        return loaded
