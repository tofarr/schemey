from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Type

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class NullSchema(JsonSchemaABC):
    default_value: Union[type(None), Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item is not None:
            yield SchemaError(current_path or [], 'type', item)
