import copy
from typing import Optional, Set

from marshy.types import ExternalItemType

from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.object_schema import ObjectSchema
from schemey.optional_schema import OptionalSchema, NoDefault


class ObjectSchemaLoader(SchemaLoaderABC):
    def load(
        self, item: ExternalItemType, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if item.get("type") != "object":
            return None
        name = item.get("name")
        properties = item.get("properties") or {}
        required = set(item.get("required") or [])
        properties = {
            k: self._load_optional(k, s, required, json_context)
            for k, s in properties.items()
        }
        loaded = ObjectSchema(
            name=name,
            properties=properties,
            additional_properties=item.get("additionalProperties"),
            required=required or None,
            description=item.get("description"),
        )
        return loaded

    @staticmethod
    def _load_optional(
        key: str, item: ExternalItemType, required: Set[str], context: JsonSchemaContext
    ) -> SchemaABC:
        schema = context.load(item)
        if key not in required:
            default = NoDefault
            if "default" in item:
                default = copy.deepcopy(item["default"])
            schema = OptionalSchema(schema, default)
        return schema
