from typing import Type, Optional, Tuple, Dict

import typing_inspect
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


class TupleSchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def from_type(
        self, type_: Type, context: SchemaContext, path: str
    ) -> Optional[Schema]:
        origin = typing_inspect.get_origin(type_)
        if origin is tuple:
            args = typing_inspect.get_args(type_)
            if len(args) == 2 and args[1] is Ellipsis:
                return
            schema = {
                "type": "array",
                "prefixItems": [
                    context.schema_from_type(a, f"{path}/prefixItems/{i}").schema
                    for i, a in enumerate(args)
                ],
                "items": False,
            }
            return Schema(schema, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        type_ = item.get("type")
        prefix_items = item.get("prefixItems")
        if type_ == "array" and prefix_items and item.get("items") is False:
            args = tuple(
                context.schema_from_json(
                    a, f"{path}/prefixItems/{i}", ref_schemas
                ).python_type
                for i, a in enumerate(prefix_items)
            )
            python_type = Tuple[args]
            return Schema(item, python_type)
