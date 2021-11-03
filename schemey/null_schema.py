from dataclasses import dataclass
from typing import Optional, List, Iterator

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError


class NullSchema(SchemaABC[bool]):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NullSchema, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_schema_errors(self, item: bool, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item is not None:
            yield SchemaError(current_path or [], 'type', item)

    def __repr__(self):
        return 'NullSchema()'
