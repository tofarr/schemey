import dataclasses
from typing import Type, Optional

from schemey.deferred_schema import DeferredSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext

SCHEMA = 'schema'


class DataclassSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type, default_value, context: SchemaContext) -> Optional[SchemaABC]:
        if not dataclasses.is_dataclass(type_):
            return
        context.register_schema(type_, DeferredSchema[type_](context, type_))
        # noinspection PyDataclass
        property_schemas = tuple(self._schema_for_field(f, context) for f in dataclasses.fields(type_))
        schema = ObjectSchema[type_](type_, property_schemas, default_value=default_value)
        return schema

    @staticmethod
    def _schema_for_field(field: dataclasses.Field, context: SchemaContext) -> PropertySchema:
        schema = field.metadata.get(SCHEMA)
        if not schema:
            schema = context.get_schema(field.type)
        required = field.default is dataclasses.MISSING and field.default_factory is dataclasses.MISSING
        return PropertySchema(field.name, schema, required)
