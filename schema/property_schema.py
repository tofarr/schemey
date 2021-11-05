from dataclasses import dataclass
from typing import TypeVar, Generic, Iterator, Optional, List, Type, Dict

from schema.schema_error import SchemaError
from schema.schema_abc import SchemaABC, T

B = TypeVar('B')


@dataclass(frozen=True)
class PropertySchema(Generic[T, B], SchemaABC[T]):
    name: str
    schema: SchemaABC

    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        attr = getattr(item, self.name, None)
        current_path.append(self.name)
        yield from self.schema.get_schema_errors(attr, defs, current_path)
        current_path.pop()
