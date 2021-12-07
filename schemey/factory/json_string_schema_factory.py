from dataclasses import dataclass
from typing import Type, Optional, Union

import typing_inspect

from schemey.factory.schema_factory_abc import SchemaFactoryABC, T
from schemey.json_string_schema import JsonStringSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext


@dataclass(frozen=True)
class JsonStringSchemaFactory(SchemaFactoryABC):
    priority = 110

    def create(self, type_: Type[T], default_value: Optional[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        if _is_match_type(type_):
            schema = JsonStringSchema(type_, default_value)
            return schema


def _is_match_type(type_) -> bool:
    # The type we are looking or will have a forward ref to marshy.types.ExternalType in there somewhere
    if typing_inspect.is_forward_ref(type_):
        forward_ref = type_.__forward_arg__
        return forward_ref == 'marshy.types.ExternalType'
    origin = typing_inspect.get_origin(type_)
    if origin is dict:
        args = typing_inspect.get_args(type_)
        if args[0] is not str:
            return False
        return _is_match_type(args[1])
    elif origin is list:
        args = typing_inspect.get_args(type_)
        return _is_match_type(args[0])
    elif origin == Union:
        for a in typing_inspect.get_args(type_):
            if _is_match_type(a):
                return True
    return False
