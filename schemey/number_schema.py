from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Any, Type, Callable

from marshy.types import ExternalItemType

from schemey.integer_schema import check, dump_json_schema, simplify_kwargs
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.str_param_schema_abc import StrParamSchemaABC


@dataclass(frozen=True)
class NumberSchema(StrParamSchemaABC):
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    description: Optional[str] = None

    def get_schema_errors(
        self, item: float, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if not isinstance(item, float) and item.__class__ is not int:
            yield SchemaError(current_path or [], "type", item)
            return
        yield from check(
            item,
            current_path,
            self.minimum,
            self.maximum,
            self.exclusive_minimum,
            self.exclusive_maximum,
        )

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        return dump_json_schema(self, "number")

    def simplify(self) -> SchemaABC:
        kwargs = simplify_kwargs(self)
        return NumberSchema(**kwargs)

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type[float]:
        return float
