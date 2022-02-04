from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, Union, TypeVar

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalItemType

from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault

T = TypeVar('T')
_DeferredSchema = 'schemey.deferred_schema.DeferredSchema'


@dataclass
class JsonSchemaContext:
    defs: Dict[str, _DeferredSchema] = field(default_factory=dict)
    defs_path: str = '#$defs'
    loaders: Optional[List[JsonSchemaLoaderABC]] = None
    factories: Optional[List[JsonSchemaFactoryABC]] = None
    marshaller_context: MarshallerContext = field(default_factory=get_default_context)

    def load(self, item: ExternalItemType) -> JsonSchemaABC:
        for loader in self.loaders:
            schema = loader.load(item, self)
            if schema:
                return schema
        raise ValueError(f'could_not_load:{item}')

    def create_schema(self, item_type: Type[T], default: Union[T, NoDefault] = NoDefault) -> JsonSchemaABC:
        for factory in self.factories:
            schema = factory.create(item_type, self, default)
            if schema:
                return schema
        raise ValueError(f'could_not_create:{item_type}:{default}')
