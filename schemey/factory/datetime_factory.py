from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Type, Dict

from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema, datetime_schema
from schemey.schema_context import SchemaContext
from schemey.string_format import StringFormat


@dataclass
class DatetimeFactory(SchemaFactoryABC):
    priority: int = 210

    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        if type_ is datetime:
            return datetime_schema()

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        if (
            item.get("type") == "string"
            and item.get("format") == StringFormat.DATE_TIME.value
        ):
            return Schema(item, datetime)
