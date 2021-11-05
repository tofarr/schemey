from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable

from marshy import ExternalType

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError


@dataclass(frozen=True)
class EnumSchema(SchemaABC):
    permitted_values: Iterable[ExternalType]

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item not in self.permitted_values:
            yield SchemaError(current_path or [], 'value_not_permitted', item)
