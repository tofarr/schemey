from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC
from schemey.object_schema import ObjectSchema
from schemey.schema_abc import SchemaABC
from schemey.with_defs_schema import WithDefsSchema

DEFS = '$defs'


class WithDefsSchemaMarshaller(SchemaMarshallerABC[WithDefsSchema]):
    priority = 200
    _schema_marshaller: MarshallerABC[SchemaABC]

    def __init__(self, schema_marshaller: MarshallerABC[SchemaABC]):
        super().__init__(WithDefsSchema)
        object.__setattr__(self, '_schema_marshaller', schema_marshaller)

    def can_load(self, item: ExternalItemType) -> bool:
        return DEFS in item

    def load(self, item: ExternalItemType) -> WithDefsSchema:
        raw_defs = item[DEFS]
        defs = {name: self._schema_marshaller.load(raw_schema) for name, raw_schema in raw_defs.items()}
        raw_schema = item['allOf'][0]
        schema = self._schema_marshaller.load(raw_schema)
        return WithDefsSchema(defs, schema)

    def dump(self, schema: WithDefsSchema) -> ExternalItemType:
        defs = {name: self._schema_marshaller.dump(raw_schema) for name, raw_schema in schema.defs.items()}
        schema = self._schema_marshaller.dump(schema.schema)
        return {'$defs': defs, 'allOf': [schema]}
