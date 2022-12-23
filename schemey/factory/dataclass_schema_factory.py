import dataclasses
from typing import Type, Optional, get_type_hints, Dict

import typing_inspect
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


class DataclassSchemaFactory(SchemaFactoryABC):
    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        if not dataclasses.is_dataclass(type_):
            return
        # Setting this here will mean any nested references will not fail
        schema = Schema({"$ref": path}, type_)
        ref_schemas[type_] = schema
        # noinspection PyDataclass
        fields = dataclasses.fields(type_)
        try:
            types = get_type_hints(type_, globalns=None, localns=None)
        except NameError:
            types = {f.name: f.type for f in fields}

        properties = {}
        required = []
        for field in fields:
            field_schema = field.metadata.get("schemey")
            if not field_schema:
                field_schema = context.schema_from_type(
                    types[field.name], f"{path}/properties/{field.name}", ref_schemas
                )
            if (
                field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING
            ):
                required.append(field.name)
            if field.default is not dataclasses.MISSING:
                field_schema = Schema({**field_schema.schema}, field_schema.python_type)
                field_schema.schema["default"] = context.marshaller_context.dump(
                    field.default, types[field.name]
                )
            properties[field.name] = field_schema.schema

        schema = {
            "type": "object",
            "name": type_.__name__,
            "properties": properties,
            "additionalProperties": False,
            "required": required,
        }
        if type_.__doc__:
            schema["description"] = type_.__doc__.strip()
        schema = Schema(schema, type_)
        return schema

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        type_ = item.get("type")
        name = item.get("name")
        properties = item.get("properties")
        additional_properties = item.get("additionalProperties")
        if (
            type_ != "object"
            or not name
            or properties is None
            or additional_properties is not False
        ):
            return
        # noinspection PyTypeChecker
        ref_schema = Schema(
            {"$ref": path}, name
        )  # Having the name here implies that this will be a future annotation
        ref_schemas[path] = ref_schema
        params = {}
        annotations = {}
        params_with_default = {}

        for field_name, field_item in item.get("properties").items():
            field_schema = context.schema_from_json(
                field_item, f"{path}/{field_name}", ref_schemas
            )
            default = field_item.get("default", dataclasses.MISSING)
            if default is not dataclasses.MISSING:
                default = context.marshaller_context.load(
                    field_schema.python_type, default
                )
                p = params_with_default
            else:
                p = params
            field = dataclasses.field(
                default=default, metadata={"schemey": field_schema}
            )
            field.name = field_name
            field.type = field_schema.python_type
            annotations[field_name] = field.type
            p[field_name] = field
        params.update(**params_with_default)
        params["__annotations__"] = {
            k: annotations[k] for k in params
        }  # dataclasses uses annotation order...
        description = item.get("description")
        if description:
            params["__doc__"] = description
        type_ = dataclasses.dataclass(type(name, (), params))

        # Circular references are resolved at the end once we have a type with which to resolve them
        _resolve_futures(type_, name, type_)
        return Schema(item, type_)


def _resolve_futures(type_: Type, replace_name: str, replace_type: Type):
    if type_ == replace_name:
        return replace_type
    if typing_inspect.is_forward_ref(type_):
        import_name = typing_inspect.get_forward_arg(type_)
        if replace_name == import_name:
            return replace_type
    args = typing_inspect.get_args(type_)
    if args:
        args = tuple(_resolve_futures(a, replace_name, replace_type) for a in args)
        return type_.copy_with(args)
    if dataclasses.is_dataclass(type_):
        # noinspection PyDataclass
        for field in dataclasses.fields(type_):
            field.type = _resolve_futures(field.type, replace_name, replace_type)
    return type_
