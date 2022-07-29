from typing import Type, Optional, Union, Dict

import typing_inspect
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


class AnyOfSchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def from_type(
        self, type_: Type, context: SchemaContext, path: str
    ) -> Optional[Schema]:
        origin = typing_inspect.get_origin(type_)
        if origin == Union:
            args = typing_inspect.get_args(type_)
            schemas = {
                "anyOf": [
                    context.schema_from_type(a, f"{path}/anyOf/{i}").schema
                    for i, a in enumerate(args)
                ]
            }
            return Schema(schemas, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        any_of = item.get("anyOf")
        if any_of:
            schemas = (
                context.schema_from_json(a, f"{path}/anyOf/{i}", ref_schemas)
                for i, a in enumerate(any_of)
            )
            union = Union[tuple(s.python_type for s in schemas)]
            return Schema(item, union)
