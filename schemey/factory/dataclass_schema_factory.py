import dataclasses
from typing import Type, Optional, Dict

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.ref_schema import RefSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext

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
        defs[name] = schema  # prevent infinite loops
        # noinspection PyDataclass
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
        required = field.default is dataclasses.MISSING and field.default_factory is dataclasses.MISSING
        return PropertySchema(field.name, schema, required)
