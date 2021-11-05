from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Type, TypeVar

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError

T = TypeVar('T', bound=Union[int, float])


@dataclass(frozen=True)
class NumberSchema(SchemaABC[T]):
    item_type: Type[T] = float
    minimum: Optional[T] = None
    exclusive_minimum: bool = False
    maximum: Optional[T] = None
    exclusive_maximum: bool = True

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, self.item_type):
            if not isinstance(item, int):
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
