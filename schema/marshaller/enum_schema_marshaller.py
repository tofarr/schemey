from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schema.enum_schema import EnumSchema


class EnumSchemaMarshaller(MarshallerABC[EnumSchema]):

    def __init__(self):
        super().__init__(EnumSchema)

    def load(self, item: ExternalItemType) -> EnumSchema:
        permitted_values = item.get('enum')
        return EnumSchema(tuple(permitted_values))

    def dump(self, schema: EnumSchema) -> ExternalItemType:
        permitted_values = schema.permitted_values
        return dict(enum=list(permitted_values))
