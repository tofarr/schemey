from dataclasses import dataclass
from typing import Optional, List, Iterator, Set

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class EnumSchema(SchemaABC):
    enum: Set[ExternalType]

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item not in self.enum:
            yield SchemaError(current_path or [], 'value_not_permitted', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(enum=list(self.enum))
        return dumped
