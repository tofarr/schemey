from typing import Type, Optional, Union

import typing_inspect

from schemey.any_of_schema import AnyOfSchema
from schemey.const_schema import ConstSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.tuple_schema import TupleSchema


class AnyOfSchemaFactory(SchemaFactoryABC):
    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            args = typing_inspect.get_args(type_)
            schemas = tuple(
                TupleSchema((ConstSchema(a.__name__), json_context.get_schema(a)))
                for a in args
            )
            return AnyOfSchema(schemas)
