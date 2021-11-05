from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from persisty.schema.null_schema import NullSchema
from persisty.schema.number_schema import NumberSchema


class NullSchemaMarshaller(MarshallerABC[NullSchema]):

    def __init__(self):
        super().__init__(NullSchema)

    def load(self, item: ExternalItemType) -> NullSchema:
        return NullSchema()

    def dump(self, item: NumberSchema) -> ExternalType:
        return dict(type=None)
