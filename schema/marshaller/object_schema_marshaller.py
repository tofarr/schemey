from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.object_schema import ObjectSchema
from persisty.schema.property_schema import PropertySchema


class ObjectSchemaMarshaller(MarshallerABC[ObjectSchema]):
    _property_schema_marshaller: MarshallerABC[SchemaABC]

    def __init__(self, property_schema_marshaller: MarshallerABC[SchemaABC]):
        super().__init__(ObjectSchema)
        object.__setattr__(self, '_property_schema_marshaller', property_schema_marshaller)

    def load(self, item: ExternalItemType) -> ObjectSchema:
        properties = item.get('properties') or {}
        properties = (PropertySchema(k, self._property_schema_marshaller.load(v)) for k, v in properties.items())
        return ObjectSchema(tuple(properties))

    def dump(self, schema: ObjectSchema) -> ExternalItemType:
        properties = {s.name: self._property_schema_marshaller.dump(s.schema) for s in schema.property_schemas}
        return dict(type='object', properties=properties)
