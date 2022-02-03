from dataclasses import dataclass
from typing import Optional, List, Iterator, Union, Type

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class BooleanSchema(JsonSchemaABC):
    default_value: Union[bool, Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item: bool, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, bool):
            yield SchemaError(current_path or [], 'type', item)
