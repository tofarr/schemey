from typing import Union, Optional, List, Iterator

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_error import SchemaError


class DefsSchema(JsonSchemaABC):

    def get_schema_errors(self, item: ExternalItemType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        pass

    @property
    def default_value(self) -> Union[NoDefault, ExternalItemType]:
        pass