from typing import Dict, Iterable, Optional, Type

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from persisty.schema.any_of_schema import AnyOfSchema
from persisty.schema.enum_schema import EnumSchema
from persisty.schema.schema_abc import SchemaABC

TYPE = 'type'
ENUM = 'enum'


class SchemaMarshaller(MarshallerABC[SchemaABC]):
    """
    Custom marshaller to json schema format - handles polymorphism, assuming that each delegate marshaller yields
    a dict
    """
    _marshallers_by_name: Dict[Optional[str], MarshallerABC[SchemaABC]]
    _marshallers_by_type: Dict[Type, MarshallerABC[SchemaABC]]

    def __init__(self, marshallers_by_name: Dict[str, MarshallerABC[SchemaABC]]):
        super().__init__(SchemaABC)
        object.__setattr__(self, '_marshallers_by_name', marshallers_by_name)
        object.__setattr__(self, '_marshallers_by_type', {m.marshalled_type: m for m in marshallers_by_name.values()})

    def load(self, item: ExternalItemType) -> SchemaABC:
        enum = item.get(ENUM)
        if enum:
            return EnumSchema(tuple(enum))
        type_ = item[TYPE]
        if type_ is None or isinstance(type_, str):
            return self._load_by_type(type_, item)
        return self._load_any_of(type_, item)

    def _load_by_type(self, type_: str, item: ExternalItemType) -> SchemaABC:
        marshaller = self._marshallers_by_name[type_]
        loaded = marshaller.load(item)
        return loaded

    def _load_any_of(self, types: Iterable[str], item: ExternalItemType):
        item = {**item}
        schemas = []
        for type_ in types:
            item[TYPE] = type_
            schemas.append(self._load_by_type(type_, item))
        return AnyOfSchema(tuple(schemas))

    def dump(self, schema: SchemaABC) -> ExternalItemType:
        if isinstance(schema, EnumSchema):
            return dict(enum=list(schema.permitted_values))
        if isinstance(schema, AnyOfSchema):
            types = []
            item = {}
            for s in schema.schemas:
                dumped = self.dump(s)
                item.update(dumped)
                sub_type = dumped[TYPE]
                if sub_type is None or isinstance(sub_type, str):
                    types.append(sub_type)
                else:
                    types.extend(sub_type)
            item[TYPE] = types
            return item
        else:
            marshaller = self._marshallers_by_type[schema.__class__]
            dumped = marshaller.dump(schema)
            return dumped
