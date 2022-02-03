import importlib
import pkgutil
from dataclasses import dataclass, field
from typing import List, Dict, Type, Union, TypeVar

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalItemType, ExternalType
from marshy.utils import resolve_forward_refs

from schemey._util import secure_hash
from schemey.ref_schema import RefSchema
from schemey.schema import Schema
from schemey.schema_key import SchemaKey
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC

T = TypeVar('T')


@dataclass
class SchemeyContext:
    schema_jsonifiers: List[SchemaJsonifierABC] = field(default_factory=list)
    schema_factories: List[SchemaFactoryABC] = field(default_factory=list)
    schema_cache: Dict[SchemaKey, Schema] = field(default_factory=dict)
    marshaller_context: MarshallerContext = field(default_factory=get_default_context)

    def __post_init__(self):
        self.schema_factories.sort()

    def get_schema(self, item_type: Type[T], default_value: Union[T, NoDefault] = NoDefault) -> Schema:
        if default_value is not NoDefault:
            default_value = self.marshaller_context.dump(default_value, item_type)
        cache_key = self.key_for_schema(item_type, default_value)
        schema = self.schema_cache.get(cache_key)
        if not schema:
            resolved_type = resolve_forward_refs(item_type)
            ref_schema = RefSchema()  # Setting a ref_schema here means we handle self references
            schema = Schema(ref_schema, self.marshaller_context.get_marshaller(resolved_type))
            self.schema_cache[cache_key] = schema
            json_schema = None
            for factory in self.schema_factories:
                json_schema = factory.create(resolved_type, self, default_value)
                if json_schema:
                    break
            if not json_schema:
                raise ValueError(f'no_schema_for_type:{item_type}')
            ref_schema.schema = json_schema
            schema.json_schema = json_schema
        return schema

    def register_factory(self, schema_factory: SchemaFactoryABC):
        self.schema_factories.append(schema_factory)
        self.schema_factories.sort()

    def register_jsonifier(self, jsonifier: SchemaJsonifierABC):
        self.schema_jsonifiers.append(jsonifier)
        self.schema_jsonifiers.sort()

    def key_for_schema(self, item_type, default_value: Union[ExternalType, NoDefault]):
        default_value_hash = None
        if default_value is not NoDefault:
            default_value_hash = secure_hash(default_value)
        return SchemaKey(item_type, default_value_hash)

    def dump_json_schema(self, schema: JsonSchemaABC, defs_path: str = '#$defs') -> ExternalItemType:
        from schemey.jsonifier.json_dump import JsonDump
        dump = JsonDump(self, defs_path=defs_path)
        dumped = dump.dump(schema)
        return dumped

    def load_json_schema(self, item: ExternalItemType) -> JsonSchemaABC:
        from schemey.jsonifier.json_load import JsonLoad
        load = JsonLoad(self, item)
        loaded = load.load(item)
        return loaded


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
