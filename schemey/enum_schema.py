from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Iterable, Type

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class EnumSchema(JsonSchemaABC):
    enum: Iterable[ExternalType]
    default: Union[ExternalType, Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item not in self.enum:
            yield SchemaError(current_path or [], 'value_not_permitted', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(enum=self.enum)
        if self.default is not NoDefault:
            dumped['default'] = self.default
        return dumped
