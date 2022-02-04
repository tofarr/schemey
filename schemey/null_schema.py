from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Type

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class NullSchema(JsonSchemaABC):
    default: Union[type(None), Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item is not None:
            yield SchemaError(current_path or [], 'type', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(type='null')
        if self.default is not NoDefault:
            dumped['default'] = self.default
        return dumped
