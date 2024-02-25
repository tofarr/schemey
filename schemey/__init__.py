from typing import Type

from marshy.types import ExternalItemType

from schemey.schema import Schema
from schemey.schema_context import SchemaContext, create_schema_context

_default_context = None
CONFIG_MODULE_PREFIX = "schemey_config_"


# pylint: disable=W0603
def get_default_schema_context() -> SchemaContext:
    global _default_context
    if not _default_context:
        _default_context = create_schema_context()
    return _default_context


def schema_from_type(type_: Type) -> Schema:
    return get_default_schema_context().schema_from_type(type_)


def schema_from_json(item: ExternalItemType) -> Schema:
    return get_default_schema_context().schema_from_json(item)
