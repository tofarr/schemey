from typing import Type, Optional, Set, List, Tuple, Union

import typing_inspect
from marshy import ExternalType

from schemey.array_schema import ArraySchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.schemey_context import SchemeyContext


class ArraySchemaFactory(SchemaFactoryABC):

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        array_type = self.get_array_type(type_)
        if array_type:
            args = typing_inspect.get_args(type_)
            schema = context.get_schema(args[0]).json_schema
            uniqueness = array_type is Set
            return ArraySchema(item_schema=schema, default_value=default_value, uniqueness=uniqueness)

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
