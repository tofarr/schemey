from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Any, Type, Callable

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC, _JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass
class ConstSchema(SchemaABC):
    """Schema representing a single constant value"""

    const: ExternalType
    description: Optional[str] = None

    def get_schema_errors(
        self, item: ExternalType, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if item != self.const:
            yield SchemaError(current_path, "invalid_value", item)

    def dump_json_schema(self, json_context: _JsonSchemaContext) -> ExternalItemType:
        dumped = dict(const=self.const)
        if self.description:
            dumped["description"] = self.description
        return dumped

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type:
        return type(self.const)
