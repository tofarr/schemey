import dataclasses
from typing import Type, Optional, Tuple, Union

from marshy import ExternalType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.object_schema import ObjectSchema
from schemey.schemey_context import SchemeyContext


class DataclassSchemaFactory(SchemaFactoryABC):

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        if not dataclasses.is_dataclass(type_):
            return
        fields = dataclasses.fields(type_)
        field_schemas = (self._schema_for_field(f, context) for f in fields)
        schema = ObjectSchema(
            properties={n: s for n, s in field_schemas},
            name=type_.__name__,
            default_value=default_value,
            required=[
                f.name for f in fields
                if f.init and f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING
            ]
        )
        return schema

    @staticmethod
    def _schema_for_field(field: dataclasses.Field, context: SchemeyContext) -> Tuple[str, JsonSchemaABC]:
        schema = field.metadata.get('schemey')
        if not schema:
            default_value = NoDefault if field.default is dataclasses.MISSING else field.default
            schema = context.get_schema(field.type, default_value).json_schema
        return field.name, schema
