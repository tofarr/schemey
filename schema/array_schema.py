from dataclasses import dataclass
from typing import Optional, List, Iterator

from persisty.schema.schema_abc import SchemaABC, T
from persisty.schema.schema_error import SchemaError


@dataclass(frozen=True)
class ArraySchema(SchemaABC[T]):
    item_schema: Optional[SchemaABC] = None
    min_items: int = 0
    max_items: Optional[int] = None
    uniqueness: bool = False

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        if not isinstance(item, list):
            yield SchemaError(current_path, 'type', item)
            return
        if self.item_schema is not None:
            for index, i in enumerate(item):
                current_path.append(str(index))
                yield from self.item_schema.get_schema_errors(i, current_path)
                current_path.pop()
        if self.min_items is not None and len(item) < self.min_items:
            yield SchemaError(current_path, 'min_items', item)
        if self.max_items is not None and len(item) >= self.max_items:
            yield SchemaError(current_path, 'max_items', item)
        if self.uniqueness is True:
            existing = set()
            for index, i in enumerate(item):
                if i in existing:
                    current_path.append(str(index))
                    yield SchemaError(current_path, 'non_unique', i)
                    current_path.pop()
                    return
                existing.add(i)
