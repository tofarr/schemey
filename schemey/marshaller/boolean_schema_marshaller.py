from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.boolean_schema import BooleanSchema
from schemey.marshaller.schema_marshaller_abc import TYPE, SchemaMarshallerABC

BOOLEAN = 'boolean'


class BooleanSchemaMarshaller(SchemaMarshallerABC[BooleanSchema]):

    def __init__(self):
        super().__init__(BooleanSchema)

    def can_load(self, item: ExternalItemType) -> bool:
        return item.get(TYPE) == BOOLEAN

    def load(self, item: ExternalItemType) -> BooleanSchema:
        return BooleanSchema()

    def dump(self, item: BooleanSchema) -> ExternalItemType:
        return dict(type=BOOLEAN)
