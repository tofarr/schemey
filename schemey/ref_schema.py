from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict

from schemey.schema_error import SchemaError
from schemey.schema_abc import SchemaABC, T


@dataclass(frozen=True)
class RefSchema(SchemaABC[T]):
    ref: str

    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        schema = defs[self.ref]
        yield from schema.get_schema_errors(item, defs, current_path)
