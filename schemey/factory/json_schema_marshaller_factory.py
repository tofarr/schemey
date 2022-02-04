import inspect
from typing import Type, Optional

from marshy.factory.marshaller_factory_abc import MarshallerFactoryABC
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext

from schemey.json_schema_abc import JsonSchemaABC
from schemey.json_schema_marshaller import JsonSchemaMarshaller


class JsonSchemaMarshallerFactory(MarshallerFactoryABC):
    priority:int = 200

    def create(self, context: MarshallerContext, type_: Type) -> Optional[MarshallerABC]:
        if inspect.isclass(type_) and issubclass(type_, JsonSchemaABC):
            return JsonSchemaMarshaller()
