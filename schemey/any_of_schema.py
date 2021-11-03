from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Sized, Union

from persisty.schema.null_schema import NullSchema
from persisty.schema.schema_abc import SchemaABC, T
from persisty.schema.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(SchemaABC[T]):
    schemas: Iterable[Union[SchemaABC[T], Sized]]

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        errors = [SchemaError(current_path or [], 'type', item)]
        for schema in self.schemas:
            errors = list(schema.get_schema_errors(item, current_path))
            if not errors:
                return
        if item is not None:
            yield from errors


def optional_schema(schema: SchemaABC[T]) -> SchemaABC[T]:
    return AnyOfSchema((NullSchema(), schema))

