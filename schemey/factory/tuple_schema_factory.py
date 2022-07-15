from typing import Type, Optional

import typing_inspect

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.tuple_schema import TupleSchema


class TupleSchemaFactory(SchemaFactoryABC):
    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        origin = typing_inspect.get_origin(type_)
        if origin is tuple:
            args = typing_inspect.get_args(type_)
            if len(args) == 2 and args[1] is Ellipsis:
                return
            schema = TupleSchema(tuple(json_context.get_schema(s) for s in args))
            return schema
