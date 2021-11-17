from dataclasses import dataclass
from typing import Optional, List, Iterator, Type
from uuid import UUID

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC
from schemey.string_format import StringFormat
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class UuidSchema(SchemaABC[UUID]):
    default_value: Optional[UUID] = None

    @property
    def item_type(self) -> Type[UUID]:
        return UUID

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        return filter_none(dict(
            type='string',
            format=StringFormat.UUID.value,
            default=None if self.default_value is None else str(self.default_value)
        ))

    def get_schema_errors(self, item: UUID, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, UUID):
            yield SchemaError(current_path, 'type', item)
