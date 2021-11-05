from typing import Optional, List, Iterator, Dict

from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError


class BooleanSchema(SchemaABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BooleanSchema, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_schema_errors(self,
                          item: bool,
                          defs: Optional[Dict[str, SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        if not isinstance(item, bool):
            yield SchemaError(current_path or [], 'type', item)

    def __repr__(self):
        return 'BooleanSchema()'
