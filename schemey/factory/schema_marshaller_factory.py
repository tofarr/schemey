import inspect
from dataclasses import dataclass
from typing import Type, Optional

from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext

from schemey.schema_abc import SchemaABC
from schemey.schema_marshaller import SchemaMarshaller
from schemey.schemey_context import SchemeyContext, get_default_schemey_context


@dataclass(frozen=True)
class SchemaMarshallerFactory(MarshallerFactoryABC):
    priority:int = 200
    schemey_context: Optional[SchemeyContext] = None

    def create(self, context: MarshallerContext, type_: Type) -> Optional[MarshallerABC]:
        if inspect.isclass(type_) and issubclass(type_, SchemaABC):
            schemey_context = self.schemey_context or get_default_schemey_context()
            return SchemaMarshaller(schemey_context=schemey_context)
