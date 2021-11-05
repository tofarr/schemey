from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict

from schemey.schema_error import SchemaError
from schemey.schema_abc import SchemaABC, T


@dataclass(frozen=True)
class WithDefsSchema(SchemaABC[T]):
    defs: Dict[str, SchemaABC]
    schema: SchemaABC

    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        yield from self.schema.get_schema_errors(item, self.defs, current_path)
