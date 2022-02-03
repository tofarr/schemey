from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Type

from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.number_schema import check
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class IntegerSchema(JsonSchemaABC):
    minimum: Optional[int] = None
    exclusive_minimum: Optional[int] = None
    maximum: Optional[int] = None
    exclusive_maximum: Optional[int] = None
    default_value: Union[int, Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item: int, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, int):
            yield SchemaError(current_path, 'type', item)
            return
        yield from check(item, current_path, self.minimum, self.maximum, self.exclusive_minimum, self.exclusive_maximum)
