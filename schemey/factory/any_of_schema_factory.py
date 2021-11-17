from typing import Type, Optional, Union

import typing_inspect

from schemey.any_of_schema import AnyOfSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC, T, NONE_TYPE
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext


class AnyOfSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], default_value, context: SchemaContext) -> Optional[SchemaABC[T]]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            args = typing_inspect.get_args(type_)
            # noinspection PyPep8
            if len(args) == 2 and args[1] == NONE_TYPE:
                args = (args[1], args[0])  # None checks are faster so make sure they are first
            schemas = tuple(context.get_schema(a) for a in args)
            return AnyOfSchema[T](schemas, default_value=default_value)
