from dataclasses import dataclass
from enum import Enum
from inspect import isclass
from typing import Type, Optional, Union

from marshy import ExternalType

from schemey.enum_schema import EnumSchema
from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schemey_context import SchemeyContext


class EnumJsonSchemaFactory(JsonSchemaFactoryABC):

    def create(self,
               type_: Type,
               json_context: JsonSchemaContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        if isclass(type_) and issubclass(type_, Enum):
            return EnumSchema(
                enum=[e.value for e in type_],
                default=default
            )
