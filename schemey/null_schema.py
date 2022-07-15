from dataclasses import dataclass
from typing import Optional, List, Iterator, Any, Dict, Type, Callable

from marshy.types import ExternalItemType

from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

_instance = None


@dataclass(frozen=True)
class NullSchema(SchemaABC):
    def __new__(cls, *args, **kwargs):
        global _instance
        if not _instance:
            _instance = super(NullSchema, cls).__new__(cls, *args, **kwargs)
        return _instance

    def get_schema_errors(
        self, item, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if item is not None:
            yield SchemaError(current_path or [], "type", item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(type="null")
        return dumped

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type:
        return type(None)
