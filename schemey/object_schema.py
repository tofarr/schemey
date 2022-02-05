from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Set

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class ObjectSchema(SchemaABC):
    properties: Dict[str, SchemaABC]
    name: Optional[str] = None
    additional_properties: bool = False
    required: Optional[Set[str]] = None

    def get_schema_errors(self, item: ExternalItemType, current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        if not isinstance(item, dict):
            yield SchemaError(current_path, 'type', item)
            return
        keys = set(item.keys())
        if self.required:
            missing = self.required - keys
            if missing:
                yield SchemaError(current_path, 'missing_properties', ", ".join(missing))
        for key, value in item.items():
            property_schema = self.properties.get(key)
            if property_schema:
                keys.remove(key)
                yield from property_schema.get_schema_errors(value, current_path)
        if keys and not self.additional_properties:
            yield SchemaError(current_path, 'additional_properties', ', '.join(keys))

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = filter_none(dict(
            type='object',
            name=self.name,
            additionalProperties=self.additional_properties
        ))
        properties = {k: s.dump_json_schema(json_context) for k, s in self.properties.items()}
        if properties:
            dumped['properties'] = properties
        if self.required:
            required = list(self.required)
            required.sort()
            dumped['required'] = required
        return dumped

    def simplify(self) -> SchemaABC:
        properties = {k: p.simplify() for k, p in self.properties.items()}
        schema = ObjectSchema(**{**self.__dict__, 'properties': properties})
        return schema
