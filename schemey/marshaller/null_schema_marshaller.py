from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC, TYPE
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema

NULL = 'null'


class NullSchemaMarshaller(SchemaMarshallerABC[NullSchema]):

    def __init__(self):
        super().__init__(NullSchema)

    def can_load(self, item: ExternalItemType) -> bool:
        return item.get(TYPE) == NULL

    def load(self, item: ExternalItemType) -> NullSchema:
        return NullSchema()

    def dump(self, item: NumberSchema) -> ExternalType:
        return dict(type=NULL)
