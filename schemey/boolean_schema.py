from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Type

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class BooleanSchema(JsonSchemaABC):
    default: Union[bool, Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item: bool, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, bool):
            yield SchemaError(current_path or [], 'type', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(type='boolean')
        if self.default is not NoDefault:
            dumped['default'] = self.default
        return dumped
