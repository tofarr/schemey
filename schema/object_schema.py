from dataclasses import dataclass, field
from typing import Iterable, Union, Sized, Optional, List, Iterator

from persisty.schema.property_schema import PropertySchema
from persisty.schema.schema_error import SchemaError
from persisty.schema.schema_abc import SchemaABC, T


@dataclass(frozen=True)
class ObjectSchema(SchemaABC[T]):
    property_schemas: Union[Iterable[PropertySchema], Sized] = field(default_factory=tuple)

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        for property_validator in (self.property_schemas or []):
            yield from property_validator.get_schema_errors(item, current_path)
