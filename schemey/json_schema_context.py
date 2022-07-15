from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_abc import SchemaABC

_DeferredSchema = "schemey.deferred_schema.DeferredSchema"


@dataclass
class JsonSchemaContext:
    defs: Dict[str, _DeferredSchema] = field(default_factory=dict)
    defs_path: str = "#$defs"
    schemas: Optional[Dict[Type, SchemaABC]] = field(default_factory=dict)
    loaders: Optional[List[SchemaLoaderABC]] = None
    factories: Optional[List[SchemaFactoryABC]] = None
    marshaller_context: MarshallerContext = field(default_factory=get_default_context)

    def load(self, item: ExternalItemType) -> SchemaABC:
        for loader in self.loaders:
            schema = loader.load(item, self)
            if schema:
                return schema
        raise ValueError(f"could_not_load:{item}")

    def get_schema(self, item_type: Type) -> SchemaABC:
        schema = self.schemas.get(item_type)
        if schema:
            return schema
        for factory in self.factories:
            schema = factory.create(item_type, self)
            if schema:
                self.schemas[item_type] = schema
                return schema
        raise ValueError(f"could_not_create:{item_type}")
