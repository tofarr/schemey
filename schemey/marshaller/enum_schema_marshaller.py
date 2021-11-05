from marshy.types import ExternalItemType

from schemey.enum_schema import EnumSchema
from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC

ENUM = 'enum'


class EnumSchemaMarshaller(SchemaMarshallerABC[EnumSchema]):

    def __init__(self):
        super().__init__(EnumSchema)

    def can_load(self, item: ExternalItemType) -> bool:
        return ENUM in item

    def load(self, item: ExternalItemType) -> EnumSchema:
        permitted_values = item.get(ENUM)
        return EnumSchema(tuple(permitted_values))

    def dump(self, schema: EnumSchema) -> ExternalItemType:
        permitted_values = schema.permitted_values
        return dict(enum=list(permitted_values))
