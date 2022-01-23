import importlib
import pkgutil
from typing import Type, TypeVar, Optional, Dict, Iterator

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.utils import resolve_forward_refs

from schemey._util import secure_hash
from schemey.schema_key import SchemaKey

T = TypeVar('T')
_SchemaFactoryABC = 'schemey.factory.schema_factory_abc.SchemaFactoryABC'
_SchemaABC = 'schemey.schema_abc.SchemaABC'


class SchemaContext:

    def __init__(self,
                 factories: Optional[_SchemaFactoryABC] = None,
                 schema_cache: Optional[Dict[SchemaKey, _SchemaABC]] = None,
                 marshaller_context: Optional[MarshallerContext] = None):
        self._factories = sorted(factories or [], reverse=True)
        self._schema_cache = dict(schema_cache or {})
        self._marshaller_context = marshaller_context or get_default_context()

    def get_schema(self, type_: Type[T], default_value: Optional[T] = None) -> _SchemaABC:
        from schemey.deferred_schema import DeferredSchema
        cache_key = self.key_for_schema(type_, default_value)
        schema = self._schema_cache.get(cache_key)
        if not schema:
            resolved_type = resolve_forward_refs(type_)
            self._schema_cache[cache_key] = DeferredSchema(self, type_, default_value)
            for factory in self._factories:
                schema = factory.create(resolved_type, default_value, self)
                if schema:
                    break
            if not schema:
                raise ValueError(f'no_schema_for_type:{type_}')
            self._schema_cache[cache_key] = schema
        return schema

    def register_factory(self, schema_factory: _SchemaFactoryABC):
        self._factories.append(schema_factory)
        self._factories = sorted(self._factories or [], reverse=True)

    def register_schema(self, schema: _SchemaABC):
        key = self.key_for_schema(schema.item_type, schema.default_value)
        self._schema_cache[key] = schema

    def key_for_schema(self, item_type, default_value):
        default_value_hash = None
        if default_value is not None:
            default_value_str = self._marshaller_context.dump(default_value, item_type)
            default_value_hash = secure_hash(default_value_str)
        return SchemaKey(item_type, default_value_hash)

    def get_factories(self) -> Iterator[_SchemaFactoryABC]:
        return iter(self._factories)


_default_context = None
CONFIG_MODULE_PREFIX = 'schemey_config_'


def get_default_schema_context() -> SchemaContext:
    global _default_context
    if not _default_context:
        _default_context = new_default_schema_context()
    return _default_context


def new_default_schema_context() -> SchemaContext:
    context = SchemaContext()
    # Set up context based on naming convention
    module_info = (m for m in pkgutil.iter_modules() if m.name.startswith(CONFIG_MODULE_PREFIX))
    modules = [importlib.import_module(m.name) for m in module_info]
    modules.sort(key=lambda m: m.priority, reverse=True)
    for m in modules:
        getattr(m, 'configure')(context)
    return context


def schema_for_type(type_: Type[T],
                    schema_context: Optional[SchemaContext] = None,
                    default_value: Optional[T] = None
                    ) -> _SchemaABC:
    if schema_context is None:
        schema_context = get_default_schema_context()
    schema = schema_context.get_schema(type_, default_value)
    return schema
