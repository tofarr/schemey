import importlib
import pkgutil
from typing import Optional, Type

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalItemType

from schemey.schema import Schema
from schemey.schema_context import SchemaContext

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


def schema_from_type(type_: Type) -> Schema:
    return get_default_schema_context().schema_from_type(type_)


def schema_from_json(item: ExternalItemType) -> Schema:
    return get_default_schema_context().schema_from_json(item)
