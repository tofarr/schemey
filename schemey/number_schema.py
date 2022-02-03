from dataclasses import dataclass
from typing import Optional, List, Iterator, Union

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class NumberSchema(JsonSchemaABC):
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    default_value: Union[float, NoDefault] = NoDefault

    def get_schema_errors(self, item: float, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, float) and item.__class__ is not int:
            yield SchemaError(current_path or [], 'type', item)
            return
        yield from check(item, current_path, self.minimum, self.maximum, self.exclusive_minimum, self.exclusive_maximum)


def check(item: Union[float, int], current_path, minimum, maximum, exclusive_minimum, exclusive_maximum):
    if minimum is not None and item < minimum:
        yield SchemaError(current_path, 'minimum', item)
    if exclusive_minimum is not None and item <= exclusive_minimum:
        yield SchemaError(current_path, 'exclusive_minimum', item)
    if maximum is not None and item > maximum:
        yield SchemaError(current_path, 'maximum', item)
    if exclusive_maximum is not None and item >= exclusive_maximum:
        yield SchemaError(current_path, 'exclusive_maximum', item)
