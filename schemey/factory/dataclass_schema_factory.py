import dataclasses
from typing import Type, Optional, Tuple, Union

from marshy import ExternalType
from marshy.utils import resolve_forward_refs

from schemey.deferred_schema import DeferredSchema
from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.object_schema import ObjectSchema


class DataclassJsonSchemaFactory(JsonSchemaFactoryABC):

    def create(self,
               type_: Type,
               json_context: JsonSchemaContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        if not dataclasses.is_dataclass(type_):
            return
        name = type_.__name__
        schema = json_context.defs.get(name)
        if schema:
            schema.num_usages += 1
            return schema
        schema = DeferredSchema(ref=name, num_usages=1)
        json_context.defs[name] = schema
        fields = dataclasses.fields(type_)
        field_schemas = (self._schema_for_field(f, json_context) for f in fields)
        schema.schema = ObjectSchema(
            properties={n: s for n, s in field_schemas},
            name=type_.__name__,
            default=default,
            required=[
                f.name for f in fields
                if f.init and f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING
            ]
        )
        return schema

    @staticmethod
    def _schema_for_field(field: dataclasses.Field, json_context: JsonSchemaContext) -> Tuple[str, JsonSchemaABC]:
        schema = field.metadata.get('schemey')
        if not schema:
            default_value = NoDefault if field.default is dataclasses.MISSING else field.default
            type_ = resolve_forward_refs(field.type)
            schema = json_context.create_schema(type_, default_value)
        return field.name, schema
