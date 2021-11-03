import dataclasses
from typing import Type, Optional

from persisty.schema.factory.schema_factory_abc import SchemaFactoryABC
from persisty.schema.object_schema import ObjectSchema
from persisty.schema.property_schema import PropertySchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_context import SchemaContext

SCHEMA = 'schema'


class DataclassSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type, context: SchemaContext) -> Optional[SchemaABC]:
        if not dataclasses.is_dataclass(type_):
            return
        property_schemas = tuple(self._schema_for_field(f, context) for f in dataclasses.fields(type_))
        return ObjectSchema(property_schemas)

    @staticmethod
    def _schema_for_field(field: dataclasses.Field, context: SchemaContext) -> PropertySchema:
        schema = field.metadata.get(SCHEMA)
        if not schema:
            schema = context.get_schema(field.type)
        return PropertySchema(field.name, schema)
