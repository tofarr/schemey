import importlib
import pkgutil
from dataclasses import dataclass, field
from typing import List, Dict, Type, Union, TypeVar

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalType
from marshy.utils import resolve_forward_refs

from schemey._util import secure_hash

from schemey.json_schema_context import JsonSchemaContext
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema import Schema

T = TypeVar('T')


@dataclass
class SchemeyContext:
    schema_loaders: List[JsonSchemaLoaderABC] = field(default_factory=list)
    schema_factories: List[JsonSchemaFactoryABC] = field(default_factory=list)
    schema_cache: Dict[str, Schema] = field(default_factory=dict)
    marshaller_context: MarshallerContext = field(default_factory=get_default_context)

    def __post_init__(self):
        self.schema_factories.sort()

    def get_json_schema(self, item_type: Type[T], default: Union[T, NoDefault] = NoDefault) -> JsonSchemaABC:
        return self.get_schema(item_type, default).json_schema

    def get_schema(self, item_type: Type[T], default: Union[T, NoDefault] = NoDefault) -> Schema:
        if default is not NoDefault:
            default = self.marshaller_context.dump(default, item_type)
        key = self.key_for_schema(item_type, default)
        schema = self.schema_cache.get(key)
        if schema:
            return schema
        item_type = resolve_forward_refs(item_type)
        json_schema_context = JsonSchemaContext(factories=self.schema_factories)
        schema = json_schema_context.create_schema(item_type, default)
        schema = schema.simplify()
        schema = Schema(schema, self.marshaller_context.get_marshaller(item_type))
        self.schema_cache[key] = schema
        return schema

    def register_factory(self, schema_factory: JsonSchemaFactoryABC):
        self.schema_factories.append(schema_factory)
        self.schema_factories.sort()

    def register_loader(self, jsonifier: JsonSchemaLoaderABC):
        self.schema_loaders.append(jsonifier)
        self.schema_loaders.sort()

    def key_for_schema(self, item_type, default_value: Union[ExternalType, NoDefault]):
        key = str(item_type)
        if default_value is not NoDefault:
            key = f"{key}:{secure_hash(default_value)}"
        return key


_default_context = None
CONFIG_MODULE_PREFIX = 'schemey_config_'


def get_default_schemey_context() -> SchemeyContext:
    global _default_context
    if not _default_context:
        _default_context = new_default_schemey_context()
    return _default_context


def new_default_schemey_context() -> SchemeyContext:
    context = SchemeyContext()
    # Set up context based on naming convention
    module_info = (m for m in pkgutil.iter_modules() if m.name.startswith(CONFIG_MODULE_PREFIX))
    modules = [importlib.import_module(m.name) for m in module_info]
    modules.sort(key=lambda m: m.priority, reverse=True)
    for m in modules:
        getattr(m, 'configure')(context)
    return context
