from dataclasses import dataclass, field
from typing import Optional, Type, List, Iterator

from marshy.types import ExternalItemType

from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC, T
from schemey.schema_context import SchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class DeferredSchema(SchemaABC[T]):
    schema_context: SchemaContext = field(repr=False)
    _item_type: Type[T]
    _default_value: T = None

    @property
    def item_type(self) -> Type[T]:
        return self._item_type

    @property
    def default_value(self) -> Optional[T]:
        return self._default_value

    @property
    def schema(self) -> SchemaABC[T]:
        return self.schema_context.get_schema(self.item_type, self.default_value)

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        yield from self.schema.get_schema_errors(item, current_path)

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        return self.schema.to_json_schema(json_output_context)
