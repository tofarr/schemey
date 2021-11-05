from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Dict

from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class EnumSchema(SchemaABC[T]):
    permitted_values: Iterable[T]

    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        value = getattr(item, 'value', item)
        if value not in self.permitted_values:
            yield SchemaError(current_path or [], 'value_not_permitted', item)
