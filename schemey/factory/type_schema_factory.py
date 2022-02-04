from dataclasses import dataclass
from typing import Type, Optional, Callable, Union

from marshy import ExternalType

from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schemey_context import SchemeyContext


@dataclass
class TypeJsonSchemaFactory(JsonSchemaFactoryABC):
    item_type: Type
    constructor: Callable[..., JsonSchemaABC]

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        if self.item_type == type_:
            return self.constructor(default=default)
