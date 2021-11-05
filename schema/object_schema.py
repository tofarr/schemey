from dataclasses import dataclass, field
from typing import Iterable, Union, Sized, Optional, List, Iterator, Type, Dict

from schema.property_schema import PropertySchema
from schema.schema_error import SchemaError
from schema.schema_abc import SchemaABC, T


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
