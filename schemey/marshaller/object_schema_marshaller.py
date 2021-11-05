from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC, TYPE
from schemey.marshaller.util import filter_none
from schemey.schema_abc import SchemaABC
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema

OBJECT = 'object'


class ObjectSchemaMarshaller(SchemaMarshallerABC[ObjectSchema]):
    _property_schema_marshaller: MarshallerABC[SchemaABC]

    def __init__(self, property_schema_marshaller: MarshallerABC[SchemaABC]):
        super().__init__(ObjectSchema)
        object.__setattr__(self, '_property_schema_marshaller', property_schema_marshaller)

    def can_load(self, item: ExternalItemType) -> bool:
        return item.get(TYPE) == OBJECT

    def load(self, item: ExternalItemType) -> ObjectSchema:
        properties = item.get('properties') or {}
        required = set(item.get('required') or [])
        properties = (PropertySchema(k, self._property_schema_marshaller.load(v), k in required)
                      for k, v in properties.items())
        return ObjectSchema(tuple(properties))

    def dump(self, schema: ObjectSchema) -> ExternalItemType:
        properties = {s.name: self._property_schema_marshaller.dump(s.schema) for s in schema.property_schemas}
        required = [s.name for s in schema.property_schemas if s.required]
        return filter_none(dict(type=OBJECT, properties=properties, additionalProperties=False,
                                required=required or None))
