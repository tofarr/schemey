from dataclasses import dataclass
from typing import Optional, List, Iterator, Union

from marshy.types import ExternalItemType

from schemey.integer_schema import check, dump_json_schema, simplify_kwargs
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class NumberSchema(JsonSchemaABC):
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    default: Union[float, NoDefault] = NoDefault

    def get_schema_errors(self, item: float, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, float) and item.__class__ is not int:
            yield SchemaError(current_path or [], 'type', item)
            return
        yield from check(item, current_path, self.minimum, self.maximum, self.exclusive_minimum, self.exclusive_maximum)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        return dump_json_schema(self, 'number')

    def simplify(self) -> JsonSchemaABC:
        kwargs = simplify_kwargs(self)
        return NumberSchema(**kwargs)
