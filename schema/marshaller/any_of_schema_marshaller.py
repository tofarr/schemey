from dataclasses import dataclass

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schema.any_of_schema import AnyOfSchema
from schema.array_schema import ArraySchema
from schema.schema_abc import SchemaABC


@dataclass(frozen=True)
class AnyOfSchemaMarshaller(MarshallerABC[ArraySchema]):
    _schema_marshaller: MarshallerABC[SchemaABC]

    def __init__(self, schema_marshaller: MarshallerABC[SchemaABC]):
        super().__init__(ArraySchema)
        object.__setattr__(self, '_schema_marshaller', schema_marshaller)

    def load(self, item: ExternalItemType) -> AnyOfSchema:
        schemas = tuple(self._schema_marshaller.load(s) for s in item['anyOf'])
        return AnyOfSchema(schemas)

    def dump(self, schema: AnyOfSchema) -> ExternalItemType:
        dumped = dict(anyOf=[self._schema_marshaller.dump(s) for s in schema.schemas])
        return dumped
