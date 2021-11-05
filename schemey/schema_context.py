import importlib
import os
from typing import Type, TypeVar, Optional, Dict

from marshy.utils import resolve_forward_refs

from schemey.with_defs_schema import WithDefsSchema

T = TypeVar('T')
_SchemaFactoryABC = 'schemey.factory.schema_factory_abc.SchemaFactoryABC'
_SchemaABC = 'schemey.schema_abc.SchemaABC'


class SchemaContext:

    def __init__(self,
                 factories: Optional[_SchemaFactoryABC] = None,
                 by_type: Optional[Dict[Type, _SchemaABC]] = None):
        self._factories = sorted(factories or [], reverse=True)
        self._by_type = dict(by_type or {})

    def get_schema(self, type_: Type[T], defs: Dict[str, _SchemaABC] = None) -> _SchemaABC:
        schema = self._by_type.get(type_)
        if not schema:
            local_defs = {} if defs is None else defs
            resolved_type = resolve_forward_refs(type_)
            for factory in self._factories:
                schema = factory.create(resolved_type, self, local_defs)
                if schema:
                    break
            if not schema:
                raise ValueError(f'no_schema_for_type:{type_}')
            if local_defs is not defs and local_defs:
                schema = WithDefsSchema(local_defs, schema)
            self._by_type[type_] = schema
        return schema

    def register_factory(self, schema_factory: _SchemaFactoryABC):
        self._factories.append(schema_factory)
        self._factories = sorted(self._factories or [], reverse=True)

    def register_schema(self, type_, schema: _SchemaABC):
        self._by_type[type_] = schema


_default_context = None
SCHEMA_CONTEXT = 'SCHEMA_CONTEXT'


def get_default_schema_context() -> SchemaContext:
    global _default_context
    if not _default_context:
        # Set up the default_context based on an environment variable
        import_name = os.environ.get(SCHEMA_CONTEXT, 'schemey.default_schema_context.DefaultSchemaContext')
        import_path = import_name.split('.')
        import_module = '.'.join(import_path[:-1])
        imported_module = importlib.import_module(import_module)
        context_fn = getattr(imported_module, import_path[-1])
        _default_context = context_fn()
    return _default_context


def schema_for_type(type_: Type[T], schema_context: Optional[SchemaContext] = None) -> _SchemaABC:
    if schema_context is None:
        schema_context = get_default_schema_context()
    schema = schema_context.get_schema(type_)
    return schema
