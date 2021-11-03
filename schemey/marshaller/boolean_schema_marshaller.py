from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from persisty.schema.boolean_schema import BooleanSchema


class BooleanSchemaMarshaller(MarshallerABC[BooleanSchema]):

    def __init__(self):
        super().__init__(BooleanSchema)

    def load(self, item: ExternalItemType) -> BooleanSchema:
        return BooleanSchema()

    def dump(self, item: BooleanSchema) -> ExternalItemType:
        return dict(type='boolean')
