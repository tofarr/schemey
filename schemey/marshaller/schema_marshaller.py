from typing import Dict, Optional, Type

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.any_of_schema import AnyOfSchema
from schemey.enum_schema import EnumSchema
from schemey.marshaller.enum_schema_marshaller import EnumSchemaMarshaller
from schemey.ref_schema import RefSchema
from schemey.schema_abc import SchemaABC

TYPE = 'type'
ENUM = 'enum'
DEFS = '$defs'
REF = '$ref'
ANY_OF = 'anyOf'


class SchemaMarshaller(MarshallerABC[SchemaABC]):
    """
    Custom marshaller to json schemey format - handles polymorphism, assuming that each delegate marshaller yields
    a dict
    """
    _marshallers_by_name: Dict[Optional[str], MarshallerABC[SchemaABC]]
    _marshallers_by_type: Dict[Type, MarshallerABC[SchemaABC]]

    def __init__(self, marshallers_by_name: Dict[str, MarshallerABC[SchemaABC]]):
        super().__init__(SchemaABC)
        object.__setattr__(self, '_marshallers_by_name', marshallers_by_name)
        object.__setattr__(self, '_marshallers_by_type', {m.marshalled_type: m for m in marshallers_by_name.values()})

    def load(self, item: ExternalItemType) -> SchemaABC:
        if DEFS in item:
            from schemey.marshaller.with_defs_schema_marshaller import WithDefsSchemaMarshaller
            return WithDefsSchemaMarshaller(self).load(item)
        if ANY_OF in item:
            from schemey.marshaller.any_of_schema_marshaller import AnyOfSchemaMarshaller
            return AnyOfSchemaMarshaller(self).load(item)
        if REF in item:
            from schemey.marshaller.ref_schema_marshaller import RefSchemaMarshaller
            return RefSchemaMarshaller().load(item)
        if ENUM in item:
            return EnumSchemaMarshaller().load(item)
        type_ = item[TYPE]
        return self._load_by_type(type_, item)

    def _load_by_type(self, type_: str, item: ExternalItemType) -> SchemaABC:
        marshaller = self._marshallers_by_name[type_]
        loaded = marshaller.load(item)
        return loaded

    def dump(self, schema: SchemaABC) -> ExternalItemType:
        from schemey.with_defs_schema import WithDefsSchema
        if isinstance(schema, WithDefsSchema):
            from schemey.marshaller.with_defs_schema_marshaller import WithDefsSchemaMarshaller
            return WithDefsSchemaMarshaller(self).dump(schema)
        if isinstance(schema, AnyOfSchema):
            from schemey.marshaller.any_of_schema_marshaller import AnyOfSchemaMarshaller
            return AnyOfSchemaMarshaller(self).dump(schema)
        if isinstance(schema, RefSchema):
            from schemey.marshaller.ref_schema_marshaller import RefSchemaMarshaller
            return RefSchemaMarshaller().dump(schema)
        if isinstance(schema, EnumSchema):
            from schemey.marshaller.enum_schema_marshaller import EnumSchemaMarshaller
            return EnumSchemaMarshaller().dump(schema)
        marshaller = self._marshallers_by_type[schema.__class__]
        dumped = marshaller.dump(schema)
        return dumped
