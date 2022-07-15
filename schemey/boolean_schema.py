from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Tuple, Union, Any, Type, Callable

from marshy.types import ExternalItemType, ExternalType

from schemey.json_schema_context import JsonSchemaContext
from schemey.optional_schema import NoDefault
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

_instance = None


@dataclass(frozen=True)
class BooleanSchema(SchemaABC):
    description: str = None

    def get_schema_errors(
        self, item: bool, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if not isinstance(item, bool):
            yield SchemaError(current_path or [], "type", item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(type="boolean")
        if self.description:
            dumped["description"] = self.description
        return dumped

    def get_param_schemas(self, current_path: str) -> List[ParamSchema]:
        return [ParamSchema(name=current_path, schema=self)]

    def from_url_params(
        self, current_path: str, params: Dict[str, List[str]]
    ) -> Union[ExternalType, NoDefault]:
        if current_path not in params:
            return NoDefault
        values = params.get(current_path)
        value = values[0].lower() not in ["", "0", "0.0", "false"]
        return value

    def to_url_params(self, current_path: str, item: bool) -> Iterator[Tuple[str, str]]:
        value = "1" if item else "0"
        yield current_path, value

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type[bool]:
        return bool
