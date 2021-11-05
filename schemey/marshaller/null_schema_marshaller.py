from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema


class NullSchemaMarshaller(MarshallerABC[NullSchema]):

    def __init__(self):
        super().__init__(NullSchema)

    def load(self, item: ExternalItemType) -> NullSchema:
        return NullSchema()

    def dump(self, item: NumberSchema) -> ExternalType:
        return dict(type="null")
