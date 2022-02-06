import copy
from dataclasses import dataclass, MISSING
from typing import Optional, List, Iterator, Union, Type

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


class NoDefault:
    pass


@dataclass
class OptionalSchema(SchemaABC):
    """
    Attributes can be optional or required. ObjectSchemas contain a list of required property names,
    and all other properties should be Optional - and may have a default value (NoDefault is used
    for dynamic defaults - e.g.: field(default_factory=uuid4)
    """
    schema: SchemaABC
    default: Union[ExternalType, Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item is not None and item is not MISSING:
            yield from self.schema.get_schema_errors(item, current_path)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        schema = self.schema.dump_json_schema(json_context)
        if self.default is not NoDefault:
            schema['default'] = copy.deepcopy(self.default)
        return schema

    def simplify(self) -> SchemaABC:
        schema = OptionalSchema(self.schema.simplify(), self.default)
        return schema
