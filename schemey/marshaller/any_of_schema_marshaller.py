from dataclasses import dataclass

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.any_of_schema import AnyOfSchema
from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC
from schemey.schema_abc import SchemaABC

ANY_OF = 'anyOf'


@dataclass(frozen=True)
class AnyOfSchemaMarshaller(SchemaMarshallerABC[AnyOfSchema]):

    _schema_marshaller: MarshallerABC[SchemaABC]

    def __init__(self, schema_marshaller: MarshallerABC[SchemaABC]):
        super().__init__(AnyOfSchema)
        object.__setattr__(self, '_schema_marshaller', schema_marshaller)

    def can_load(self, item: ExternalItemType) -> bool:
        return ANY_OF in item

    def load(self, item: ExternalItemType) -> AnyOfSchema:
        schemas = tuple(self._schema_marshaller.load(s) for s in item[ANY_OF])
        return AnyOfSchema(schemas)

    def dump(self, schema: AnyOfSchema) -> ExternalItemType:
        dumped = dict(anyOf=[self._schema_marshaller.dump(s) for s in schema.schemas])
        return dumped
