from dataclasses import dataclass
from typing import Optional, List, Iterator

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError

ARRAY = 'array'


@dataclass(frozen=True)
class ArraySchema(SchemaABC[List[T]]):
    item_schema: Optional[SchemaABC[T]] = None
    min_items: int = 0
    max_items: Optional[int] = None
    uniqueness: bool = False
    default_value: Optional[List[T]] = None

    @property
    def item_type(self):
        return List[self.item_schema.item_type]

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        json_schema = filter_none(dict(type=ARRAY,
                                       items=self.item_schema.to_json_schema(json_output_context),
                                       minItems=self.min_items or None,
                                       maxItems=self.max_items,
                                       uniqueness=self.uniqueness or None))
        return json_schema

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
