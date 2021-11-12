from dataclasses import dataclass
from typing import Optional, List, Iterator, Type

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError

INTEGER = 'integer'
NUMBER = 'number'


@dataclass(frozen=True)
class NumberSchema(SchemaABC[T]):
    item_type: Type[T] = float
    minimum: Optional[T] = None
    exclusive_minimum: bool = False
    maximum: Optional[T] = None
    exclusive_maximum: bool = True
    default_value: Optional[T] = None

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, self.item_type):
            if not (self.item_type is float and isinstance(item, int)):
                yield SchemaError(current_path, 'type', item)
                return
        if self.minimum is not None and item < self.minimum:
            yield SchemaError(current_path, 'minimum', item)
        if self.exclusive_minimum and self.minimum is not None and item == self.minimum:
            yield SchemaError(current_path, 'exclusive_minimum', item)
        if self.maximum is not None and item > self.maximum:
            yield SchemaError(current_path, 'maximum', item)
        if self.exclusive_maximum and self.maximum is not None and item == self.maximum:
            yield SchemaError(current_path, 'exclusive_maximum', item)

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        exclusive_minimum = self.exclusive_minimum
        exclusive_maximum = self.exclusive_maximum
        return filter_none(dict(
            type=INTEGER if self.item_type is int else NUMBER,
            minimum=self.minimum,
            exclusiveMinimum=exclusive_minimum if exclusive_minimum != NumberSchema.exclusive_minimum else None,
            maximum=self.maximum,
            exclusiveMaximum=exclusive_maximum if exclusive_maximum != NumberSchema.exclusive_maximum else None
        ))
