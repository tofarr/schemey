from dataclasses import dataclass, field
from typing import Type

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.deferred_schema import DeferredSchema
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_context import SchemaContext, get_default_schema_context


@dataclass(frozen=True)
class SchemaMarshaller(MarshallerABC[SchemaABC]):
    marshalled_type: Type[SchemaABC] = SchemaABC
    schemey_context: SchemaContext = field(default_factory=get_default_schema_context)
    defs_key: str = "$defs"

    def load(self, item: ExternalItemType) -> SchemaABC:
        raw_defs = item.get(self.defs_key) or {}
        defs = {k: DeferredSchema(k) for k in raw_defs}
        json_schema_context = JsonSchemaContext(
            defs=defs,
            loaders=self.schemey_context.schema_loaders,
            defs_path=f"#{self.defs_key}/",
        )
        for k, raw_def in raw_defs.items():
            deferred = defs[k]
            deferred.schema = json_schema_context.load(raw_def)
        schema = json_schema_context.load(item)
        schema = schema.simplify()
        return schema

    def dump(self, item: SchemaABC) -> ExternalType:
        json_context = JsonSchemaContext()
        dumped = item.dump_json_schema(json_context)
        if json_context.defs:
            dumped[self.defs_key] = {
                k: s.schema.dump_json_schema(json_context)
                for k, s in json_context.defs.items()
                if s.num_usages > 1
            }
        return dumped
