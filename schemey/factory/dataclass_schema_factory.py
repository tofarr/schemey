import dataclasses
from typing import Type, Optional, Tuple, get_type_hints

from marshy.factory.optional_marshaller_factory import get_optional_type

from schemey.deferred_schema import DeferredSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.object_schema import ObjectSchema
from schemey.optional_schema import OptionalSchema, NoDefault


class DataclassSchemaFactory(SchemaFactoryABC):
    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if not dataclasses.is_dataclass(type_):
            return
        name = type_.__name__
        schema = json_context.defs.get(name)
        if schema:
            schema.num_usages += 1
            return schema
        schema = DeferredSchema(ref=name, num_usages=1)
        json_context.defs[name] = schema
        # noinspection PyDataclass
        fields = dataclasses.fields(type_)
        try:
            types = get_type_hints(type_, globalns=None, localns=None)
        except NameError:
            types = {f.name: f.type for f in fields}
        field_schemas = tuple(self._schema_for_field(f, types, json_context) for f in fields)
        required = {n for n, s in field_schemas if not isinstance(s, OptionalSchema)}
        schema.schema = ObjectSchema(
            properties={n: s for n, s in field_schemas},
            name=type_.__name__,
            required=required or None,
        )
        return schema

    @staticmethod
    def _schema_for_field(
        field: dataclasses.Field, types, json_context: JsonSchemaContext
    ) -> Tuple[str, SchemaABC]:
        schema = field.metadata.get("schemey")
        field_type = field.type
        if isinstance(field_type, str):
            field_type = types[field.name]
        field_type = get_optional_type(field_type) or field_type
        if not schema:
            schema = json_context.get_schema(field_type)
        default = NoDefault
        if field.default is not dataclasses.MISSING:
            if field.default is None:
                default = None
            else:
                default = json_context.marshaller_context.dump(
                    field.default, field_type
                )
        if default is not NoDefault or field.default_factory is not dataclasses.MISSING:
            schema = OptionalSchema(schema, default)
        return field.name, schema
