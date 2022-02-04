from typing import Type, Optional, Set, List, Tuple, Union

import typing_inspect
from marshy import ExternalType

from schemey.array_schema import ArraySchema
from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.json_schema_context import JsonSchemaContext


class ArrayJsonSchemaFactory(JsonSchemaFactoryABC):

    def create(self,
               type_: Type,
               json_context: JsonSchemaContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        array_type = self.get_array_type(type_)
        if array_type:
            args = typing_inspect.get_args(type_)
            schema = json_context.create_schema(args[0])
            uniqueness = array_type is Set
            return ArraySchema(item_schema=schema, default=default, uniqueness=uniqueness)

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
