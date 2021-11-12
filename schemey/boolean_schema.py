from typing import Optional, List, Iterator, Type

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

_true = None
_false = None
BOOLEAN = 'boolean'


class BooleanSchema(SchemaABC[bool]):

    def __init__(self, default_value: bool = False):
        self._default_value = default_value

    def __new__(cls, *args, **kwargs):
        global _true, _false
        if _true is None or _false is None:
            _true = super(BooleanSchema, cls).__new__(cls, default_value=True)
            _false = super(BooleanSchema, cls).__new__(cls, default_value=False)
        if (len(args) and args[0]) or kwargs.get('default_value'):
            return _true
        return _false

    @property
    def item_type(self) -> Type[bool]:
        return bool

    @property
    def default_value(self):
        return self._default_value

    def get_schema_errors(self, item: bool, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, bool):
            yield SchemaError(current_path or [], 'type', item)

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        return filter_none(dict(type=BOOLEAN, default=self.default_value or None))

    def __repr__(self):
        return 'BooleanSchema()'
