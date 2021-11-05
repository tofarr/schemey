from typing import Optional, Iterable

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC
from schemey.schema_abc import SchemaABC

TYPE = 'type'
ENUM = 'enum'
DEFS = '$defs'
REF = '$ref'
ANY_OF = 'anyOf'


class SchemaMarshaller(MarshallerABC[SchemaABC]):
    """
    Custom marshaller to json schemey format - handles polymorphism, assuming that each delegate marshaller yields
    a dict
    """
    _marshallers: Iterable[SchemaMarshallerABC]
    _marshallers_by_type: Iterable[SchemaMarshallerABC]

    def __init__(self, schema_marshallers: Optional[Iterable[SchemaMarshallerABC]] = None):
        super().__init__(SchemaABC)
        schema_marshallers = list(schema_marshallers or [])
        schema_marshallers.sort()
        marshallers_by_type = {m.marshalled_type: m for m in schema_marshallers}
        schema_marshallers.sort(reverse=True)
        object.__setattr__(self, '_marshallers', schema_marshallers)
        object.__setattr__(self, '_marshallers_by_type', marshallers_by_type)

    @property
    def schema_marshallers(self):
        return list(self._marshallers)

    def load(self, item: ExternalItemType) -> SchemaABC:
        for schema_marshaller in self._marshallers:
            if schema_marshaller.can_load(item):
                loaded = schema_marshaller.load(item)
                return loaded
        raise ValueError(f'unloadable:{item}')

    def dump(self, schema: SchemaABC) -> ExternalItemType:
        marshaller = self._marshallers_by_type[type(schema)]
        dumped = marshaller.dump(schema)
        return dumped
