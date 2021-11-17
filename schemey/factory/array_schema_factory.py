from typing import Type, Optional

import typing_inspect

from schemey.array_schema import ArraySchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC, T
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext


class ArraySchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type, default_value, context: SchemaContext) -> Optional[SchemaABC]:
        origin = typing_inspect.get_origin(type_)
        if origin is list:
            args = typing_inspect.get_args(type_)
            schema = context.get_schema(args[0])
            return ArraySchema[T](schema, default_value=default_value)
