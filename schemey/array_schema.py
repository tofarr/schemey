from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Any, Type, Set, Callable

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class ArraySchema(SchemaABC):
    item_schema: Optional[SchemaABC] = None
    min_items: int = 0
    max_items: Optional[int] = None
    uniqueness: bool = False
    description: str = None

    def get_schema_errors(
        self, item: List[ExternalItemType], current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        if not isinstance(item, list):
            yield SchemaError(current_path, "type", item)
            return
        if self.item_schema is not None:
            for index, i in enumerate(item):
                current_path.append(str(index))
                yield from self.item_schema.get_schema_errors(i, current_path)
                current_path.pop()
        if self.min_items is not None and len(item) < self.min_items:
            yield SchemaError(current_path, "min_items", item)
        if self.max_items is not None and len(item) >= self.max_items:
            yield SchemaError(current_path, "max_items", item)
        if self.uniqueness is True:
            existing = set()
            for index, i in enumerate(item):
                if i in existing:
                    current_path.append(str(index))
                    yield SchemaError(current_path, "non_unique", i)
                    current_path.pop()
                    return
                existing.add(i)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        items = (
            self.item_schema.dump_json_schema(json_context)
            if self.item_schema
            else None
        )
        dumped = filter_none(
            dict(
                type="array",
                items=items,
                maxItems=self.max_items,
                description=self.description,
            )
        )
        if self.min_items:
            dumped["minItems"] = self.min_items
        if self.uniqueness:
            dumped["uniqueness"] = True
        return dumped

    def simplify(self) -> SchemaABC:
        item_schema = self.item_schema.simplify()
        schema = ArraySchema(**{**self.__dict__, "item_schema": item_schema})
        return schema

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type:
        item_type = self.item_schema.get_normalized_type(existing_types, object_wrapper)
        if self.uniqueness:
            return Set[item_type]
        else:
            return List[item_type]
