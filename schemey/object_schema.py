from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Set, Tuple, Union

from marshy.types import ExternalItemType, ExternalType

from schemey._util import filter_none
from schemey.optional_schema import NoDefault
from schemey.param_schema import ParamSchema
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

    def get_param_schemas(self, current_path: str) -> Optional[List[ParamSchema]]:
        param_schemas = []
        for name, schema in self.properties.items():
            sub_path = f"{current_path}.{name}" if current_path else name
            sub_schemas = schema.get_param_schemas(sub_path)
            if sub_schemas is None:
                return None
            param_schemas.extend(sub_schemas)
        return param_schemas

    def from_url_params(self, current_path: str, params: Dict[str, List[str]]) -> Union[ExternalType, NoDefault]:
        result = {}
        for key, schema in self.properties.items():
            sub_path = self._sub_path(current_path, key)
            value = schema.from_url_params(sub_path, params)
            if value is NoDefault:
                raise SchemaError(current_path, 'missing_value')
            result[key] = value
        return result

    def to_url_params(self, current_path: str, item: ExternalItemType) -> Iterator[Tuple[str, str]]:
        for key, schema in self.properties.items():
            if key in item:
                sub_path = self._sub_path(current_path, key)
                yield from schema.to_url_params(sub_path, item[key])

    def _sub_path(self, current_path: str, key: str):
        sub_path = f"{current_path}.{key}" if current_path else key
        return sub_path
