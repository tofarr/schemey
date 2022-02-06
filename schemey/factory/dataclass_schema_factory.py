import dataclasses
from typing import Type, Optional, Tuple

from marshy.factory.optional_marshaller_factory import get_optional_type

from schemey.deferred_schema import DeferredSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.object_schema import ObjectSchema
from schemey.optional_schema import OptionalSchema, NoDefault


class DataclassSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type, json_context: JsonSchemaContext) -> Optional[SchemaABC]:
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
        field_schemas = tuple(self._schema_for_field(f, json_context) for f in fields)
        required = {n for n, s in field_schemas if not isinstance(s, OptionalSchema)}
        schema.schema = ObjectSchema(
            properties={n: s for n, s in field_schemas},
            name=type_.__name__,
            required=required or None
        )
        return schema

    @staticmethod
    def _schema_for_field(field: dataclasses.Field, json_context: JsonSchemaContext) -> Tuple[str, SchemaABC]:
        schema = field.metadata.get('schemey')
        field_type = get_optional_type(field.type) or field.type
        if not schema:
            schema = json_context.get_schema(field_type)
        default = NoDefault
        if field.default is not dataclasses.MISSING:
            if field.default is None:
                default = None
            else:
                default = json_context.marshaller_context.dump(field.default, field_type)
        if default is not NoDefault or field.default_factory is not dataclasses.MISSING:
            schema = OptionalSchema(schema, default)
        return field.name, schema
