from typing import Type, Optional, Union

import typing_inspect
from marshy.factory.optional_marshaller_factory import get_optional_type

from persisty.schema.any_of_schema import AnyOfSchema
from persisty.schema.factory.schema_factory_abc import SchemaFactoryABC, T
from persisty.schema.null_schema import NullSchema

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_context import SchemaContext


class OptionalSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            optional_type: Type[T] = get_optional_type(type_)
            if optional_type:
                schema = context.get_schema(optional_type)
                return AnyOfSchema[T]((NullSchema(), schema))
