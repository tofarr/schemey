from dataclasses import dataclass
from typing import Type, Optional

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

from schemey import Schema, get_default_schema_context, SchemaContext


@dataclass(frozen=True)
class SchemaMarshaller(MarshallerABC[Schema]):
    marshalled_type: Type[Schema] = Schema
    context: Optional[SchemaContext] = None

    def load(self, item: ExternalType) -> Schema:
        context = self.context or get_default_schema_context()
        loaded = context.schema_from_json(item)
        return loaded

    def dump(self, item: Schema) -> ExternalType:
        return item.schema
