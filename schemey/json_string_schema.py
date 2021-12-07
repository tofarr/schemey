import json
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional, List, Iterator, Type, TypeVar
from marshy.types import ExternalItemType, ExternalType
from typing_inspect import get_origin

from schemey._util import filter_none
from schemey.graphql.graphql_attr import GraphqlAttr
from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

T = TypeVar('T', bound=ExternalType)


@dataclass(frozen=True)
class JsonStringSchema(SchemaABC[T]):
    """
    Schema that indicates that the output data structure includes a string which contains encoded json.
    This is occasionally useful as technologies like graphql do not allow freeform data at all.
    """
    _item_type: Type[T]
    default_value: Optional[T] = None

    @property
    def item_type(self) -> Type[T]:
        return self._item_type

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        return filter_none(dict(
            type='string',
            format='json_object' if get_origin(self._item_type) is dict else 'json',
            default=None if self.default_value is None else json.dumps(self.default_value)
        ))

    def get_schema_errors(self, item: str, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, str):
            yield SchemaError(current_path, 'type', item)
            return
        try:
            loaded = json.loads(item)
            if type(loaded) is not dict and get_origin(self._item_type) is dict:
                yield SchemaError(current_path, 'not_an_object', loaded)
        except JSONDecodeError:
            yield SchemaError(current_path, 'format:json', item)

    def to_graphql_attr(self) -> GraphqlAttr:
        return GraphqlAttr('String')
