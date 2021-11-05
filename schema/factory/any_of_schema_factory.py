from typing import Type, Optional, Union, Dict

import typing_inspect
from marshy.factory.optional_marshaller_factory import get_optional_type

from schema.any_of_schema import AnyOfSchema
from schema.factory.schema_factory_abc import SchemaFactoryABC, T
from schema.null_schema import NullSchema

from schema.schema_abc import SchemaABC
from schema.schema_context import SchemaContext


class AnyOfSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], context: SchemaContext, defs: Dict[str, SchemaABC]) -> Optional[SchemaABC[T]]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            args = typing_inspect.get_args(type_)
            schemas = tuple(context.get_schema(a, defs) for a in args)
            return AnyOfSchema[T](schemas)
