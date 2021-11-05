from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.ref_schema import RefSchema

PREFIX = '#/$defs/'


class RefSchemaMarshaller(MarshallerABC[RefSchema]):

    def __init__(self):
        super().__init__(RefSchema)

    def load(self, item: ExternalItemType) -> RefSchema:
        ref = item['$ref']
        ref = ref[len(PREFIX):]
        return RefSchema(ref)

    def dump(self, item: RefSchema) -> ExternalItemType:
        return {'$ref': f'{PREFIX}{item.ref}'}
