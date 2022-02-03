from typing import Type, Optional, Union

import typing_inspect
from marshy import ExternalType

from schemey.any_of_schema import AnyOfSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC, NONE_TYPE
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.schemey_context import SchemeyContext


class AnyOfSchemaFactory(SchemaFactoryABC):

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            args = typing_inspect.get_args(type_)
            # noinspection PyPep8
            if len(args) == 2 and args[1] == NONE_TYPE:
                args = (args[1], args[0])  # None checks are faster so make sure they are first
            schemas = tuple(context.get_schema(a).json_schema for a in args)
            return AnyOfSchema(schemas, default_value=default_value)
