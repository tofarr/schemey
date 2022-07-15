import importlib
import pkgutil
from dataclasses import dataclass, field
from typing import List, Dict, Type, TypeVar, Optional

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.utils import resolve_forward_refs

from schemey.json_schema_context import JsonSchemaContext
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.obj_schema import ObjSchema

T = TypeVar("T")


@dataclass
class SchemaContext:
    schema_loaders: List[SchemaLoaderABC] = field(default_factory=list)
    schema_factories: List[SchemaFactoryABC] = field(default_factory=list)
    schemas: Dict[Type, SchemaABC] = field(default_factory=dict)
    marshaller_context: MarshallerContext = field(default_factory=get_default_context)

    def __post_init__(self):
        self.schema_factories.sort()

    def get_obj_schema(self, item_type: Type[T]) -> ObjSchema:
        schema = self.get_schema(item_type)
        schema = ObjSchema(schema, self.marshaller_context.get_marshaller(item_type))
        return schema

    def get_schema(self, item_type: Type[T]) -> SchemaABC:
        item_type = resolve_forward_refs(item_type)
        schema = self.schemas.get(item_type)
        if schema:
            return schema
        json_schema_context = JsonSchemaContext(
            schemas={**self.schemas}, factories=self.schema_factories
        )
        schema = json_schema_context.get_schema(item_type)
        schema = schema.simplify()
        self.schemas[item_type] = schema
        return schema

    def register_schema(self, item_type: Type, schema: SchemaABC):
        item_type = resolve_forward_refs(item_type)
        self.schemas[item_type] = schema

    def register_factory(self, schema_factory: SchemaFactoryABC):
        self.schema_factories.append(schema_factory)
        self.schema_factories.sort(reverse=True)

    def register_loader(self, jsonifier: SchemaLoaderABC):
        self.schema_loaders.append(jsonifier)
        self.schema_loaders.sort(reverse=True)


_default_context = None
CONFIG_MODULE_PREFIX = "schemey_config_"


def get_default_schema_context() -> SchemaContext:
    global _default_context
    if not _default_context:
        _default_context = new_default_schema_context()
    return _default_context


def new_default_schema_context(
    marshaller_context: Optional[MarshallerContext] = None,
) -> SchemaContext:
    if marshaller_context is None:
        marshaller_context = get_default_context()
    context = SchemaContext(marshaller_context=marshaller_context)
    # Set up context based on naming convention
    module_info = (
        m for m in pkgutil.iter_modules() if m.name.startswith(CONFIG_MODULE_PREFIX)
    )
    modules = [importlib.import_module(m.name) for m in module_info]
    modules.sort(key=lambda m: m.priority, reverse=True)
    for m in modules:
        getattr(m, "configure")(context)
    return context


def schema_for_type(
    type_: Type[T], context: Optional[SchemaContext] = None
) -> ObjSchema:
    if context is None:
        context = get_default_schema_context()
    schema = context.get_obj_schema(type_)
    return schema
