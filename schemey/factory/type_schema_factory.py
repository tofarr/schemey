from dataclasses import dataclass
from typing import Type, Optional, Callable, Union

from marshy import ExternalType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schemey_context import SchemeyContext


@dataclass
class TypeSchemaFactory(SchemaFactoryABC):
    item_type: Type
    constructor: Callable[..., JsonSchemaABC]

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        if self.item_type == type_:
            return self.constructor(default_value=default_value)
