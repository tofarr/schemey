from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Iterator, Set, Dict, Any, Type, Callable

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError
from schemey.str_param_schema_abc import StrParamSchemaABC


@dataclass(frozen=True)
class EnumSchema(StrParamSchemaABC):
    name: str
    enum: Set[ExternalType]
    description: Optional[str] = None

    def get_schema_errors(
        self, item: ExternalType, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        if item not in self.enum:
            yield SchemaError(current_path or [], "value_not_permitted", item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = dict(name=self.name, enum=list(self.enum))
        if self.description:
            dumped["description"] = self.description
        return dumped

    def get_normalized_type(
        self, existing_types: Dict[str, Any], object_wrapper: Callable
    ) -> Type:
        type_ = existing_types.get(self.name)
        if type_:
            return type_
        attributes = {str(e): e for e in self.enum}
        type_ = Enum(self.name, attributes)
        existing_types[self.name] = type_
        return type_
