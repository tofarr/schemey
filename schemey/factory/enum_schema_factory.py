from dataclasses import dataclass
from enum import Enum
from inspect import isclass
from typing import Type, Optional, Dict

from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


@dataclass
class EnumSchemaFactory(SchemaFactoryABC):
    priority: int = 190

    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        if isclass(type_) and issubclass(type_, Enum):
            # noinspection PyTypeChecker
            schema = dict(name=type_.__name__, enum=[e.value for e in type_])
            return Schema(schema, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        name = item.get("name")
        enum = item.get("enum")
        if name and enum and isinstance(enum, list):
            if next((False for e in enum if not isinstance(e, str)), True):
                type_ = Enum(name, {e: e for e in enum})
                return Schema(item, type_)
