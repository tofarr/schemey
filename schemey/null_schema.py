from typing import Optional, List, Iterator, Type

from marshy.types import ExternalItemType

from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

NULL = 'null'


class NullSchema(SchemaABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NullSchema, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_schema_errors(self, item, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item is not None:
            yield SchemaError(current_path or [], 'type', item)

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        return dict(type=NULL)

    def __repr__(self):
        return 'NullSchema()'

    @property
    def item_type(self) -> Type:
        return type(None)

    @property
    def default_value(self):
        return None
