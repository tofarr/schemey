from dataclasses import dataclass
from typing import Optional, List, Iterator, TypeVar

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError

T = TypeVar('T')


@dataclass(frozen=True)
class ArraySchema(SchemaABC[List[T]]):
    item_schema: Optional[SchemaABC[T]] = None
    min_items: int = 0
    max_items: Optional[int] = None
    uniqueness: bool = False

    def get_schema_errors(self,
                          items: List[T],
                          current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        if not isinstance(items, list):
            yield SchemaError(current_path, 'type', items)
            return
        if self.item_schema is not None:
            for index, item in enumerate(items):
                current_path.append(str(index))
                yield from self.item_schema.get_schema_errors(item, current_path)
                current_path.pop()
        if self.min_items is not None and len(items) < self.min_items:
            yield SchemaError(current_path, 'min_items', items)
        if self.max_items is not None and len(items) >= self.max_items:
            yield SchemaError(current_path, 'max_items', items)
        if self.uniqueness is True:
            existing = set()
            for index, item in enumerate(items):
                if item in existing:
                    current_path.append(str(index))
                    yield SchemaError(current_path, 'non_unique', item)
                    current_path.pop()
                    return
                existing.add(item)
