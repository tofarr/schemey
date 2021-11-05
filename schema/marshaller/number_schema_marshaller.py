from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from persisty.schema.marshaller.util import filter_none
from persisty.schema.number_schema import NumberSchema


class NumberSchemaMarshaller(MarshallerABC[NumberSchema]):

    def __init__(self):
        super().__init__(NumberSchema)

    def load(self, item: ExternalItemType) -> NumberSchema:
        item_type = item['type']
        item_type = int if item_type == 'integer' else float
        return NumberSchema(
            item_type=item_type,
            minimum=item_type(item['minimum']) if item.get('minimum') is not None else None,
            exclusive_minimum=item.get('exclusiveMinimum') is True,
            maximum=item_type(item['maximum']) if 'maximum' in item else None,
            exclusive_maximum=item.get('exclusiveMaximum') in [True, None],
        )

    def dump(self, item: NumberSchema) -> ExternalType:
        exclusive_minimum = item.exclusive_minimum
        exclusive_maximum = item.exclusive_maximum
        return filter_none(dict(
            type='integer' if item.item_type is int else 'number',
            minimum=item.minimum,
            exclusiveMinimum=exclusive_minimum if exclusive_minimum != NumberSchema.exclusive_minimum else None,
            maximum=item.maximum,
            exclusiveMaximum=exclusive_maximum if exclusive_maximum != NumberSchema.exclusive_maximum else None
        ))
