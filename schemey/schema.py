from dataclasses import dataclass
from typing import Optional, Type, List, Iterator

from marshy.marshaller.marshaller_abc import MarshallerABC

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError


@dataclass
class Schema(SchemaABC[T]):
    """ Implementation of SchemaABC using Json """
    json_schema: JsonSchemaABC
    marshaller: MarshallerABC[T]

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        dumped = self.marshaller.dump(item)
        yield from self.json_schema.get_schema_errors(dumped, current_path)

    @property
    def item_type(self) -> Type[T]:
        return self.marshaller.marshalled_type

    @property
    def default_value(self) -> Optional[T]:
        default_value = self.json_schema.default_value
        if default_value is NoDefault:
            return None
        loaded = self.marshaller.load(default_value)
        return loaded
