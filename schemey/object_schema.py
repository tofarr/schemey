from dataclasses import dataclass
from typing import Union, Optional, List, Iterator, Dict

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class ObjectSchema(JsonSchemaABC):
    properties: Dict[str, JsonSchemaABC]
    name: Optional[str] = None
    default: Union[ExternalItemType, NoDefault] = NoDefault
    additional_properties: bool = False
    required: Optional[List[str]] = None

    def get_schema_errors(self, item: ExternalItemType, current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        if not isinstance(item, dict):
            yield SchemaError(current_path, 'type', item)
            return
        keys = set(item.keys())
        for key, property_schema in self.properties.items():
            if key in keys:
                keys.remove(key)
            yield from property_schema.get_schema_errors(item, current_path)
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
            dumped['required'] = self.required
        if self.default is not NoDefault:
            dumped['default'] = self.default
        return dumped

    def simplify(self) -> JsonSchemaABC:
        properties = {k: p.simplify() for k, p in self.properties.items()}
        schema = ObjectSchema(**{**self.__dict__, 'properties': properties})
        return schema
