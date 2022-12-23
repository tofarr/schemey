from typing import Type, Optional, Set, List, Tuple, Union, Dict, FrozenSet

import typing_inspect
from marshy.types import ExternalItemType
from marshy.utils import resolve_forward_refs

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


class ArraySchemaFactory(SchemaFactoryABC):
    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        array_type = self.get_array_type(type_)
        if array_type:
            schema = {"type": "array"}
            args = typing_inspect.get_args(type_)
            if args:
                item_type = resolve_forward_refs(args[0])
                if item_type and not typing_inspect.is_typevar(item_type):
                    item_schema = context.schema_from_type(
                        item_type, f"{path}/items", ref_schemas
                    )
                    schema["items"] = item_schema.schema
            if array_type in (Set, FrozenSet):
                schema["uniqueItems"] = True
            if array_type in (Tuple, FrozenSet):
                schema["frozen"] = True  # Custom annotation
            return Schema(schema, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        if item.get("type") == "array":
            type_ = List
            if item.get("uniqueItems") is True:
                if item.get("frozen") is True:  # Custom annotation
                    type_ = FrozenSet
                else:
                    type_ = Set
            elif item.get("frozen") is True:  # Custom annotation
                type_ = Tuple
            items = item.get("items")
            if not items:
                return Schema(item, type_)
            # noinspection PyTypeChecker
            item_schema = context.schema_from_json(items, f"{path}/items", ref_schemas)
            if type_ is Tuple:
                # noinspection PyTypeChecker
                python_type = type_[item_schema.python_type, ...]
            else:
                # noinspection PyTypeChecker
                python_type = type_[item_schema.python_type]
            return Schema(item, python_type)

    @staticmethod
    def get_array_type(
        type_: Type,
    ) -> Union[Type[List], Type[Set], Type[Tuple], Type[FrozenSet], None]:
        origin = typing_inspect.get_origin(type_)
        if origin is list:
            return List
        if origin is set:
            return Set
        if origin is frozenset:
            return FrozenSet
        if origin is tuple:
            args = typing_inspect.get_args(type_)
            if len(args) == 2 and args[1] is Ellipsis:
                return Tuple
