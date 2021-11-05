import dataclasses
from typing import Type, Optional, Dict

from schema.factory.schema_factory_abc import SchemaFactoryABC
from schema.object_schema import ObjectSchema
from schema.property_schema import PropertySchema
from schema.ref_schema import RefSchema
from schema.schema_abc import SchemaABC
from schema.schema_context import SchemaContext

SCHEMA = 'schema'


class DataclassSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type, context: SchemaContext, defs: Dict[str, SchemaABC]) -> Optional[SchemaABC]:
        if not dataclasses.is_dataclass(type_):
            return
        name = type_.__name__
        if name in defs:
            return defs[name]
        # noinspection PyTypeChecker
        schema = RefSchema(name)
        defs[name] = schema  # prevent inifinite loops
        property_schemas = tuple(self._schema_for_field(f, context, defs) for f in dataclasses.fields(type_))
        defs[name] = ObjectSchema(property_schemas)
        return schema

    @staticmethod
    def _schema_for_field(field: dataclasses.Field,
                          context: SchemaContext,
                          defs: Dict[str, SchemaABC]
                          ) -> PropertySchema:
        schema = field.metadata.get(SCHEMA)
        if not schema:
            schema = context.get_schema(field.type, defs)
        return PropertySchema(field.name, schema)
