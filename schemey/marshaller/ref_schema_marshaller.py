from marshy.types import ExternalItemType

from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC
from schemey.ref_schema import RefSchema

REF = '$ref'
PREFIX = '#/$defs/'


class RefSchemaMarshaller(SchemaMarshallerABC[RefSchema]):
    priority = 200

    def __init__(self):
        super().__init__(RefSchema)

    def can_load(self, item: ExternalItemType) -> bool:
        return REF in item

    def load(self, item: ExternalItemType) -> RefSchema:
        ref = item[REF]
        ref = ref[len(PREFIX):]
        return RefSchema(ref)

    def dump(self, item: RefSchema) -> ExternalItemType:
        return {REF: f'{PREFIX}{item.ref}'}
