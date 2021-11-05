from dataclasses import dataclass

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.array_schema import ArraySchema
from schemey.marshaller.schema_marshaller_abc import TYPE, SchemaMarshallerABC
from schemey.marshaller.util import filter_none
from schemey.schema_abc import SchemaABC

ARRAY = 'array'


@dataclass(frozen=True)
class ArraySchemaMarshaller(SchemaMarshallerABC[ArraySchema]):
    _marshaller: MarshallerABC[SchemaABC]

    def __init__(self, marshaller: MarshallerABC[SchemaABC]):
        super().__init__(ArraySchema)
        object.__setattr__(self, '_marshaller', marshaller)

    def can_load(self, item: ExternalItemType) -> bool:
        return item.get(TYPE) == ARRAY
    
    def load(self, item: ExternalItemType) -> ArraySchema:
        item_schema = self._marshaller.load(item['items']) if 'items' in item else None
        return ArraySchema(
            item_schema=item_schema,
            min_items=int(item['minItems']) if 'minItems' in item else None,
            max_items=int(item['maxItems']) if 'maxItems' in item else None,
            uniqueness=item.get('uniqueness') is True
        )

    def dump(self, schema: ArraySchema) -> ExternalItemType:
        return filter_none(dict(
            type=ARRAY,
            items=self._marshaller.dump(schema.item_schema) if schema.item_schema else None,
            minItems=schema.min_items or None,
            maxItems=schema.max_items,
            uniqueness=schema.uniqueness or None
        ))
