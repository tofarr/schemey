from typing import Optional, List, Iterator, Dict

from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError


class NullSchema(SchemaABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NullSchema, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_schema_errors(self,
                          item,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        if item is not None:
            yield SchemaError(current_path or [], 'type', item)

    def __repr__(self):
        return 'NullSchema()'
