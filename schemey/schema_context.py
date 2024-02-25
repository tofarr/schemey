from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Type

from injecty import InjectyContext, get_default_injecty_context
from marshy import create_marshy_context, MarshyContext, get_default_marshy_context
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema

# Referencing by name prevents circular reference
SchemaFactoryABC_ = "schemey.factory.schema_factory_abc.SchemaFactoryABC"


@dataclass
class SchemaContext:
    factories: List[SchemaFactoryABC_] = field(default_factory=list)
    marshy_context: MarshyContext = field(default_factory=create_marshy_context)

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


def create_schema_context(
    marshy_context: Optional[MarshyContext] = None,
    injecty_context: Optional[InjectyContext] = None,
) -> SchemaContext:
    if marshy_context is None:
        if injecty_context:
            marshy_context = create_marshy_context(injecty_context)
        else:
            marshy_context = get_default_marshy_context()
    if injecty_context is None:
        injecty_context = get_default_injecty_context()
    context = SchemaContext(
        factories=injecty_context.get_instances(SchemaFactoryABC),
        marshy_context=marshy_context,
    )
    return context
