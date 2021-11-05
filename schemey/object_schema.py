from dataclasses import dataclass, field
from typing import Iterable, Union, Sized, Optional, List, Iterator, Dict

from schemey.property_schema import PropertySchema
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class ObjectSchema(SchemaABC[T]):
    property_schemas: Union[Iterable[PropertySchema], Sized] = field(default_factory=tuple)

    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        for property_schema in (self.property_schemas or []):
            yield from property_schema.get_schema_errors(item, defs, current_path)
