from dataclasses import dataclass, field
from typing import Optional, List, Iterator, Dict, Any, Callable, Type

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass
class DeferredSchema(SchemaABC):
    ref: str
    schema: Optional[SchemaABC] = field(default=None, compare=False)
    num_usages: int = 0

    def get_schema_errors(
        self, item: ExternalType, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        yield from self.schema.get_schema_errors(item, current_path)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        json_context.defs[self.ref] = self
        dumped = {"$ref": f"{json_context.defs_path}/{self.ref}"}
        return dumped

    def simplify(self) -> SchemaABC:
        if self.num_usages >= 2:
            return self
        self.num_usages = 0
        return self.schema.simplify()

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type:
        return self.schema.get_normalized_type(existing_types, object_wrapper)
