from dataclasses import dataclass

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from persisty.schema.array_schema import ArraySchema
from persisty.schema.marshaller.util import filter_none
from persisty.schema.schema_abc import SchemaABC


@dataclass(frozen=True)
class ArraySchemaMarshaller(MarshallerABC[ArraySchema]):
    _item_schema_marshaller: MarshallerABC[SchemaABC]

    def __init__(self, item_schema_marshaller: MarshallerABC[SchemaABC]):
        super().__init__(ArraySchema)
        object.__setattr__(self, '_item_schema_marshaller', item_schema_marshaller)

    def load(self, item: ExternalItemType) -> ArraySchema:
        item_schema = self._item_schema_marshaller.load(item['items']) if 'items' in item else None
        return ArraySchema(
            item_schema=item_schema,
            min_items=int(item['minItems']) if 'minItems' in item else None,
            max_items=int(item['maxItems']) if 'maxItems' in item else None,
            uniqueness=item.get('uniqueness') is True
        )

    def dump(self, schema: ArraySchema) -> ExternalItemType:
        return filter_none(dict(
            type='array',
            items=self._item_schema_marshaller.dump(schema.item_schema) if schema.item_schema else None,
            minItems=schema.min_items or None,
            maxItems=schema.max_items,
            uniqueness=schema.uniqueness or None
        ))
