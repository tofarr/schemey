from dataclasses import dataclass
from typing import Optional, List, Iterator, Union

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_error import SchemaError


@dataclass
class RefSchema(JsonSchemaABC):
    schema: Optional[JsonSchemaABC] = None

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        yield from self.schema.get_schema_errors(item, current_path)

    @property
    def default_value(self) -> Union[NoDefault, ExternalItemType]:
        return self.schema.default_value
