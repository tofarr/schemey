from typing import Type, Optional

import typing_inspect

from persisty.schema.array_schema import ArraySchema
from persisty.schema.factory.schema_factory_abc import SchemaFactoryABC, T
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_context import SchemaContext


class ArraySchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        origin = typing_inspect.get_origin(type_)
        if origin is list:
            args = typing_inspect.get_args(type_)
            schema = context.get_schema(args[0])
            return ArraySchema[T](schema)
