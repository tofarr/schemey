from typing import Type, Optional, Set, List, Tuple, Union

import typing_inspect
from marshy.utils import resolve_forward_refs

from schemey.array_schema import ArraySchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


class ArraySchemaFactory(SchemaFactoryABC):
    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        array_type = self.get_array_type(type_)
        if array_type:
            args = typing_inspect.get_args(type_)
            item_type = resolve_forward_refs(args[0])
            schema = json_context.get_schema(item_type)
            uniqueness = array_type is Set
            return ArraySchema(item_schema=schema, uniqueness=uniqueness)

    @staticmethod
    def get_array_type(type_: Type) -> Union[Type[List], Type[Set], Type[Tuple], None]:
        origin = typing_inspect.get_origin(type_)
        if origin is list:
            return List
        if origin is set:
            return Set
        if origin is tuple:
            args = typing_inspect.get_args(type_)
            if len(args) == 2 and args[1] is Ellipsis:
                return Tuple
