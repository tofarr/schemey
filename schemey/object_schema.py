from dataclasses import dataclass, field, is_dataclass, fields, MISSING
from typing import Optional, List, Iterator, Dict, Set, Tuple, Union, Type, Any

import typing

import typing_inspect
from marshy.factory.optional_marshaller_factory import get_optional_type
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
    description: Optional[str] = None

    def get_schema_errors(
        self, item: ExternalItemType, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if not isinstance(item, dict):
            yield SchemaError(current_path, "type", item)
            return
        keys = set(item.keys())
        if self.required:
            missing = self.required - keys
            if missing:
                yield SchemaError(
                    current_path, "missing_properties", ", ".join(missing)
                )
        for key, value in item.items():
            property_schema = self.properties.get(key)
            if property_schema:
                keys.remove(key)
                yield from property_schema.get_schema_errors(value, current_path)
        if keys and not self.additional_properties:
            yield SchemaError(current_path, "additional_properties", ", ".join(keys))

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = filter_none(
            dict(
                type="object",
                name=self.name,
                additionalProperties=self.additional_properties,
                description=self.description,
            )
        )
        properties = {
            k: s.dump_json_schema(json_context) for k, s in self.properties.items()
        }
        if properties:
            dumped["properties"] = properties
        if self.required:
            required = list(self.required)
            required.sort()
            dumped["required"] = required
        return dumped

    def simplify(self) -> SchemaABC:
        properties = {k: p.simplify() for k, p in self.properties.items()}
        schema = ObjectSchema(**{**self.__dict__, "properties": properties})
        return schema

    def get_param_schemas(self, current_path: str) -> Optional[List[ParamSchema]]:
        param_schemas = []
        for name, schema in self.properties.items():
            sub_path = self._sub_path(current_path, name)
            sub_schemas = schema.get_param_schemas(sub_path)
            if sub_schemas is None:
                return None
            param_schemas.extend(sub_schemas)
        return param_schemas

    def from_url_params(
        self, current_path: str, params: Dict[str, List[str]]
    ) -> Union[ExternalType, type(MISSING), NoDefault]:
        result = {}
        for key, schema in self.properties.items():
            sub_path = self._sub_path(current_path, key)
            value = schema.from_url_params(sub_path, params)
            if value is NoDefault:
                return NoDefault
            elif value is not MISSING:
                result[key] = value
        return result

    def to_url_params(
        self, current_path: str, item: ExternalItemType
    ) -> Iterator[Tuple[str, str]]:
        for key, schema in self.properties.items():
            if key in item:
                sub_path = self._sub_path(current_path, key)
                yield from schema.to_url_params(sub_path, item[key])

    @staticmethod
    def _sub_path(current_path: str, key: str):
        sub_path = f"{current_path}.{key}" if current_path else key
        return sub_path

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: typing.Callable
    ) -> Type:
        type_ = existing_types.get(self.name)
        if type_:
            return type_
        existing_types[self.name] = typing.ForwardRef(self.name)
        attributes = build_attributes(
            self.properties.items().__iter__(), existing_types, object_wrapper
        )
        type_ = object_wrapper(type(self.name, (), attributes))
        existing_types[self.name] = type_
        _resolve_forward_refs(type_, existing_types)
        return type_


def build_attributes(
    properties: Iterator[Tuple[str, SchemaABC]],
    existing_types: Dict[str, Any],
    object_wrapper: typing.Callable,
):
    annotations = {}
    attrs = {"__annotations__": annotations}
    default_attrs = {}
    for name, schema in properties:
        type_ = schema.get_normalized_type(existing_types, object_wrapper)
        if hasattr(schema, "default"):
            if schema.default is NoDefault:
                default = None
                type_ = Optional[get_optional_type(type_) or type_]
            else:
                default = schema.default
            default_attrs[name] = field(default=default)
        else:
            attrs[name] = field()
        annotations[name] = type_
    attrs.update(**default_attrs)
    return attrs


def _resolve_forward_refs(type_, existing_types: Dict[str, Any]) -> typing.Type:
    if isinstance(type_, typing.ForwardRef):
        type_ = existing_types[type_.__forward_arg__]
        return type_
    if is_dataclass(type_):
        for f in fields(type_):
            f.type = type_.__annotations__[f.name] = _resolve_forward_refs(
                f.type, existing_types
            )
        return type_
    origin = typing_inspect.get_origin(type_)
    if origin is not None:
        type_.__args__ = tuple(
            _resolve_forward_refs(a, existing_types) for a in type_.__args__
        )
    return type_
