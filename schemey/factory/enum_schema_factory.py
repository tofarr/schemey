from dataclasses import dataclass
from enum import Enum
from inspect import isclass
from typing import Type, Optional, Union

from marshy import ExternalType

from schemey.enum_schema import EnumSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schemey_context import SchemeyContext


class EnumSchemaFactory(SchemaFactoryABC):

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        if isclass(type_) and issubclass(type_, Enum):
            return EnumSchema(
                enum=[e.value for e in type_],
                default_value=default_value
            )
