from typing import Type, Optional, Dict

import typing_inspect

from schema.array_schema import ArraySchema
from schema.factory.schema_factory_abc import SchemaFactoryABC, T
from schema.schema_abc import SchemaABC
from schema.schema_context import SchemaContext


class ArraySchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type, context: SchemaContext, defs: Dict[str, SchemaABC]) -> Optional[SchemaABC]:
        origin = typing_inspect.get_origin(type_)
        if origin is list:
            args = typing_inspect.get_args(type_)
            schema = context.get_schema(args[0], defs)
            return ArraySchema[T](schema)
