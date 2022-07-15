from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Dict, Any, Type, Callable

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError
from schemey.str_param_schema_abc import StrParamSchemaABC


@dataclass(frozen=True)
class IntegerSchema(StrParamSchemaABC):
    minimum: Optional[int] = None
    exclusive_minimum: Optional[int] = None
    maximum: Optional[int] = None
    exclusive_maximum: Optional[int] = None
    description: Optional[str] = None

    def get_schema_errors(
        self, item: int, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if not isinstance(item, int):
            yield SchemaError(current_path, "type", item)
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
        return dump_json_schema(self, "integer")

    def simplify(self) -> SchemaABC:
        kwargs = simplify_kwargs(self)
        return IntegerSchema(**kwargs)

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type[int]:
        return int


def simplify_kwargs(schema):
    kwargs = {**schema.__dict__}
    if schema.minimum is not None and schema.exclusive_minimum is not None:
        del kwargs[
            "minimum"
            if schema.minimum <= schema.exclusive_minimum
            else "exclusive_minimum"
        ]
    if schema.maximum is not None and schema.exclusive_maximum is not None:
        del kwargs[
            "maximum"
            if schema.maximum >= schema.exclusive_maximum
            else "exclusive_maximum"
        ]
    return kwargs


def dump_json_schema(item, type_name: str) -> Optional[ExternalItemType]:
    dumped = filter_none(
        dict(
            type=type_name,
            minimum=item.minimum,
            exclusiveMinimum=item.exclusive_minimum,
            maximum=item.maximum,
            exclusiveMaximum=item.exclusive_maximum,
            description=item.description,
        )
    )
    return dumped


def check(
    item: Union[float, int],
    current_path,
    minimum,
    maximum,
    exclusive_minimum,
    exclusive_maximum,
):
    if minimum is not None and item < minimum:
        yield SchemaError(current_path, "minimum", item)
    if exclusive_minimum is not None and item <= exclusive_minimum:
        yield SchemaError(current_path, "exclusive_minimum", item)
    if maximum is not None and item > maximum:
        yield SchemaError(current_path, "maximum", item)
    if exclusive_maximum is not None and item >= exclusive_maximum:
        yield SchemaError(current_path, "exclusive_maximum", item)
