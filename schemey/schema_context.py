from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Type, Callable

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalItemType

from schemey.schema import Schema

# Referencing by name prevents circular reference
SchemaFactoryABC_ = "schemey.factory.schema_factory_abc.SchemaFactoryABC"


@dataclass
class SchemaContext:
    factories: List[SchemaFactoryABC_] = field(default_factory=list)
    marshaller_context: MarshallerContext = field(default_factory=get_default_context)
    custom_validators: Dict[str, Callable] = field(default_factory=dict)

    def register_factory(self, schema_factory: SchemaFactoryABC_):
        self.factories.append(schema_factory)
        self.factories.sort(reverse=True)

    def schema_from_type(
        self,
        type_,
        path: Optional[str] = "#",
        ref_schemas: Optional[Dict[Type, Schema]] = None,
    ) -> Schema:
        if ref_schemas is None:
            ref_schemas = {}
        schema = ref_schemas.get(type_)
        if schema:
            return schema
        for factory in self.factories:
            schema = factory.from_type(type_, self, path, ref_schemas)
            if schema:
                return schema
        raise ValueError(f"no_schema_for_type:{type_}")

    def schema_from_json(
        self,
        item: ExternalItemType,
        path: str = "#",
        ref_schemas: Optional[Dict[str, Schema]] = None,
    ) -> Schema:
        if ref_schemas is None:
            ref_schemas = {}
        for factory in self.factories:
            schema = factory.from_json(item, self, path, ref_schemas)
            if schema:
                return schema
        raise ValueError(f"no_schema_for_json:{item}")
